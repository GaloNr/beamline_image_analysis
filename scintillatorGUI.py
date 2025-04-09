# ScintillatorGUI.py
import time
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from scintillatorAnalyze import ScintillatorAnalyzer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np


class ScintillatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scintillator Analyzer")
        self.analyzer = None
        self.results = []

        # Create main frame
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill='both')

        # Create file path display
        self.file_path = tk.StringVar()
        self.path_entry = tk.Entry(self.main_frame, textvariable=self.file_path, width=50)
        self.path_entry.pack(fill='x', pady=(0, 5))

        # Create upload button
        self.upload_button = tk.Button(
            self.main_frame,
            text="Select Video File",
            command=self.upload_file
        )
        self.upload_button.pack(fill='x')

        # Create status label
        self.status_label = tk.Label(self.main_frame, text="")
        self.status_label.pack(fill='x', pady=(5, 0))

        # Create figure for plotting
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.timing_label = tk.Label(self.main_frame, text="")
        self.timing_label.pack()

    def upload_file(self):
        # Open file dialog
        file_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov")]
        )

        if file_path:
            self.file_path.set(file_path)
            self.status_label.config(text="File selected successfully", fg="green")

            try:
                start = float(time.time())
                # Create analyzer instance
                self.analyzer = ScintillatorAnalyzer()
                peaks = self.analyzer.process_video_with_multiple_peaks(file_path)

                # Assign arbitrary voltage (nth flash = nV)
                for i, peak in enumerate(peaks):
                    self.results.append({
                        'video_path': Path(file_path).name,
                        'voltage': i + 1,  # nth flash = nV
                        'peak_intensity': peak['intensity'],
                        'peak_timestamp': peak['timestamp']
                    })

                # Update plot
                self.update_plot()

                end = float(time.time())
                self.timing_label.config(
                    text=f"{str(round(end-start, 2))} seconds taken"
                )

                # Save to CSV
                self.save_to_csv()

                self.status_label.config(
                    text="Analysis completed successfully",
                    fg="green"
                )
            except Exception as e:
                self.status_label.config(
                    text=f"Error: {str(e)}",
                    fg="red"
                )

    def update_plot(self):
        self.ax.clear()
        if self.results:
            voltages = [r['voltage'] for r in self.results]
            intensities = [r['peak_intensity'] for r in self.results]

            self.ax.plot(voltages, intensities, marker='o', linestyle='-', linewidth=2)
            self.ax.set_xlabel('Flash Number (V)')
            self.ax.set_ylabel('Peak Intensity')
            self.ax.set_title('Scintillator Peak Intensities vs Flash Number')
            self.ax.grid(True)

            self.canvas.draw()

    def save_to_csv(self):
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_csv('analysis_results.csv', index=False)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ScintillatorGUI()
    app.run()