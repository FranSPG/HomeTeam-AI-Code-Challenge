import logging
import time
from urllib.error import URLError
from typing import List

import requests
from ultralytics import YOLO

MAX_RETRIES = 10
RETRY_DELAY = 5
TRITON_URL = 'triton'  # Change to 'localhost' if running locally


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("yolo-inference")

class YOLOModelSingleton:
    """
    Singleton class to ensure only one instance of the YOLO model is loaded.
    """
    _instance: YOLO = None

    @classmethod
    def get_instance(cls) -> YOLO:
        if cls._instance is None:
            logger.info("Loading YOLO model")
            cls._instance = YOLO(f"http://{TRITON_URL}:8000/yolo", task="detect")
            logger.info("Model loaded successfully")
        return cls._instance



def wait_for_triton_server() -> None:
    """
    Waits for the Triton inference server to become ready, retrying multiple times.

    Raises:
        ConnectionError: If the server is unreachable after max retries.
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"http://{TRITON_URL}:8000/v2/health/ready")
            if response.status_code == 200:
                logger.info("Connected to Triton server successfully")
                return
        except (ConnectionError, URLError):
            logger.info(f"Waiting for Triton server (attempt {attempt + 1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)

    raise ConnectionError("Failed to connect to Triton server after multiple attempts")




def detect_motion(frames: List, frame_idx: int) -> List:
    """
    Detect motion in the given frames using YOLO object detection.

    Args:
        frames (List): List of video frames.
        frame_idx (int): Index of the current frame.

    Returns:
        List: List of bounding boxes for detected motion regions.
    """
    if frame_idx < 1 or frame_idx >= len(frames):
        return []

    detections: List = []
    model = YOLOModelSingleton.get_instance()


    for frame in frames:
        try:
            logger.info("Running inference on image")
            results = model(frame)
            detections.append(results)
            logger.info("Inference completed")
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")

    return detections
