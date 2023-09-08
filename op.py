import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from colorthief import ColorThief
import matplotlib.pyplot as plt
import pandas as pd
import tempfile
import os

class ImageCropperApp:
    def __init__(self, root, callback):
        self.root = root
        self.root.title("Image Cropper")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        self.image = Image.open("bg.jpg")
        self.image = self.image.resize((screen_width, screen_height), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(root, cursor="cross", width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        self.cropping = False
        self.callback = callback
        self.temp_image = None
        self.color_box = None

        self.canvas.bind("<ButtonPress-1>", self.capture_box)
        self.canvas.bind("<Motion>", self.on_hover)

    def on_hover(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        color = self.get_color_at_point(x, y)

        if self.color_box:
            self.canvas.delete(self.color_box)

        color_box_size = 40
        self.color_box = self.canvas.create_rectangle(
            event.x - color_box_size // 2,
            event.y - color_box_size // 2,
            event.x + color_box_size // 2,
            event.y + color_box_size // 2,
            fill=color,
            outline=color,
        )

    def get_color_at_point(self, x, y):
        if self.image:
            pixel = self.image.getpixel((int(x), int(y)))
            return "#%02x%02x%02x" % pixel[:3]
        return ""

    def capture_box(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        half_box_size = 5 

        left = int(x - half_box_size)
        top = int(y - half_box_size)
        right = int(x + half_box_size)
        bottom = int(y + half_box_size)

        left = max(left, 0)
        top = max(top, 0)
        right = min(right, self.image.width)
        bottom = min(bottom, self.image.height)

        self.temp_image = self.image.crop((left, top, right, bottom))

        self.callback(self.temp_image)
        self.root.destroy()
        self.root.quit()


def get_color_name(cod):
    R, G, B = cod[0], cod[1], cod[2]
    min_diff = 1000
    for i in range(len(csv)):
        diff = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(
            B - int(csv.loc[i, "B"])
        )
        if diff <= min_diff:
            min_diff = diff
            cname = csv.loc[i, "color_name"]
    return cname

def Basic(cropped_img):
    if cropped_img is None:
        print("No valid cropped image to save and analyze.")
        return
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        cropped_img.save(temp_file, format="JPEG")
        temp_file_path = temp_file.name

    try:
        img = ColorThief(temp_file_path)  
        limit = int(input("Enter range of colors to extract info:"))
        palet = img.get_palette(color_count=20)
        hexcode = []
        rg = []
        nam = []

        def rgtohex(rgb):
            rg.append(rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

        for i in range(0, limit):
            hexcode.append(rgtohex(palet[i]))
            nam.append(get_color_name(palet[i]))

        print("Name of the colors are:", nam)
        print("RGB color palette:", rg)
        print("Hex color palette:", hexcode)
        domi = img.get_color()
        plt.imshow([[palet[i] for i in range(limit)]])
        plt.show()
    finally:
        os.remove(temp_file_path)  

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("colors.csv", names=index, header=None)

image = "bg.jpg"
reselect = 0
print("hello")

while True:
    print(
        '''Enter 1 For Basic Mode
Enter 2 For Advance Mode 
Enter 3 For Suggestion
Enter 0 To Exit
      '''
    )
    op = int(input("Your choice : "))

    if op == 0:
        break
    elif op == 1:
        Basic(image) 
    elif op == 2:
        root = tk.Tk()
        root.state('zoomed') 
        app = ImageCropperApp(root, Basic)
        root.mainloop()
    else:
        print("No Valid Input. Please enter a valid option.")

print("End!")
