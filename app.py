import streamlit as st
import cv2
import tempfile
import os
import av
import threading

from detector import detect_objects
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase


st.set_page_config(
    page_title="VisionTrack AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #080e1c;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background-color: #101a2d;
    border-right: 1px solid #263750;
}

.main-heading {
    color: #38bdf8 !important;
    font-size: 42px !important;
    font-weight: 900 !important;
    letter-spacing: 1.5px;
    text-shadow: 0 0 15px rgba(56, 189, 248, 0.35);
    margin-bottom: 5px;
}

h2, h3 {
    color: #f1f5f9 !important;
}

p, label {
    color: #cbd5e1;
}

div[data-testid="stMetric"] {
    background-color: #121e33;
    border: 1px solid #263a59;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricValue"] {
    color: #38bdf8;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 42px;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

[data-testid="stFileUploader"] {
    background-color: #121e33;
    border: 1px solid #263a59;
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stFileUploader"] section {
    background-color: #121e33;
}

hr {
    border-color: #263750;
}
</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown("## VisionTrack AI")
    st.caption("INTELLIGENT COMPUTER VISION")
    st.divider()

    st.markdown("### Input Source")
    input_type = st.radio(
        "Choose input source",
        ["Upload Video", "Webcam"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### Technologies")
    st.markdown("""
    🧠 YOLOv8

    🎯 ByteTrack

    👁️ OpenCV

    ⚡ Streamlit
    """)


# Main Header
st.markdown(
    '<h1 class="main-heading">🎯 VISIONTRACK AI</h1>',
    unsafe_allow_html=True
)

st.caption(
    "Real-Time Object Detection & Tracking System | "
    "Powered by YOLOv8 • ByteTrack • OpenCV"
)


# Video Upload
if input_type == "Upload Video":
    st.divider()
    st.markdown("### 📁 Upload Video")

    uploaded_file = st.file_uploader(
        "Choose your video file",
        type=["mp4", "avi", "mov"]
    )

    if uploaded_file is None:
        st.info("Upload an MP4, AVI or MOV video to start detection.")

    else:
        video_col, info_col = st.columns([2, 1])

        with video_col:
            st.video(uploaded_file)

        with info_col:
            st.markdown("### Video Information")
            st.write("**File Name:**", uploaded_file.name)
            st.write(
                "**File Size:**",
                f"{uploaded_file.size / (1024 * 1024):.2f} MB"
            )
            st.write(
                "**Format:**",
                uploaded_file.name.split(".")[-1].upper()
            )

        st.divider()

        if st.button(
            "▶ Start Object Detection",
            type="primary",
            use_container_width=True
        ):
            video_path = None
            cap = None

            try:
                suffix = os.path.splitext(uploaded_file.name)[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_video:
                    temp_video.write(uploaded_file.getvalue())
                    video_path = temp_video.name

                cap = cv2.VideoCapture(video_path)

                st.markdown("### 🔍 Detection Output")

                video_col, analytics_col = st.columns([2, 1])

                with video_col:
                    st.markdown("#### Processed Video")
                    video_placeholder = st.empty()

                with analytics_col:
                    st.markdown("#### Live Analytics")
                    total_placeholder = st.empty()
                    frame_placeholder = st.empty()
                    classes_placeholder = st.empty()

                frame_number = 0
                max_count = 0
                latest_classes = {}

                if not cap.isOpened():
                    st.error("Could not open the uploaded video.")

                else:
                    while cap.isOpened():
                        ret, frame = cap.read()

                        if not ret:
                            break

                        frame_number += 1

                        output, count, class_counts = detect_objects(frame)

                        max_count = max(max_count, count)
                        latest_classes = class_counts

                        output = cv2.cvtColor(
                            output,
                            cv2.COLOR_BGR2RGB
                        )

                        video_placeholder.image(
                            output,
                            channels="RGB",
                            use_container_width=True
                        )

                        total_placeholder.metric(
                            "Objects in Current Frame",
                            count
                        )

                        frame_placeholder.metric(
                            "Frames Processed",
                            frame_number
                        )

                        classes_placeholder.markdown(
                            "#### Object-wise Detection"
                        )

                        if class_counts:
                            classes_placeholder.json(class_counts)
                        else:
                            classes_placeholder.info("No objects detected.")

                    st.success("Video processing completed successfully!")

                    st.markdown("### Final Detection Summary")

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Total Frames Processed", frame_number)
                    col2.metric("Maximum Objects in One Frame", max_count)
                    col3.metric(
                        "Object Classes in Last Frame",
                        len(latest_classes)
                    )

            except Exception as e:
                st.error(f"Detection Error: {e}")

            finally:
                if cap is not None:
                    cap.release()

                if video_path and os.path.exists(video_path):
                    os.remove(video_path)


# Webcam Detection
elif input_type == "Webcam":
    st.markdown("### 📷 Live Webcam Detection")
    st.caption(
        "Allow camera permission in your browser to start detection."
    )

    class VisionTrackProcessor(VideoProcessorBase):
        def __init__(self):
            self.total_objects = 0
            self.class_counts = {}
            self.lock = threading.Lock()

        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            output, count, class_counts = detect_objects(img)

            with self.lock:
                self.total_objects = count
                self.class_counts = class_counts.copy()

            cv2.putText(
                output,
                f"Objects: {count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            return av.VideoFrame.from_ndarray(
                output,
                format="bgr24"
            )

    ctx = webrtc_streamer(
        key="visiontrack-webcam",
        video_processor_factory=VisionTrackProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        async_processing=True
    )

    st.divider()
    st.markdown("### 📈 Live Analytics")

    @st.fragment(run_every=1)
    def show_live_analytics():
        if ctx.state.playing and ctx.video_processor is not None:
            processor = ctx.video_processor

            with processor.lock:
                current_count = processor.total_objects
                current_classes = processor.class_counts.copy()

            col1, col2 = st.columns(2)
            col1.metric("Objects in Current Frame", current_count)
            col2.metric("Detected Classes", len(current_classes))

            st.markdown("#### Detected Classes")

            if current_classes:
                for class_name, count in current_classes.items():
                    st.write(f"**{class_name.capitalize()}**: {count}")
            else:
                st.info("No objects detected in the current frame.")

        else:
            col1, col2 = st.columns(2)
            col1.metric("Objects in Current Frame", 0)
            col2.metric("Detected Classes", 0)

            st.markdown("#### Detected Classes")
            st.info("Waiting for object detection...")

    show_live_analytics()
