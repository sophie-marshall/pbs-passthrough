import cv2
from utils.video_loader import VideoLoader
from utils.video_feature_extractor import FeatureExtractor
from utils.video_processor import VideoProcessor

def convert_image_to_bytea(image_array):
    """
    Function to convert an image represented as an array into bytes 

    Args:
        image_array (array): Array representation of an image 
    
    Returns:
        image bytes (bytes): Bytes representation f the image 
    """
    success, encoding = cv2.imencode(".jpg", image_array)
    if not success:
        return None
    return encoding.tobytes()


def video_procesisng_pipeline(mp4_filepath, load_previous):
    """
    Function to wrap scene detection preparation steps

    Args:
        mp4_filepath (str): Filepath pointing to the video you'd like to process
        load_previous (bool): Shhould the video procesor keep track of the previous frame

    Returns:
        df (DataFrame): padnas DataFrame with columns for edges, pixel_diffs, and bhattacharyya_distance
    """

    # instantiate video loader and feature extractor 
    loader = VideoLoader(mp4_filepath)
    extractor = FeatureExtractor()

    # initialize pipeline 
    procesor = VideoProcessor(video_loader=loader, feature_extractor=extractor)

    # process the video
    loader.__enter__()
    try:
        df = procesor.extract_features(load_previous)
    finally:
        loader.__exit__(None, None, None)

    # return the resulting df
    return df 

def get_frame_rate(mp4_filepath):
    """
    Function to retrieve frames per second

    Args:
        mp4_filepath (str): Filepath pointing to video to analyze

    Returns:
        frame_rate (float): Frame rate / frames per second
    """
    cap = cv2.VideoCapture(mp4_filepath)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return frame_rate