import cv2
import numpy as np 

class FeatureExtractor:
    def __init__(self):
        pass

    def compute_edges(self, curr_frame):
        # compute edges using Canny algorithm 
        edges = cv2.Canny(curr_frame, 100, 200)
        # sum non-white (representing edges) pixels 
        n_edges = np.count_nonzero(edges)
        return n_edges
    
    def compute_pixel_diff(self, prev_frame, curr_frame):
        # grayscale the frames
        prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        # find ab pixel diff 
        abs_pixel_diff = cv2.absdiff(curr_frame_gray, prev_frame_gray)
        # create binary image using threshold 
        _, thresh = cv2.threshold(abs_pixel_diff, 30, 255, cv2.THRESH_BINARY)
        # count non-zero (white) pixels 
        pixel_diff = np.count_nonzero(thresh)
        return pixel_diff
    
    def compute_bhattacharyya(self, prev_frame, curr_frame):
        # convert frames to grayscale
        prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        # compute histograms 
        prev_hist = cv2.calcHist([prev_frame_gray], [0], None, [256], [0, 256])
        curr_hist = cv2.calcHist([curr_frame_gray], [0], None, [256], [0, 256])
        # normlaize histograms
        cv2.normalize(prev_hist, prev_hist, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(curr_hist, curr_hist, 0, 255, cv2.NORM_MINMAX)
        # compute Bhattacharyya distance
        distance = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_BHATTACHARYYA)
        return distance