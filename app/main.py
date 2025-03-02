import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse

from app.frame_processor import get_frames
from app.motion_detector import detect_motion
from app.visualizer import visualize_results

app = FastAPI()


@app.post("/process_video/")
async def process_video(file: UploadFile = File(...), fps: int = Form(...), resize_dim: str = Form(...)) -> FileResponse:
    """
    Processes an uploaded video file by extracting frames, detecting motion,
    and visualizing the results into a processed video.

    Args:
        file (UploadFile): The uploaded video file.
        fps (int): Frames per second for the output video.
        resize_dim (str): Dimensions as a comma-separated string "width,height".

    Returns:
        FileResponse: The processed video file.
    """
    # Create temporary files for input and output videos
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as input_temp:
        input_path = input_temp.name
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    width, height = map(int, resize_dim.split(","))
    resize_dim = (width, height)

    output_path = f"processed_{Path(file.filename).name}"

    # Extract frames from the video
    frame_results, original_frames = get_frames(video_path=input_path, target_fps=fps,
                                                resize_dim=resize_dim)

    # Perform motion detection on extracted frames
    motion_results = detect_motion(frame_results, frame_idx=1)


    # Visualize results and save processed video
    visualize_results(
        frames=frame_results,
        motion_results=motion_results,
        output_video_path=output_path,
        fps=original_frames
    )

    # Return processed video as response
    return FileResponse(output_path, media_type="video/mp4", filename=Path(output_path).name)
