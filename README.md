# AI-Powered CCTV Person Detection System

Sistem deteksi orang menggunakan YOLOv8 dengan kemampuan text-to-speech dan analisis AI untuk kamera webcam atau CCTV.

## Fitur

- Deteksi orang real-time menggunakan YOLOv8
- Notifikasi suara otomatis saat mendeteksi orang
- Analisis AI untuk mendeskripsikan jumlah orang dan barang yang dibawa
- Mendukung webcam dan kamera CCTV (via RTSP)
- Penyimpanan otomatis gambar deteksi
- Delay 4 detik untuk mendapatkan gambar yang sempurna
- Cooldown 30 detik antara deteksi

## Persyaratan Sistem

- Python 3.8 atau lebih baru
- Webcam atau kamera CCTV dengan RTSP support
- Koneksi internet untuk analisis AI

## Instalasi

1. Clone repository ini:
```bash
git clone [URL_REPOSITORY_ANDA]
cd [NAMA_FOLDER]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Penggunaan

1. Untuk menggunakan webcam:
```bash
python main.py
```

2. Untuk menggunakan CCTV, edit `main.py` dan ganti `RTSP_URL` dengan URL RTSP kamera CCTV Anda:
```python
RTSP_URL = "rtsp://username:password@ip_address:port/stream"
```

## Konfigurasi RTSP URL

Format umum RTSP URL:
- Format umum: `rtsp://username:password@ip_address:port/stream1`
- Hikvision: `rtsp://username:password@ip_address:port/ch01/0`
- Dahua: `rtsp://username:password@ip_address:port/cam/realmonitor?channel=1&subtype=0`

## Fitur Detail

1. **Deteksi Orang**
   - Menggunakan YOLOv8 untuk deteksi akurat
   - Menampilkan bounding box dan confidence score

2. **Notifikasi**
   - Suara "Ada orang" saat deteksi
   - Deskripsi AI tentang jumlah orang dan barang yang dibawa

3. **Penyimpanan**
   - Menyimpan gambar di folder `captures`
   - Format nama file: `person_[TIMESTAMP].jpg`

4. **Kontrol**
   - Tekan 'q' untuk keluar dari program
   - Cooldown 30 detik antara deteksi untuk menghindari spam

## API Key

Program menggunakan OpenRouter API untuk analisis AI. Pastikan untuk mengganti `OPENROUTER_API_KEY` dengan API key Anda sendiri.

## Troubleshooting

1. **Kamera tidak terdeteksi**
   - Pastikan kamera terhubung dengan benar
   - Cek permission kamera
   - Untuk CCTV, pastikan URL RTSP benar dan dapat diakses

2. **Error Text-to-Speech**
   - Pastikan edge-tts terinstall dengan benar
   - Cek koneksi internet

3. **Error Analisis AI**
   - Verifikasi API key OpenRouter
   - Cek koneksi internet
   - Pastikan format gambar valid

## Kontribusi

Kontribusi selalu diterima! Silakan buat pull request atau laporkan issues.

## Lisensi

[daffaar0206]
