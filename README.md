# 🎯 VisionTrack AI
### Real-Time Object Detection and Tracking System

VisionTrack AI is a computer vision application built using Python, YOLOv8, ByteTrack, OpenCV, and Streamlit. It detects and tracks multiple objects in uploaded videos and through a live webcam.

## 🚀 Features

- Real-time object detection using YOLOv8.
- Object tracking using ByteTrack.
- Upload and process MP4, AVI, and MOV videos.
- Live object detection using a webcam.
- Display bounding boxes and object labels.
- Show the number of detected objects.
- Display object-wise detection analytics.
- Interactive dashboard built with Streamlit.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| YOLOv8 | Object detection |
| ByteTrack | Object tracking |
| OpenCV | Video and image processing |
| Streamlit | Web application interface |
| Streamlit-WebRTC | Live webcam streaming |

## 📂 Project Structure

```text
VisionTrack-AI/
│
├── app.py
├── detector.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── screenshots/
│   ├── 01_homepage.png
│   ├── 02_video_upload.png
│   ├── 03_video_detection.png
│   ├── 04_live_analytics.png
│   └── 05_webcam_detection.png
│
└── .streamlit/
    └── config.toml
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/gauribaravkar/VisionTrack-AI.git
```

### 2. Open the Project Folder

```bash
cd VisionTrack-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📸 Application Screenshots

### 1. Homepage
<img width="1912" height="927" alt="dashboard" src="https://github.com/user-attachments/assets/63cafff4-f67d-403f-82fd-dad7aebe12e7" />

### 2. Video Upload
<img width="1917" height="916" alt="video detection" src="https://github.com/user-attachments/assets/529af24c-51df-4c92-81fa-586397b86af6" />

### 3. Object Detection Output
<img width="1892" height="906" alt="video detection 2" src="https://github.com/user-attachments/assets/540b2985-319b-4e7b-bbbf-df3e4b23b76a" />

### 4. Webcam Detection
<img width="1891" height="891" alt="webcam detection" src="https://github.com/user-attachments/assets/62c176a8-c598-4111-b096-db0ab9052e62" />

## ⚠️ Limitations

- Real-time performance depends on hardware capabilities.
- Webcam detection requires camera permission.
- Processing large videos may take additional time.
- CPU-based inference may be slower than GPU-based inference.
- YOLOv8 model weights may need to be downloaded on first execution.

## 🔮 Future Improvements

- Support more YOLO models.
- Improve detection accuracy.
- Add object counting across video frames.
- Export detection reports.
- Deploy the application online.
- Add support for more video formats.

## 🧠 How It Works

1. The user selects an input source: video upload or webcam.
2. OpenCV reads the video frames.
3. YOLOv8 detects objects in each frame.
4. ByteTrack tracks detected objects across frames.
5. Bounding boxes and object labels are displayed.
6. Streamlit displays detection results and analytics.

## 🎯 Project Objective

The objective of VisionTrack AI is to develop an interactive computer vision system that can detect and track multiple objects in videos and live webcam streams.

**Project:** Object Detection and Tracking  
**Category:** Artificial Intelligence / Computer Vision

Built with ❤️ using Python, YOLOv8, and Streamlit.
