# ScintillatorAnalyzer.py
import numpy as np
import cv2
from pathlib import Path
from scipy.signal import find_peaks


class ScintillatorAnalyzer:
    def __init__(self):
        pass

    def process_video_with_multiple_peaks(self, video_path):
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Initialize storage
        intensities = []
        timestamps = []

        while True:
            ret, frame = cap.read()
            print(ret, frame)
            if not ret:
                break

            # Convert to grayscale and calculate intensity
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_intensity = np.mean(gray)

            intensities.append(avg_intensity)
            timestamps.append(len(intensities) / fps)

        cap.release()

        # Find all peaks using scipy's find_peaks
        peaks, _ = find_peaks(intensities, height=np.mean(intensities) + 2 * np.std(intensities))

        # Create list of peak data
        peak_data = []
        for peak_idx in peaks:
            peak_data.append({
                'intensity': intensities[peak_idx],
                'timestamp': timestamps[peak_idx]
            })

        return peak_data