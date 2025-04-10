"""
Class ScintillatorAnalyzer for video frame sequential processing and conversion of
greyscale brightness into a line graph

Does not take parameters, global scope

Single threaded processing
"""
# ScintillatorAnalyzer.py
import numpy as np
import cv2
from pathlib import Path
from scipy.signal import find_peaks


class ScintillatorAnalyzer:
    def __init__(self):
        self.all_frames = []  # to plot every point

    def process_video_with_multiple_peaks(self, video_path):
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Initialize storage arrays
        intensities = []
        timestamps = []

        while True:
            ret, frame = cap.read()
            print(ret, frame)
            if not ret:
                break

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Calculate mean intensity
            curr_intensity = np.mean(gray)
            intensities.append(curr_intensity)
            timestamps.append(len(timestamps) / fps)

        cap.release()

        # Find peaks in intensity values
        peaks, _ = find_peaks(intensities, height=np.mean(intensities) + np.std(intensities) - 6, prominence=2)

        # Create peak data structure
        peak_data = []
        for peak_idx in peaks:
            peak_data.append({
                'intensity': intensities[peak_idx],
                'timestamp': timestamps[peak_idx]
            })

        # Store all frames for plotting
        self.all_frames = {
            'intensities': intensities,
            'timestamps': timestamps
        }

        return peak_data