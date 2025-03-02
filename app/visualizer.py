from typing import List

import cv2
import numpy as np
import supervision as sv


def visualize_results(frames: List[np.ndarray], motion_results: List, output_video_path: str, fps: float) -> None:
    """
    Create a visualization video of motion detection results.

    Args:
        frames (List[np.ndarray]): List of video frames.
        motion_results (List): List of motion detection results for each frame.
        output_video_path (str): Path to save the annotated video.
        fps (float): Frame rate of the output video.
    """
    if not frames:
        raise ValueError("No frames provided for visualization.")

    annotated_frames = []
    for frame, result in zip(frames, motion_results):
        detections = sv.Detections.from_ultralytics(result[0])
        annotator = sv.ColorAnnotator(opacity=0.3)
        annotated_frame = annotator.annotate(scene=frame.copy(), detections=detections)
        annotated_frames.append(annotated_frame)

    height, width, _ = annotated_frames[0].shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for frame in annotated_frames:
        video_writer.write(frame)

    video_writer.release()
