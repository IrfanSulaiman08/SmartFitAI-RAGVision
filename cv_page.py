import streamlit as st
import cv2
from pose.pose_extract import get_landmarks
from model.predict import predict_exercise

def cv_page():
    st.title("🏋️ SmartFit AI – Camera")

    start = st.checkbox("Start Camera")

    if start:
        cap = cv2.VideoCapture(0)

        sequence = []
        exercise = "Collecting..."

        frame_box = st.empty()
        result_box = st.empty()

        while start:
            ret, frame = cap.read()
            if not ret:
                break

            # Get landmarks
            landmarks = get_landmarks(frame)

            if landmarks:
                sequence.append(landmarks)

                # Keep only last 30 frames
                if len(sequence) > 30:
                    sequence.pop(0)

                # Predict when 30 frames available
                if len(sequence) == 30:
                    exercise = predict_exercise(sequence)
                else:
                    exercise = "Collecting..."

            else:
                exercise = "No Pose Detected"

            # Show result
            result_box.info(f"Exercise: {exercise}")

            # Show frame
            frame_box.image(frame, channels="BGR")

        cap.release()

    # Navigation button
    if st.button("🤖 Go to AI Advisor"):
        st.session_state.page = "rag"

