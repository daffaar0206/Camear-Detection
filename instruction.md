Pendeteksi gerak

1. buat untuk membuka kamera
2. buat pendeteksi gerak
3. apabila terdapat sesuatu yang bergerak, ambil foto kemudian kirimkan ke ai
4. tanya ke ai apa yang terjadi ketika mengirim foto
5. ketika terdeteksi pergerakan print kata "ada orang"
6. gunakan fitur speak untuk membaca "ada orang" dan output dari ai

gunakan api request berikut
import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
    "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "google/learnlm-1.5-pro-experimental:free", # Optional
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What's in this image?"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            }
          }
        ]
      }
    ]
    
  })
)

api= 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