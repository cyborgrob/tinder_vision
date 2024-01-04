import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import shutil


class ImageLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling App")

        # Variables
        self.image_folder = ""
        self.image_list = []
        self.current_image_index = 0

        # Create GUI elements
        self.label = tk.Label(root, text="Label the image:")
        self.label.pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.yes_button = tk.Button(root, text="Yes (1)", command=lambda: self.label_image(1))
        self.yes_button.pack(side=tk.LEFT, padx=10)

        self.no_button = tk.Button(root, text="No (0)", command=lambda: self.label_image(0))
        self.no_button.pack(side=tk.RIGHT, padx=10)

        self.next_button = tk.Button(root, text="Next Image", command=self.load_next_image)
        self.next_button.pack(pady=20)

        self.load_folder_button = tk.Button(root, text="Load Image Folder", command=self.load_image_folder)
        self.load_folder_button.pack(pady=10)

        # Bind keyboard events
        root.bind("<Key-1>", lambda event: self.label_image(1))  # Press '1' for 'Yes'
        root.bind("<Key-0>", lambda event: self.label_image(0))  # Press '0' for 'No'
        root.bind("<Right>", lambda event: self.load_next_image())  # Press 'Right Arrow' for 'Next Image'

    # Runs when you click 'Load Image Folder'
    def load_image_folder(self):
        # Asks which folder you want
        self.image_folder = filedialog.askdirectory()
        # Creates image list of items in folder
        self.image_list = [f for f in os.listdir(self.image_folder)]
        self.current_image_index = 0
        self.load_image()

    # Loads image into tkinter window
    def load_image(self):
        if self.image_list:
            image_path = os.path.join(self.image_folder, self.image_list[self.current_image_index])
            image = Image.open(image_path)
            image = image.resize((700, 700))
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.label.config(text=f"Label the image: {self.image_list[self.current_image_index]}")

    def label_image(self, label):
        image_name = self.image_list[self.current_image_index]
        # Create source path before changing image_name
        source_path = os.path.join(self.image_folder, image_name)

        # If image_name starts with a non-alpha char like '-', replace it with a '0' (causes issues in csv file)
        if not image_name[0].isalnum():
            image_name = '0' + image_name[1:]

        # Copy image to destination folder
        destination_folder = 'PATH TO YOUR FOLDER'
        destination_path = os.path.join(destination_folder, image_name)

        # Copy the image
        shutil.copy(source_path, destination_path)

        # Write filename and label to csv file
        label_file_path = 'PATH TO YOUR CSV FILE'  # Filepath of the labels csv file

        with open(label_file_path, "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([image_name, label])

        self.load_next_image()

    def load_next_image(self):
        self.current_image_index += 1
        if self.current_image_index < len(self.image_list):
            self.load_image()
        else:
            self.label.config(text="No more images in the folder.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLabelingApp(root)
    root.mainloop()
