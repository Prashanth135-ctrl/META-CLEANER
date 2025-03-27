import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import piexif

def remove_metadata(input_path):
    try:
        image = Image.open(input_path)

        # Remove metadata
        exif_data = piexif.load(image.info.get("exif", b""))
        exif_data["Exif"] = {}

        output_path = "cleaned_" + os.path.basename(input_path)
        image.save(output_path, exif=piexif.dump(exif_data))

        messagebox.showinfo("Success", f"✅ Metadata removed!\nSaved as: {output_path}")
        return output_path

    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to remove metadata: {e}")
        return None

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img = ImageTk.PhotoImage(img)
        
        img_label.config(image=img)
        img_label.image = img

        global selected_file
        selected_file = file_path

def clean_image():
    if not selected_file:
        messagebox.showwarning("Warning", "⚠️ Please select an image first!")
        return

    cleaned_path = remove_metadata(selected_file)

    if cleaned_path:
        img = Image.open(cleaned_path)
        img.thumbnail((300, 300))
        img = ImageTk.PhotoImage(img)
        
        cleaned_img_label.config(image=img)
        cleaned_img_label.image = img

# Create GUI window
root = tk.Tk()
root.title("Instagram Metadata Cleaner")
root.geometry("500x500")

# Labels
tk.Label(root, text="Original Image:").pack()
img_label = tk.Label(root)
img_label.pack()

tk.Label(root, text="Cleaned Image:").pack()
cleaned_img_label = tk.Label(root)
cleaned_img_label.pack()

# Buttons
selected_file = None
tk.Button(root, text="Select Image", command=select_image).pack(pady=10)
tk.Button(root, text="Remove Metadata", command=clean_image).pack(pady=10)

# Run the application
root.mainloop()
