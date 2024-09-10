import cv2
import os

def process_video(filepath):
    try:
        # Load pre-trained face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Read the input video
        cap = cv2.VideoCapture(filepath)

        if not cap.isOpened():
            print(f"Error: Unable to open video file {filepath}")
            return None

        # Get video properties: frame width, height, and frames per second
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        if width == 0 or height == 0 or fps == 0:
            print(f"Error: Unable to retrieve video properties from {filepath}")
            return None

        # Define the codec and create a VideoWriter object for the output video
        output_path = f'/tmp/processed_{os.path.basename(filepath)}'  # Save locally for upload later
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 videos
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))  # Specify frame size

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Draw rectangles around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Write the processed frame to the output video
            out.write(frame)

        cap.release()
        out.release()

        return output_path  # Return the local processed video path

    except Exception as e:
        print(f"Error processing the video: {e}")
        return None
