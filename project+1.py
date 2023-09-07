import tkinter as tk
from PIL import Image, ImageTk
from colorthief import ColorThief
import matplotlib.pyplot as plt
import pandas as pd
import os
import tempfile

class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")

        self.image = Image.open("bg.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.cropping = False
        
        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)
        
        self.cropped_image = None
        
    def start_crop(self, event):
        if not self.cropping:
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)
            self.cropping = True
    
    def update_crop(self, event):
        if self.cropping:
            cur_x = self.canvas.canvasx(event.x)
            cur_y = self.canvas.canvasy(event.y)
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
    
    def end_crop(self, event):
        if self.cropping:
            self.end_x = self.canvas.canvasx(event.x)
            self.end_y = self.canvas.canvasy(event.y)
            
            # Perform the crop
            left = min(self.start_x, self.end_x)
            top = min(self.start_y, self.end_y)
            right = max(self.start_x, self.end_x)
            bottom = max(self.start_y, self.end_y)
            self.cropped_image = self.image.crop((left, top, right, bottom))
            
            self.cropping = False
            self.root.quit()
            self.root.destroy() 

def get_color_name(cod):
    R, G, B = cod[0], cod[1], cod[2]
    min_diff = 1000
    for i in range(len(csv)):
        diff = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if diff <= min_diff:
            min_diff = diff
            cname = csv.loc[i, "color_name"]
    return cname

def Basic(cropped_img):
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
        
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv = pd.read_csv("colors.csv", names=index, header=None)

image = "bg.jpg"
reselect = 0
print("hello")
print('''Enter 1 For Basic Mode
Enter 2 For Advance Mode 
Enter 3 For Suggestion
      ''')
op = int(input("Your choice : "))

while op != 0:
    if op == 1:
        Basic(image)
        break
    elif op == 2:
        root = tk.Tk()
        app = ImageCropperApp(root)
        root.mainloop()

        cropped_img = app.cropped_image
        Basic(cropped_img)
        break
    else:
        print("No Valid Input Exiting The Program")
        op = 0

print("End!")
