import base64
import cv2

from io import BytesIO
from PIL import Image

class WebcamService:
    def __init__(self):
        self.camera_index = self.find_webcam_index()

    def find_webcam_index(self):
        """Find the index of the webcam."""
        for index in range(5):
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    return index
        return None

    def capture_image_from_webcam(self):
        """Captures an image from the webcam."""
        cap = cv2.VideoCapture(self.camera_index)

        if not cap.isOpened():
            raise Exception("Could not open video device")

        for i in range(5):
            cap.read()

        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise Exception("Could not read frame from webcam")

        return self.convert_image_to_base64(frame)
    
    def convert_image_to_base64(self, image):
        """Convert a NumPy array image to a base64 string."""
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
