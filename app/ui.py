import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk  # Import ttk for the progress bar
from PIL import Image, ImageTk
import threading  # Import threading for background tasks
import time  # For tracking elapsed time
from . import video_helpers  # Import video_helpers
import re
from moviepy import (VideoFileClip, concatenate_videoclips)
import random
import subprocess
import platform
import traceback

class VideoUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Video Tool")
        self.root.geometry("600x800")
        self.selected_file = None

        # Define a bigger font size for everything
        self.default_font = ('Arial', 14)

        self.create_widgets()

    def create_widgets(self):
        # Load the PNG image

        # Get the absolute path to the project root
        project_root = os.path.dirname(os.path.abspath(__file__))  # Get the directory of ui.py
        assets_folder = os.path.join(project_root, '..', 'assets')  # Go up one level and into 'assets'

        # Now construct the full path to the logo.png
        logo_path = os.path.join(assets_folder, 'logo.png')
        self.image = Image.open(logo_path)  # Corrected path
        self.image = self.image.resize((150, 150))  # Resize the image to fit the UI
        self.image_tk = ImageTk.PhotoImage(self.image)

        # Label to show the image (on the left side)
        self.image_label = tk.Label(self.root, image=self.image_tk)
        self.image_label.pack(side="left", padx=10)

        # Button to select a video file
        self.select_button = tk.Button(self.root, text="Select Video File", font=self.default_font,
                                       command=self.browse_file)
        self.select_button.pack(pady=10)

        # Label to show selected file
        self.file_label = tk.Label(self.root, text="No file selected", font=self.default_font, wraplength=350)
        self.file_label.pack(pady=20)

        # Dropdown for font color selection
        self.text_color_label = tk.Label(self.root, text="Select Number Font Color:", font=self.default_font)
        self.text_color_label.pack(pady=5)

        self.text_color_var = tk.StringVar(self.root)
        self.text_color_var.set("Red")  # default value

        self.color_options = ["Red", "White", "Blue", "Pink", "Yellow", "Orange", "Green", "Purple", "Random"]
        self.text_color_menu = tk.OptionMenu(self.root, self.text_color_var, *self.color_options)
        self.text_color_menu.config(font=self.default_font)
        self.text_color_menu.pack(pady=5)

        # Label for Starting Number
        self.starting_number_label = tk.Label(self.root, text="Enter the Starting Number:", font=self.default_font)
        self.starting_number_label.pack(pady=5)

        # Entry for Starting Number
        validate_starting_number_command = self.root.register(self.validate_starting_number)
        self.starting_number_entry = tk.Entry(self.root, font=self.default_font, validate="key",
                                              validatecommand=(validate_starting_number_command, '%P'))
        self.starting_number_entry.pack(pady=10)

        self.starting_number_entry.insert(0, "1")  # Default value for starting number

        # Label for number of iterations input
        self.number_label = tk.Label(self.root, text="Enter the number of iterations (1-99999):",
                                     font=self.default_font)
        self.number_label.pack(pady=5)

        # Entry for user to input a number
        validate_command = self.root.register(self.only_digits)
        self.number_entry = tk.Entry(self.root, font=self.default_font, validate="key",
                                     validatecommand=(validate_command, '%P'))
        self.number_entry.pack(pady=10)

        self.number_entry.insert(0, "72")  # Default value for number of iterations

        # Label for output file name input
        self.output_filename_label = tk.Label(self.root, text="Enter the output file name:", font=self.default_font)
        self.output_filename_label.pack(pady=5)

        # Entry for output file name
        output_name_validate_command = self.root.register(self.validate_output_filename)
        self.output_filename_entry = tk.Entry(self.root, font=self.default_font, validate="key",
                                              validatecommand=(output_name_validate_command, '%P'))
        self.output_filename_entry.pack(pady=10)

        self.output_filename_entry.insert(0, "output_video.mp4")  # Default value for output file name

        # Button to start the task
        self.validate_button = tk.Button(self.root, text="Submit Number", font=self.default_font,
                                         command=self.start_task)
        self.validate_button.pack(pady=5)

        # Progress Bar (hidden initially)
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=10)
        self.progress['value'] = 0
        self.progress["maximum"] = 100  # Max value for progress (set to 100 for percentage)

        # Label to display progress percentage
        self.progress_percentage_label = tk.Label(self.root, text="0%", font=self.default_font)
        self.progress_percentage_label.pack(pady=5)

        # Label to show elapsed time
        self.time_label = tk.Label(self.root, text="Elapsed Time: 00:00:00", font=self.default_font)
        self.time_label.pack(pady=10)

        # Setup drag and drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

        self.show_folder_button = tk.Button(
            self.root,
            text="Show Video Location Folder",
            font=self.default_font,
            command=self.open_output_folder
        )

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv")])
        if file_path:
            self.set_selected_file(file_path)

    def set_selected_file(self, file_path):
        self.selected_file = file_path
        self.file_label.config(text=f"Selected: {file_path}")

    def open_output_folder(self):

        full_path = os.path.abspath(self.final_output_path)
        print(full_path)
        print(self.final_output_path)
        if platform.system() == "Windows":
            subprocess.run(['explorer', '/select,', full_path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(['open', '-R', full_path])
        else:
            print("Unsupported OS")

    def validate_number(self):
        value = self.number_entry.get()
        try:
            num = int(value)
            if 1 <= num <= 99999:
                messagebox.showinfo("Valid Number", f"Accepted number: {num}")
            else:
                messagebox.showerror("Invalid Number", "Number must be between 1 and 99999.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

    def only_digits(self, new_value):
        if new_value == "":
            self.number_entry.config(bg="white")
            return True

        if new_value.isdigit():
            num = int(new_value)
            if 1 <= num <= 99999:
                self.number_entry.config(bg="white")
            else:
                self.number_entry.config(bg="#ffcccc")
            return True
        else:
            return False

    def validate_starting_number(self, new_value):
        # Allow empty input (before the user starts typing)
        if new_value == "":
            return True

        # Check if the value is a whole number
        if new_value.isdigit():
            return True
        else:
            return False

    def validate_output_filename(self, new_value):
        # Check if the new value contains only valid characters (alphanumeric, -, ., and _)
        if new_value == "":
            return True  # Allow empty input (before the user starts typing)

        # Regex for alphanumeric characters, hyphens, periods, and underscores
        pattern = r'^[a-zA-Z0-9.-_]*$'
        if re.match(pattern, new_value):
            return True  # Valid input
        else:
            self.output_filename_entry.config(bg="#ffcccc")  # Highlight invalid input
            return False  # Reject invalid input

    def on_drop(self, event):
        file_path = event.data.strip('{}')
        if file_path:
            self.set_selected_file(file_path)

    def start_task(self):
        """Start the long-running task in a separate thread"""
        # Disable the submit button immediately when the task starts
        self.validate_button.config(state="disabled")

        # Reset progress bar
        self.progress['value'] = 0
        self.progress.pack()  # Make sure it's visible

        # Record the start time
        self.start_time = time.time()

        # Start the task in a background thread to keep the UI responsive
        threading.Thread(target=self.run_task).start()

    def run_task(self):
        """Run the three-step task: Set up, Iterations, Clean up"""
        try:
            # Set up (done once)
            input_file_path = self.selected_file
            file_directory = os.path.dirname(input_file_path)
            current_dir = os.path.dirname(os.path.abspath(__file__))

            self.final_output_path = os.path.join(file_directory, self.output_filename_entry.get())
            temp_folder = os.path.join(current_dir,'tmp')

            os.makedirs(temp_folder, exist_ok=True)

            initial_clip = (
                VideoFileClip(input_file_path)
            )
            files = [initial_clip]
            stub_files_list = []
            files_cap_limit = 150

            starting_number = int(self.starting_number_entry.get()) if self.starting_number_entry.get() else 1
            version_number = starting_number - 1

            # Get the number from the text box (this is the number of iterations)
            max_iterations = int(self.number_entry.get())

            # Set the maximum value of the progress bar
            self.progress["maximum"] = max_iterations


            # Iterations (done multiple times)
            for i in range(max_iterations):
                version_number += 1
                temp_output_file = os.path.join(temp_folder, f"ex_{i}.mp4")

                # Call the helper function for each iteration
                sped_up_clip_file = video_helpers.double_and_concat(initial_clip,
                                                                    temp_output_file)

                sped_up_clip = (
                    VideoFileClip(sped_up_clip_file)
                )
                self.text_color = self.text_color_var.get()

                if self.text_color.lower() == 'random':
                    valid_colors = [c for c in self.color_options if c.lower() != "random"]
                    self.text_color = random.choice(valid_colors)
                clip_with_number = video_helpers.put_text_on_video(sped_up_clip,
                                                                   text_to_write=f"{version_number}",
                                                                   font_size=150,
                                                                   color=self.text_color)
                if len(files) == files_cap_limit:
                    print(f"Hit files cap limit on loop: {i}")
                    stub_clip = concatenate_videoclips(files)
                    mini_stub_path = os.path.join(temp_folder, f"stub_{i}.mp4")
                    stub_clip.write_videofile(mini_stub_path)
                    stub_clip.close()
                    while files:
                        mini = files.pop()

                        mini.close()

                    read_stub_clip = (
                        VideoFileClip(mini_stub_path)
                    )
                    stub_files_list.append(read_stub_clip)

                files.append(clip_with_number)

                initial_clip = clip_with_number

                # Update progress bar value
                self.progress['value'] = i + 1

                # Update the elapsed time every second
                self.update_elapsed_time()
                self.update_progress(i, max_iterations)

                # Force UI to update progress bar
                self.root.update_idletasks()

            final_clip = concatenate_videoclips(stub_files_list + files)

            final_clip.write_videofile(self.final_output_path)
            final_clip.close()
            # Task complete, update the progress bar
            self.progress['value'] = max_iterations
            self.validate_button.config(state="normal")
            self.show_folder_button.pack(pady=10)
            messagebox.showinfo("Task Complete", "Speed video has been created!")

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"{e}")
            tb = traceback.extract_tb(sys.exc_info()[2])
            for filename, lineno, func, text in tb:
                print(f"Error in {filename}, line {lineno}, in {func}")
                print(f"    {text}")

    def update_elapsed_time(self):
        """Update the elapsed time label"""
        elapsed_seconds = int(time.time() - self.start_time)
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        self.time_label.config(text=f"Elapsed Time: {hours:02}:{minutes:02}:{seconds:02}")

    def update_progress(self, current_value, max_value):
        # Update progress bar value
        self.progress['value'] = current_value

        # Calculate the percentage and update the label
        percentage = (current_value / max_value) * 100
        self.progress_percentage_label.config(text=f"{int(percentage)}%")

    def run(self):
        self.root.mainloop()
