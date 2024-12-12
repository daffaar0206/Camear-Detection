import cv2
import numpy as np
import requests
import json
import base64
from datetime import datetime, timedelta
import os
import asyncio
import edge_tts
import threading
from queue import Queue
import tempfile
from playsound import playsound
from ultralytics import YOLO
import time

# OpenRouter API configuration
OPENROUTER_API_KEY = "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"
YOUR_SITE_URL = "http://localhost"
YOUR_APP_NAME = "CCTV Detector"

# RTSP Configuration
# Ganti dengan URL RTSP kamera CCTV Anda
RTSP_URL = "rtsp://username:password@ip_address:port/stream"

# Create temp directory for speech files
TEMP_DIR = os.path.join(tempfile.gettempdir(), "cctv_detector")
os.makedirs(TEMP_DIR, exist_ok=True)

# Initialize YOLO model
model = YOLO('yolov8n.pt')

# Global variables
last_analysis_time = datetime.now() - timedelta(minutes=1)
detection_in_progress = False

def speak_text(text):
    """Synchronous function to speak text"""
    try:
        speech_file = os.path.join(TEMP_DIR, f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
        communicate = edge_tts.Communicate(text, "id-ID-GadisNeural")
        asyncio.run(communicate.save(speech_file))
        playsound(speech_file)
        try:
            os.remove(speech_file)
        except:
            pass
    except Exception as e:
        print(f"Error in speak_text: {str(e)}")

def speak(text):
    """Non-blocking function to speak text"""
    print(f"Speaking: {text}")
    threading.Thread(target=speak_text, args=(text,), daemon=True).start()

def analyze_image(image_path):
    """Send image to AI for analysis"""
    try:
        print("Starting image analysis...")
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        image_url = f"data:image/jpeg;base64,{encoded_string}"
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": YOUR_SITE_URL,
            "X-Title": YOUR_APP_NAME,
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "google/learnlm-1.5-pro-experimental:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "anggap anda adalah sebuah cctv, dan apabila ada foto yang terkirim anggap itu adalah frame dari sebuah video cctv. gunakan bahasa indonesia, ada berapa orang di gambar dan sedang membawa apa, tidak perlu menjelasakan lebih panjang lagi. hanya jawab ada berapa orang dan membawa apa."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ]
        }
        
        print("Sending request to AI API...")
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            print(f"API Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return "Error menganalisis gambar"
            
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error in analyze_image: {str(e)}")
        return f"Error menganalisis gambar: {str(e)}"

def detect_person(frame):
    """Detect people in the frame using YOLOv8"""
    try:
        results = model(frame, conf=0.5)
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                if box.cls[0] == 0:  # Class 0 is person
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    conf = float(box.conf[0])
                    cv2.putText(frame, f'Person: {conf:.2f}', (x1, y1-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    return True
        return False
    except Exception as e:
        print(f"Error in person detection: {str(e)}")
        return False

def process_detection_async(cap):
    """Process detection asynchronously"""
    try:
        print("Menunggu 4 detik untuk foto yang sempurna...")
        time.sleep(4)
        
        # Capture the frame after waiting
        ret, frame = cap.read()
        if not ret:
            print("Error capturing frame")
            return
            
        os.makedirs('captures', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join('captures', f"person_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        
        if os.path.exists(image_path):
            analysis = analyze_image(image_path)
            if analysis:
                speak(analysis)
    except Exception as e:
        print(f"Error in process_detection_async: {str(e)}")

def connect_to_cctv():
    """Connect to CCTV camera"""
    print(f"Connecting to CCTV at {RTSP_URL}...")
    cap = cv2.VideoCapture(RTSP_URL)
    
    # Set buffer size to reduce delay
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Optional: set frame width and height if needed
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    return cap

def main():
    global last_analysis_time, detection_in_progress
    
    try:
        print("Starting CCTV detection system...")
        
        # Connect to CCTV
        cap = connect_to_cctv()
        
        if not cap.isOpened():
            print("Error: Could not connect to CCTV camera")
            print("Please check:")
            print("1. RTSP URL is correct")
            print("2. Camera is powered on")
            print("3. Network connection is stable")
            print("4. Username and password are correct")
            return
            
        print("Successfully connected to CCTV camera")
        print("System ready. Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Lost connection to CCTV")
                print("Attempting to reconnect...")
                cap.release()
                cap = connect_to_cctv()
                if not cap.isOpened():
                    print("Reconnection failed. Exiting...")
                    break
                continue
            
            # Optional: resize frame if too large
            # frame = cv2.resize(frame, (640, 480))
                
            # Show frame
            cv2.imshow('CCTV Person Detection', frame)
            
            # Check for person
            current_time = datetime.now()
            if not detection_in_progress and (current_time - last_analysis_time).total_seconds() > 30:
                if detect_person(frame):
                    detection_in_progress = True
                    speak("Ada orang")
                    threading.Thread(target=process_detection_async, 
                                  args=(cap,), 
                                  daemon=True).start()
                    last_analysis_time = current_time
                    detection_in_progress = False
            
            # Break loop with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"Error in main function: {str(e)}")
    finally:
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
