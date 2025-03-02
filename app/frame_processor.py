from typing import List, Tuple, Any

import cv2
import numpy as np
from cv2 import Mat
from numpy import ndarray, dtype


def get_frames(video_path: str, target_fps: int = 5, resize_dim: Tuple[int, int] = (640, 480)) -> tuple[
    list[ndarray | Any], float]:
    """
    Extract frames from a video at a specified frame rate.

    Args:
        video_path (str): Path to the video file.
        target_fps (int): Target frames per second to extract.
        resize_dim (Tuple[int, int]): Dimensions to resize frames to (width, height).

    Returns:
        tuple[List[np.ndarray | Any], float]: List of extracted frames and the original video fps.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video file: {video_path}")

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(original_fps / target_fps))

    frames = []
    frame_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % frame_interval == 0:
            if resize_dim:
                frame = cv2.resize(frame, resize_dim, interpolation=cv2.INTER_AREA)
            frames.append(frame)

        frame_index += 1

    cap.release()
    return frames, original_fps