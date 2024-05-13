import cv2 
from tqdm import tqdm 
import pandas as pd 


class VideoLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.cap = None

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.filepath)
        if not self.cap.isOpened():
            raise ValueError("Error opening video file")
        return self 
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.cap is not None:
            self.cap.release()

    def create_frame_and_timestamp_df(self):
        if self.cap is None:
            raise ValueError("VideoCapture object not initialized. Call 'enter' first")
        
        frame_numbers = []
        timestamps = []

        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar = tqdm(total=total_frames, desc="Processing MP4 Frames", unit="frames")

        while True:
            has_next_frame, _ = self.cap.read()
            if not has_next_frame:
                break

            frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            timestamp = self.cap.get(cv2.CAP_PROP_POS_MSEC)

            frame_numbers.append(frame_number)
            timestamps.append(timestamp)

            progress_bar.update(1)

        progress_bar.close()
        
        df = pd.DataFrame({
            "frame_number": frame_numbers, 
            "timestamp": timestamps
        })

        return df

    def yield_frames(self, load_previous=False):
        if self.cap is None:
            raise ValueError("VideoCapture object not initialized. Call 'enter' first")
        
        prev_frame = None
        while True:
            has_next_frame, curr_frame = self.cap.read()
            if load_previous:
                yield prev_frame, curr_frame
                prev_frame = curr_frame
            else:
                yield curr_frame 
            if not has_next_frame:
                break