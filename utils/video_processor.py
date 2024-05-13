from tqdm import tqdm 
import numpy as np 

class VideoProcessor:
    def __init__(self, video_loader, feature_extractor):
        self.video_loader = video_loader
        self.feature_extractor = feature_extractor
        self.edges = []
        self.pixel_diffs = []
        self.bhat_distances = []

    def extract_features(self, load_previous=True):
        """
        Extract features from an MP4 file using provided feature extractor 

        Args:
            load_previous (bool): Do we want to track and load previous frames 

        Returns:
            DataFrame with frame_number, timestamp(ms), and extracted features
        """
        # create df with frame number and timestamp 
        df = self.video_loader.create_frame_and_timestamp_df()

        # get total number of frames
        total_frames = len(df)

        # lazy load videos and extract features 
        with self.video_loader as loader:
            progress_bar = tqdm(total=total_frames, desc="Extracting Features", unit=" frames")
            for frames in loader.yield_frames(load_previous=load_previous):
                try:
                    if load_previous:
                        prev_frame, curr_frame = frames
                        if prev_frame is not None:
                            try:
                                # get features 
                                edge = self.feature_extractor.compute_edges(curr_frame)
                                pixel_diff = self.feature_extractor.compute_pixel_diff(prev_frame, curr_frame)
                                bhat_distance = self.feature_extractor.compute_bhattacharyya(prev_frame, curr_frame)
                                # append features to data list 
                                self.edges.append(edge)
                                self.pixel_diffs.append(pixel_diff)
                                self.bhat_distances.append(bhat_distance)
                            except Exception as e:
                                self.edges.append(edge)
                                self.pixel_diffs.append(np.nan)
                                self.bhat_distances.append(np.nan)
                        else:
                            self.edges.append(edge)
                            self.pixel_diffs.append(np.nan)
                            self.bhat_distances.append(np.nan)

                    else:
                        curr_frame = frames
                        # get edges 
                        edge = self.feature_extractor.compute_edges(curr_frame)
                        # append featuers 
                        self.edges.append(edge)
                except Exception as e:
                    print(f"Error extracting features: {str(e)}")
                finally:
                    progress_bar.update(1)
            
        progress_bar.close()
        
        df["edges"] = self.edges
        df["pixel_diffs"] = self.pixel_diffs
        df["bhattacharyya_distance"] = self.bhat_distances

        return df 