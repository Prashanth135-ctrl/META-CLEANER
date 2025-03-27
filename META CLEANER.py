import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def remove_image_metadata(input_path):
    """Removes metadata from an image."""
    try:
        img = Image.open(input_path)
        img_data = list(img.getdata())  # Extract pixel data

        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(img_data)  # Save without metadata
        
        output_path = "cleaned_" + os.path.basename(input_path)
        clean_img.save(output_path, format=img.format, exif=b"")
        
        messagebox.showinfo("Success", f"Metadata removed! Saved as: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clean image: {str(e)}")

def remove_video_metadata(input_path):
    """Removes metadata from a video using FFmpeg."""
    try:
        output_path = "cleaned_" + os.path.basename(input_path)
        
        (
            ffmpeg
            .input(input_path)
            .output(output_path, map_metadata=-1, codec="copy")
            .run(overwrite_output=True, quiet=True)
        )
        
        messagebox.showinfo("Success", f"Metadata removed! Saved as: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clean video: {str(e)}")

def select_file():
    """Opens file dialog to select an image or video."""
    file_path = filedialog.askopenfilename(title="Select an Image or Video",
                                           filetypes=[("Images", "*.jpg;*.jpeg;*.png"),
                                                      ("Videos", "*.mp4;*.mov;*.avi;*.mkv"),
                                                      ("All Files", "*.*")])
    if file_path:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in [".jpg", ".jpeg", ".png"]:
            remove_image_metadata(file_path)
        elif file_ext in [".mp4", ".mov", ".avi", ".mkv"]:
            remove_video_metadata(file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format!")

# GUI Setup
root = tk.Tk()
root.title("Meta Cleaner")
root.geometry("400x200")

label = tk.Label(root, text="Select a file to remove metadata", font=("Arial", 12))
label.pack(pady=20)

select_button = tk.Button(root, text="Choose File", command=select_file, font=("Arial", 12), bg="blue", fg="white")
select_button.pack(pady=10)

root.mainloop()
