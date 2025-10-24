import streamlit as st
from shutil import copyfile
from object_counting import process_video_and_count, process_image_and_count
import tempfile
import os

# --- Simple Light CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        font-family: 'Poppins', sans-serif;
        color: #000000;
    }

    h1, h2, h3, h4, h5 {
        color: #1f4e79;
        font-weight: 600;
    }

    label, .stRadio label, .stMultiSelect label {
        color: #1f4e79 !important;
        font-weight: 500;
    }

    div[data-testid="stFileUploader"] {
        border: 1px solid #b0c4de;
        border-radius: 8px;
        background-color: #f8fafc;
        padding: 15px;
    }

    button[kind="primary"] {
        background-color: #1f4e79 !important;
        color: white !important;
        border-radius: 5px !important;
        font-weight: 500 !important;
        border: none !important;
    }

    .count-card {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 10px 15px;
        margin-top: 8px;
    }

    .count-card h4 {
        color: #1f4e79;
        margin-bottom: 4px;
    }

    .count-card p {
        margin: 0;
        font-weight: 600;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title('Object Detection and Counting')

# --- Input Type ---
input_type = st.radio("Select the input type:", ("Video", "Image"))

# --- File Uploader ---
if input_type == "Video":
    uploaded_file = st.file_uploader("Upload a video file (MP4):", type=["mp4"])
    file_type = "video"
else:
    uploaded_file = st.file_uploader("Upload an image file (JPG/PNG):", type=["jpg", "png"])
    file_type = "image"

# --- Object Classes ---
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

selected_classes = st.multiselect(
    'Select object classes to count:',
    options=classNames,
    default=['cup', 'fork', 'spoon', 'knife']
)

class_ids = [classNames.index(cls) for cls in selected_classes if cls in classNames]

# --- Processing ---
if uploaded_file is not None and len(selected_classes) > 0:
    with st.spinner('Processing...'):
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.type.split("/")[-1]}')
        tfile.write(uploaded_file.getvalue())
        file_path = tfile.name

        run_dir = "runs/temp"
        os.makedirs(run_dir, exist_ok=True)

        if file_type == "video":
            object_counts, output_path = process_video_and_count(file_path, 'yolov8s.pt', class_ids, run_dir)
            st.video(output_path)
        else:
            object_counts, output_path = process_image_and_count(file_path, 'yolov8s.pt', class_ids, run_dir)
            st.image(output_path)

    # --- Display Object Counts ---
    st.subheader("Detected Object Counts")
    for obj, count in object_counts.items():
        st.markdown(f"""
            <div class="count-card">
                <h4>{obj.title()}</h4>
                <p>{count}</p>
            </div>
        """, unsafe_allow_html=True)
