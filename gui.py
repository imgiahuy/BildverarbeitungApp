from tkinter import *
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk
from final_0 import open_image, kantenerkennung, increase_brightness, kreiserkennung, decrease_brightness

current_image = None #numpy array
display_img = None #image tkinter can display
history_stack = []

root = Tk()

root.title("Bildverarbeitung")
root.minsize(600, 600)
root.configure(background="#fff")

#Vorschau bereich
img_label = Label(root, bg="lightgray", bd=5, relief=SUNKEN)
examplePic = ImageTk.PhotoImage(Image.open("example.png"))
img_label.config(image=examplePic)
img_label.grid(column=0, row=0)
minRadius = 1
maxRadius = 100

# Function
def open_file():
    history_stack.clear()
    global current_image
    global display_img
    filename = filedialog.askopenfilename()
    if filename:
        current_image = open_image(filename)
        current_image_RGB = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
        display_img = Image.fromarray(current_image_RGB)
        image_tk = ImageTk.PhotoImage(display_img)
        img_label.configure(image=image_tk)
        img_label.image = image_tk

def process_kanten():
    global current_image
    global display_img
    if current_image is not None:
        history_stack.append(current_image)
        current_image = kantenerkennung(current_image)
        display_img = Image.fromarray(current_image)
        image_tk = ImageTk.PhotoImage(display_img)
        img_label.configure(image=image_tk)
        img_label.image = image_tk
    else :
        messagebox.showerror("Error", "Ungueltiges Bild")

def process_brightness():
    global current_image
    global display_img
    if current_image is not None:
        history_stack.append(current_image.copy())
        current_image = increase_brightness(current_image)
        current_image_RGB = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
        display_img = Image.fromarray(current_image_RGB)
        image_tk = ImageTk.PhotoImage(display_img)
        img_label.configure(image=image_tk)
        img_label.image = image_tk
    else:
        messagebox.showerror("Error", "Ungueltiges Bild")

def process_circle():
    global current_image
    global display_img
    if current_image is not None:
        history_stack.append(current_image.copy())
        process_img = kreiserkennung(current_image, minRadius, maxRadius)
        process_img_RGB = cv2.cvtColor(process_img, cv2.COLOR_BGR2RGB)
        display_img = Image.fromarray(process_img_RGB)
        image_tk = ImageTk.PhotoImage(display_img)
        img_label.configure(image=image_tk)
        img_label.image = image_tk
    else:
        messagebox.showerror("Error", "Ungueltiges Bild")

def save_file():
    global display_img
    if display_img is not None:  # Ensure there is an image to save
        types = [("JPEG Image", "*.jpg"), ("PNG Image", "*.png"), ("All files", "*.*")]
        filepath = filedialog.asksaveasfilename(filetypes=types)
        if filepath:
            display_img.save(filepath)  # Use the save method of the PIL.Image object
            print(f"Image saved to {filepath}")
    else:
        messagebox.showerror("Error", "Ungueltige Name")

def process_brightness_reduzieren():
    global current_image
    global display_img
    if current_image is not None:
        history_stack.append(current_image.copy())
        current_image = decrease_brightness(current_image)
        current_image_RGB = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
        display_img = Image.fromarray(current_image_RGB)
        image_tk = ImageTk.PhotoImage(display_img)
        img_label.configure(image=image_tk)
        img_label.image = image_tk
    else:
        messagebox.showerror("Error", "Ungueltiges Bild")


def undo():
    global current_image
    global display_img
    if history_stack:
        # Restore the last image from the stack
        current_image = history_stack.pop()
        current_image_RGB = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
        display_img = Image.fromarray(current_image_RGB)
        image_tk = ImageTk.PhotoImage(display_img)
        img_label.configure(image=image_tk)
        img_label.image = image_tk
    else:
        messagebox.showerror("Error", "Undo unmoeglich")

def submit():
    global minRadius, maxRadius
    if (entry_min.get()) and (entry_max.get()):
        minRadius = int(entry_min.get())
        maxRadius = int(entry_max.get())

def delete():
    global minRadius, maxRadius
    entry_min.delete(0, END)
    entry_max.delete(0, END)
    minRadius = 1
    maxRadius = 100

# Button
button = Frame(root)
Button(button, text="Bild Laden", command=open_file, width=15).grid(column=0, row=0)
Button(button, text='Speichern', command=save_file, width=15).grid(column=1, row=0)
Button(button, text="Helligkeit erhöhen", command=process_brightness, width=15).grid(column=2, row=0)
Button(button, text="Kreiserkennung", command=process_circle, width=15).grid(column=3, row=0)
Button(button, text="Kantenerkennung", command=process_kanten, width=15).grid(column=0, row=1)
Button(button, text="Helligkeit reduzieren", command=process_brightness_reduzieren, width=15).grid(column=1, row=1)
Button(button,text="Undo", command=undo, width=15).grid(column=2, row=1)
Button(button, text = "Exit", command=exit, width=15).grid(column=3, row=1)
button.grid(column=0, row=1)

# Label
label = Frame(root)
Label(label, text="Min Radius").grid(column=0, row=0)
entry_min = Entry(label)
entry_min.grid(column=1, row=0)

Label(label, text="Max Radius").grid(column=0, row=1)
entry_max = Entry(label)
entry_max.grid(column=1, row=1)

Button(label, text="Submit", command=submit, width=15).grid(column=2, row=0)

Button(label, text="Delete", command=delete, width=15).grid(column=2, row=1)

label.grid(column=0, row=2)


root.resizable(width=0, height=0)
root.mainloop()
