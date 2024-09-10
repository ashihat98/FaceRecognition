import cv2
from mtcnn import MTCNN

def test_face_detection_on_image(image_path):
    # Initialize the MTCNN detector
    detector = MTCNN()

    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print("Error loading image.")
        return

    # Detect faces in the image
    faces = detector.detect_faces(img)

    # Draw rectangles around detected faces
    for face in faces:
        x, y, width, height = face['box']
        cv2.rectangle(img, (x, y), (x + width, y + height), (255, 0, 0), 2)

    # Display the image with rectangles
    cv2.imshow('Image with Face Detection', img)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

# Test the function with an image path
test_face_detection_on_image('/Users/abanoubshihat/Downloads/IMG_0780 Large.jpeg')
