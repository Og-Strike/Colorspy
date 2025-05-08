import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, Canvas, Frame
from PIL import Image, ImageTk
from colorthief import ColorThief
import pandas as pd
import seaborn as sns
import tkinter.messagebox
import pyperclip
import os
import cv2
import csv
import numpy as np
import time
import matplotlib.pyplot as plt
import tempfile
import pyautogui
from pygame import mixer
import keyboard

def get_color_name(cod):
    R,G,B=cod[0],cod[1],cod[2]
    min=1000
    closest_rgb=()
    closest_hex=""
    for i in range (len(csv)):
        diff=abs(R-int(csv.loc[i,"R"]))+abs(G-int(csv.loc[i,"G"]))+abs(B-int(csv.loc[i,"B"]))
        if diff<=min:
            min=diff
            cname=csv.loc[i,"color_name"]
            closest_rgb = (int(csv.loc[i, "R"]), int(csv.loc[i, "G"]), int(csv.loc[i, "B"]))
            closest_hex = csv.loc[i, "hex"]
    return cname

def Basic2(cropped_img, result_window):
    if cropped_img is None:
        tk.messagebox.showinfo("Invalid Image", "No valid cropped image to analyze and reuse.")
        return
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        cropped_img.save(temp_file, format="JPEG")
        temp_file_path = temp_file.name
    try:
        img = ColorThief(temp_file_path) 
        limit=1
        palet = img.get_palette(color_count=limit+1)
        hexcode = []
        rg = []
        nam = []

        def rgtohex(rgb):
            rg.append(rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

        for i in range(limit):
            hexcode.append(rgtohex(palet[i]))
            nam.append(get_color_name(palet[i]))
      
        domi = img.get_color()
        result_text = f"Name of the color: {nam[0]}\nRGB color: {rg[0]}\nHex color: {hexcode[0]}"
        result_label = tk.Label(result_window, text=result_text)
        result_label.pack()

        fig, ax = plt.subplots()

        im = ax.imshow([[palet[i] for i in range(limit)]])
        ax.axis('off')

        fig.savefig('temp_plot.png', bbox_inches='tight', pad_inches=0.0)

        saved_image = Image.open('temp_plot.png')
        photo = ImageTk.PhotoImage(saved_image)

        result_label1 = tk.Label(result_window, image=photo)
        result_label1.photo = photo 
        result_label1.pack()
    finally:
        os.remove(temp_file_path)  

mixer.init()

def music_start():
    mixer.music.load("bgm.mp3")
    mixer.music.play(2000000000)

def music_start1():
    mixer.music.unpause()

def music_stop():
    mixer.music.pause()

class ColorSpyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Spy")
        root.iconbitmap("logo1.ico")

        self.root.state('zoomed')

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        self.create_home_tab()

        self.create_basic_tab()

        self.create_image_cropper_tab()

        self.create_live()

        self.create_palette_generator_tab()

        self.create_pic_color_changer_tab()

        self.create_color_mixing()

        self.hover_temp_image = None
        self.hover_color_box = None
        self.hover_result_window = None

        self.modified_image = None

    def create_image_cropper_tab(self):
        image_cropper_tab = ttk.Frame(self.tabs)
        self.tabs.add(image_cropper_tab, text=" Image Spy |")

        self.image = None  

        file_frame = tk.Frame(image_cropper_tab)
        file_frame.pack(pady=20)

        open_button = tk.Button(file_frame,text="Open Image", command=self.load_image)
        open_button.pack(side="left")
        open_button = tk.Button(file_frame,text="Capture & Open Image", command=self.capture_and_process_image2)
        open_button.pack(side="left",padx=20)

        self.canvas = tk.Canvas(image_cropper_tab,cursor="cross", width=800, height=600)
        self.canvas.place(x=250,y=150)

        self.cropping = False
        self.temp_image = None
        self.color_box = None
        self.result_window=None

        self.canvas.bind("<ButtonPress-1>", self.capture_box)
        self.canvas.bind("<Motion>", self.on_hover)
        
    def load_image(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if image_path:
            self.image = Image.open(image_path)
            self.image = self.image.resize((screen_width-500, screen_height-400), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.image)

            self.canvas.delete("all")

            self.canvas.config(width=screen_width, height=screen_height)
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

    def capture_and_process_image2(self):
        user_profile_folder = os.path.expanduser("~")
        store_dir = os.path.join(user_profile_folder, "Color Spy", "Images")
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture a frame")
                break

            cv2.imshow('Live Capture (Press c to capture  & q to exit)', frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                image_path = os.path.join(store_dir, "image.jpg")
                cv2.imwrite(image_path, frame)
                print("Image captured")
                cv2.destroyAllWindows()
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        if image_path:
            self.image = Image.open(image_path)
            self.image = self.image.resize((screen_width-500, screen_height-400), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.image)

            self.canvas.delete("all")

            self.canvas.config(width=screen_width, height=screen_height)
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
                
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
        half_box_size = 2

        left = int(x - half_box_size)
        top = int(y - half_box_size)
        right = int(x + half_box_size)
        bottom = int(y + half_box_size)

        left = max(left, 0)
        top = max(top, 0)
        right = min(right, self.image.width)
        bottom = min(bottom, self.image.height)

        self.temp_image = self.image.crop((left, top, right, bottom))
        if self.result_window:
            self.result_window.destroy()
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("Color Analysis")

        Basic2(self.temp_image, self.result_window)

    def create_home_tab(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background="black")
        home_tab = ttk.Frame(self.tabs,style="Custom.TFrame")
        
        self.tabs.add(home_tab, text=" Home |")


        logo_image = Image.open("logo2.jpg")
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(home_tab, image=logo_photo,height=500,width=540,bg="black")
        logo_label.image = logo_photo
        logo_label.pack(pady=100)

        quote_label = tk.Label(home_tab, text="' Colors Are The Smiles Of Nature. '", font=("Arial", 24),fg="blue",bg="black")
        quote_label.pack(pady=10)

        t_label = tk.Label(home_tab, text="Press 'alt + s' to stop bg music and 'alt + p' to play again.", font=("Arial", 14),fg="white",bg="black")
        t_label.pack(pady=50)

    def create_basic_tab(self):
        basic_tab = ttk.Frame(self.tabs)
        self.tabs.add(basic_tab, text=" Color Extractor |")

        self.basic_file_path = tk.StringVar()
        file_frame = tk.Frame(basic_tab)
        file_frame.pack(pady=20)
        file_label = tk.Label(file_frame, text="Select an image:")
        file_label.pack(side="left")
        file_entry = tk.Entry(file_frame, textvariable=self.basic_file_path, width=40)
        file_entry.pack(side="left")
        file_button = tk.Button(file_frame, text="Browse", command=self.browse_file)
        file_button.pack(side="left",padx=5)
        file_button1 = tk.Button(file_frame, text="Capture", command=self.capture_and_process_image1)
        file_button1.pack(side="left",padx=10)

        self.basic_palette_entry = tk.StringVar()
        palette_frame = tk.Frame(basic_tab)
        palette_frame.pack(pady=10)
        palette_label = tk.Label(palette_frame, text="Enter the number of colors:")
        palette_label.pack(side="left")
        palette_entry = tk.Entry(palette_frame, textvariable=self.basic_palette_entry, width=5)
        palette_entry.pack(side="left")

        analyze_button = tk.Button(basic_tab, text="Analyze", command=self.basic_mode)
        analyze_button.pack(pady=10)

        self.basic_result_text = scrolledtext.ScrolledText(basic_tab, wrap=tk.WORD, width=50, height=15)
        self.basic_result_text.pack()

        color_boxes_frame = Frame(basic_tab)
        color_boxes_frame.pack(pady=10)

        self.basic_color_canvas = Canvas(color_boxes_frame, width=500, height=400)
        self.basic_color_canvas.pack(side="left", fill="both", expand=True)

        self.basic_color_scrollbar = ttk.Scrollbar(color_boxes_frame, orient="vertical", command=self.basic_color_canvas.yview)
        self.basic_color_scrollbar.pack(side="right", fill="y")

        self.basic_color_canvas.configure(yscrollcommand=self.basic_color_scrollbar.set)
        self.basic_color_canvas.bind("<Configure>", self.on_canvas_configure)

        self.color_boxes_frame_in_canvas = Frame(self.basic_color_canvas)
        self.basic_color_canvas.create_window((0, 0), window=self.color_boxes_frame_in_canvas, anchor="nw")

        self.root.bind("<MouseWheel>", self.on_mousewheel)

    def capture_and_process_image1(self):
        user_profile_folder = os.path.expanduser("~")
        store_dir = os.path.join(user_profile_folder, "Color Spy", "Images")
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture a frame")
                break

            cv2.imshow('Live Capture (Press c to capture  & q to exit)', frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                image_path = os.path.join(store_dir, "image.jpg")
                cv2.imwrite(image_path, frame)
                print("Image captured")
                cv2.destroyAllWindows()
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
        if image_path:
            self.basic_file_path.set(image_path)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.basic_file_path.set(file_path)
    
    def create_pic_color_changer_tab(self):
        pic_color_changer_tab = ttk.Frame(self.tabs)
        self.tabs.add(pic_color_changer_tab, text=" Pixel Changer |")

        file_frame = tk.Frame(pic_color_changer_tab)
        file_frame.pack(pady=20)
        file_label = tk.Label(file_frame, text="Select an image:")
        file_label.pack(side="left")
        self.pic_file_path = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=self.basic_file_path, width=40)
        file_entry.pack(side="left")
        file_button1 = tk.Button(file_frame, text="Browse", command=self.browse_pic_file)
        file_button1.pack(side="left",padx=5)
        file_button = tk.Button(file_frame, text="Capture", command=self.capture_and_process_image1)
        file_button.pack(side="left",padx=10)

        option_label = tk.Label(pic_color_changer_tab, text="Choose an option:")
        option_label.pack(pady=10)

        self.option_var = tk.IntVar()
        rgb_option = tk.Radiobutton(pic_color_changer_tab, text="RGB Value", variable=self.option_var, value=1)
        csv_option = tk.Radiobutton(pic_color_changer_tab, text="Search in CSV", variable=self.option_var, value=2)
        rgb_option.pack()
        csv_option.pack()

        self.rgb_frame = tk.Frame(pic_color_changer_tab)
        self.csv_frame = tk.Frame(pic_color_changer_tab)

        ur_label = tk.Label(self.rgb_frame, text="Give R Value                     :")
        ug_label = tk.Label(self.rgb_frame, text="Give G Value                     :")
        ub_label = tk.Label(self.rgb_frame, text="Give B Value                     :")
        self.ur_entry = tk.Entry(self.rgb_frame)
        self.ug_entry = tk.Entry(self.rgb_frame)
        self.ub_entry = tk.Entry(self.rgb_frame)

        ur_label.grid(row=0, column=0)
        ug_label.grid(row=1, column=0)
        ub_label.grid(row=2, column=0)
        self.ur_entry.grid(row=0, column=1)
        self.ug_entry.grid(row=1, column=1)
        self.ub_entry.grid(row=2, column=1)

        search_label = tk.Label(self.csv_frame, text="Color Name \ Hex Code  :")
        self.search_entry = tk.Entry(self.csv_frame)
        search_label.grid(row=0, column=0)
        self.search_entry.grid(row=0, column=1)

        self.color_threshold = 30
        self.threshold_slider = tk.Scale(
            pic_color_changer_tab,
            from_=0,
            to=100,
            orient="horizontal",
            label="Color Threshold",
            variable=self.color_threshold,
            resolution=5
        )
        self.threshold_slider.set(self.color_threshold)
        self.threshold_slider.pack(pady=10)

        change_button = tk.Button(pic_color_changer_tab, text="Change Color", command=self.change_pic_colors)
        change_button.pack(pady=10)

        save_button = tk.Button(pic_color_changer_tab, text="Reuse Image", command=self.reuse_img)
        save_button.pack(pady=10)

        self.rgb_frame.pack()
        self.csv_frame.pack()

    def change_pic_colors(self):
        file_path = self.basic_file_path.get()
        option = self.option_var.get()

        if not file_path:
            tk.messagebox.showinfo("Invalid File", "File path is empty.")
            return

        try:
            pic = cv2.imread(file_path)

            cv2.namedWindow('Select Pixel')

            cr = None
            cg = None
            cb = None

            def on_mouse_click(event, x, y, flags, param):
                nonlocal cr, cg, cb
                if event == cv2.EVENT_LBUTTONDOWN:
                    (cb, cg, cr) = pic2[y, x]  
                    cv2.destroyAllWindows()

            cv2.setMouseCallback('Select Pixel', on_mouse_click)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            scale_factor = min(screen_width / pic.shape[1], screen_height / pic.shape[0])
            pic2 = cv2.resize(pic, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA) 
            cv2.imshow('Select Pixel', pic2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if option == 1:  
                ur = int(self.ur_entry.get())
                ug = int(self.ug_entry.get())
                ub = int(self.ub_entry.get())
                result = [ur, ug, ub]
            elif option == 2: 
                csv_file_path = 'colors.csv'  
                search_value = self.search_entry.get().strip()
                if search_value.startswith("#") and len(search_value) == 7:
                    result = self.hex_to_rgb(search_value)
                else:
                    search_name = self.search_entry.get().lower().capitalize()
                    result = self.search_color_in_csv(csv_file_path, search_name)
            else:
                print("Invalid option selected.")
                tk.messagebox.showinfo("Invalid Option Selected.", "Choose a valid option between Search In CSV or RGB value .")
                return
            pic1 = Image.open(file_path)
            newr, newg, newb = result[0], result[1], result[2]
            
            x, y, w, h= cv2.selectROI("ROI Selection (Space to Confirm, C to Stop)",pic2)
            cv2.destroyAllWindows()

            color_threshold = self.color_threshold

            x_orig, y_orig, w_orig, h_orig = int(x / scale_factor), int(y / scale_factor), int(w / scale_factor), int(h / scale_factor)

            color_threshold = self.color_threshold

            for i in range(x_orig, min(x_orig + w_orig, pic1.width)):
                for j in range(y_orig, min(y_orig + h_orig, pic1.height)):
                    r, g, b = pic1.getpixel((i, j))
                    if self.is_color_similar((cr, cg, cb), (r, g, b), color_threshold):
                        pic1.putpixel((i, j), (newr, newg, newb))

            pic1.show()
            self.modified_image = pic1.copy()
        except Exception as e:
            tk.messagebox.showinfo("Exception", f"Error color {str(e)}")

    def change_pic_colors1(self,file_path):
        option = self.option_var.get()

        if not file_path:
            print("No file selected.")
            return

        try:
            pic = cv2.imread(file_path)

            cv2.namedWindow('Select Pixel')

            cr = None
            cg = None
            cb = None

            def on_mouse_click(event, x, y, flags, param):
                nonlocal cr, cg, cb
                if event == cv2.EVENT_LBUTTONDOWN:
                    (cb, cg, cr) = pic2[y, x]  
                    cv2.destroyAllWindows()

            cv2.setMouseCallback('Select Pixel', on_mouse_click)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            scale_factor = min(screen_width / pic.shape[1], screen_height / pic.shape[0])
            pic2 = cv2.resize(pic, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA) 
            cv2.imshow('Select Pixel', pic2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if option == 1:  
                ur = int(self.ur_entry.get())
                ug = int(self.ug_entry.get())
                ub = int(self.ub_entry.get())
                result = [ur, ug, ub]
            elif option == 2: 
                csv_file_path = 'colors.csv'  
                search_value = self.search_entry.get().strip()
                if search_value.startswith("#") and len(search_value) == 7:
                    result = self.hex_to_rgb(search_value)
                else:
                    search_name = self.search_entry.get().lower().capitalize()
                    result = self.search_color_in_csv(csv_file_path, search_name)
            else:
                tk.messagebox.showinfo("Invalid Option Selected.", "Choose a valid option between Search in csv or RGB value .")
                return
            pic1 = Image.open(file_path)
            newr, newg, newb = result[0], result[1], result[2]
            
            x, y, w, h= cv2.selectROI("ROI Selection (Space to Confirm, C to Stop)",pic2)
            cv2.destroyAllWindows()

            color_threshold = self.color_threshold

            x_orig, y_orig, w_orig, h_orig = int(x / scale_factor), int(y / scale_factor), int(w / scale_factor), int(h / scale_factor)

            color_threshold = self.color_threshold

            for i in range(x_orig, min(x_orig + w_orig, pic1.width)):
                for j in range(y_orig, min(y_orig + h_orig, pic1.height)):
                    r, g, b = pic1.getpixel((i, j))
                    if self.is_color_similar((cr, cg, cb), (r, g, b), color_threshold):
                        pic1.putpixel((i, j), (newr, newg, newb))

            pic1.show()
            self.modified_image = pic1.copy()
        except Exception as e:
            tk.messagebox.showinfo("Exception", f"Error: {str(e)}")

    def is_color_similar(color1, color2, threshold):
        color1 = np.array(color1)
        color2 = np.array(color2)
        distance = np.linalg.norm(color1 - color2)
        return distance <= threshold
    
    def hex_to_rgb(self, hex_value):
        hex_value = hex_value.lstrip("#")
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

    def browse_pic_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.basic_file_path.set(file_path)
            self.temp_image = cv2.imread(file_path)  

    def reuse_img(self):
        save_path = "modified_image.jpg" 
        self.modified_image.save(save_path)
        self.change_pic_colors1(save_path)

    def search_color_in_csv(self, csv_file_path, search_name):
        df = pd.read_csv(csv_file_path)
        filtered_df = df[df.iloc[:, 1] == search_name]

        if not filtered_df.empty:
            result = filtered_df.iloc[0, 3:6].tolist()
            print(f"Results for '{search_name}': {result}")
            return result
        else:
            print(f"No results found for '{search_name}' in the CSV.")
            return []

    def create_palette_generator_tab(self):
        generator_tab = ttk.Frame(self.tabs)
        self.tabs.add(generator_tab, text=" Color Palette Generator |")

        self.palette_num_colors = tk.StringVar()
        num_colors_frame = tk.Frame(generator_tab)
        num_colors_frame.pack(pady=20)
        num_colors_label = tk.Label(num_colors_frame, text="Enter the number of colors:")
        num_colors_label.pack(side="left")
        num_colors_entry = tk.Entry(num_colors_frame, textvariable=self.palette_num_colors, width=5)
        num_colors_entry.pack(side="left")

        self.palette_color_list = tk.StringVar()
        color_list_frame = tk.Frame(generator_tab)
        color_list_frame.pack(pady=10)
        color_list_label = tk.Label(color_list_frame, text="Enter a list of colors (comma-separated):")
        color_list_label.pack(side="left")
        color_list_entry = tk.Entry(color_list_frame, textvariable=self.palette_color_list, width=30)
        color_list_entry.pack(side="left")

        generate_button = tk.Button(generator_tab, text="Generate Palette", command=self.generate_palette)
        generate_button.pack(pady=10)

        self.palette_frame = tk.Frame(generator_tab)
        self.palette_frame.pack()

    def generate_palette(self):

        for widget in self.palette_frame.winfo_children():
            widget.destroy()
    
        num_colors = self.palette_num_colors.get()
    
        color_list_str = self.palette_color_list.get()

        if not color_list_str:
            tk.messagebox.showinfo("Colors List", "Color list is empty.")
            return

        if not num_colors:
            tk.messagebox.showinfo("No. Of Colors", "Please enter the valid no. of Colors.")
            return
        
        

        try:
            num_colors = int(num_colors)
        
            if num_colors <= 0:
                tk.messagebox.showinfo("No. Of Colors", "Please enter the valid no. of Colors.")
                return

            if color_list_str:
                color_list = [color.strip() for color in color_list_str.split(",")]
                color_num = len(color_list)
                if color_num<=1:
                    tk.messagebox.showinfo("Colors List", "Please enter 2 or mor more color name.")
                    return
            else:
                color_list = []

            blended_palette = sns.blend_palette(color_list, num_colors)

            if num_colors <= 100:
                self.display_palette(blended_palette)
            else:
                tk.messagebox.showinfo("Invalid Range", "The number of colors should be 100 or less.")

        except ValueError:
            tk.messagebox.showinfo("Colors Not Found", "Plese enter a valid color name.")
            return

    def display_palette(self, blended_palette):
    
        num_colors_per_row = 20
        rect_width = 80
        rect_height = 80

        for i, color in enumerate(blended_palette):

            color_str = "#{:02X}{:02X}{:02X}".format(
            int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

            color_frame = tk.Frame(self.palette_frame, width=rect_width, height=rect_height + 60)
            color_frame.grid(row=i // num_colors_per_row, column=i % num_colors_per_row)

            color_canvas = Canvas(color_frame, width=rect_width, height=rect_height)
            color_canvas.create_rectangle(0, 0, rect_width, rect_height, fill=color_str)
            color_canvas.pack()

            hex_label = tk.Label(color_frame, text=color_str)
            hex_label.pack()

            copy_button = tk.Button(color_frame, text="Copy", command=lambda text=color_str: self.copy_to_clipboard(text))
            copy_button.pack()

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def basic_mode(self):
        file_path = self.basic_file_path.get()
        num_colors = self.basic_palette_entry.get()

        if not file_path:
            tk.messagebox.showinfo("File Eroor", "No file selected.")
            return

        if not num_colors:
            tk.messagebox.showinfo("No. Of Colors", "Please enter the number of colors.")
            return

        try:
            num_colors = int(num_colors)
        except ValueError:
            tk.messagebox.showinfo("Invalid Input", "Please enter a valid number.")
            return

        if num_colors <= 0:
            tk.messagebox.showinfo("No. Of Colors", "Please enter the number of colors to 1 or more then 1.")
            return

        max_colors = 50

        if num_colors > max_colors:
            tk.messagebox.showinfo("Invalid Range", f"Number of colors requested ({num_colors}) exceeds the maximum available ({max_colors}).")
            return

        names, hex_values, rgb_values = self.basic_color_analysis(file_path, num_colors)

        result_text = ""
        max_colors_per_row = 4
        for i in range(len(hex_values)):
            if i % max_colors_per_row == 0:
                result_text += "\n" 
            result_text += f"Color {i + 1} - Name: {names[i]}, Hex: {hex_values[i]}, RGB: {rgb_values[i]}\n"

        self.basic_result_text.delete(1.0, tk.END) 
        self.basic_result_text.insert(tk.END, result_text)

        self.display_color_boxes1(hex_values)

    def basic_color_analysis(self, image_path, num_colors):
        img = ColorThief(image_path)
        palette = img.get_palette(color_count=num_colors)

        names = []
        hex_values = []
        rgb_values = []

        for color in palette:
            rgb = tuple(color)
            hex_value = "#{:02X}{:02X}{:02X}".format(*rgb)
            names.append(self.get_color_name(rgb))
            hex_values.append(hex_value)
            rgb_values.append(rgb)

        return names, hex_values, rgb_values

    def display_color_boxes(self, hex_colors):
        for widget in self.color_boxes_frame_in_canvas.winfo_children():
            widget.destroy()

        max_colors_per_row = 4
        box_size = 80
        x, y = 10, 10

        for i, hex_color in enumerate(hex_colors):
            color_box = tk.Label(self.color_boxes_frame_in_canvas, bg=hex_color, width=box_size, height=box_size)
            color_box.grid(row=i // max_colors_per_row, column=i % max_colors_per_row, padx=10, pady=10)

            copy_button_frame = tk.Frame(self.color_boxes_frame_in_canvas)
            copy_button_frame.grid(row=i // max_colors_per_row + 1, column=i % max_colors_per_row, padx=10, pady=2)

            color_number_label = tk.Label(copy_button_frame, text=f"Color {i + 1}", font=("Arial", 10))
            color_number_label.pack()

            copy_button = tk.Button(copy_button_frame, text="Copy", command=lambda text=hex_color: self.copy_to_clipboard(text))
            copy_button.pack()

        self.basic_color_canvas.update_idletasks()
        self.basic_color_canvas.config(scrollregion=self.basic_color_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.basic_color_canvas.config(scrollregion=self.basic_color_canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.basic_color_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def create_live(self):
        generator_tab = ttk.Frame(self.tabs)
        self.tabs.add(generator_tab, text=" Live Detection |")

        text_label = tk.Label(generator_tab, text="Click the below button to start live detection", font=("Arial", 16))
        text_label.pack(pady=20)

        button_frame = tk.Frame(generator_tab)
        button_frame.pack(expand=True)
        generate_button = tk.Button(button_frame, text="Live Detection", command=self.capture_and_process_image, font=("Arial", 14))
        generate_button.pack(pady=10)

    def get_color_name(self, rgb):
        R,G,B=rgb[0],rgb[1],rgb[2]
        min=1000
        for i in range (len(csv)):
            diff=abs(R-int(csv.loc[i,"R"]))+abs(G-int(csv.loc[i,"G"]))+abs(B-int(csv.loc[i,"B"]))
            if diff<=min:
                min=diff
                cname=csv.loc[i,"color_name"]
        return cname

    def get_color_name1(self,cod):
        R,G,B=cod[0],cod[1],cod[2]
        min=1000
        closest_rgb=()
        closest_hex=""
        for i in range (len(csv)):
            diff=abs(R-int(csv.loc[i,"R"]))+abs(G-int(csv.loc[i,"G"]))+abs(B-int(csv.loc[i,"B"]))
            if diff<=min:
                min=diff
                cname=csv.loc[i,"color_name"]
                closest_rgb = (int(csv.loc[i, "R"]), int(csv.loc[i, "G"]), int(csv.loc[i, "B"]))
                closest_hex = csv.loc[i, "hex"]
        return cname,closest_rgb,closest_hex
    
    def Basic1(self,image_path):
        img= ColorThief(image_path)
        palet = img.get_palette(color_count=2)
        hexcode=""
        rg=()
        nam=""
        nam,rg,hexcode=(self.get_color_name1(palet[0]))
        return nam,hexcode,rg

    def display_color_boxes1(self, hex_colors):
        for widget in self.color_boxes_frame_in_canvas.winfo_children():
            widget.destroy()

        max_colors_per_row = 4
        box_size = 80
        x, y = 10, 10  

        for i, hex_color in enumerate(hex_colors):
            if i % max_colors_per_row == 0 and i != 0:
                x = 10 
                y += box_size + 40  
            color_frame = Frame(self.color_boxes_frame_in_canvas, width=box_size, height=box_size)
            color_frame.grid_propagate(False)
            color_frame.grid(row=i // max_colors_per_row, column=i % max_colors_per_row, padx=5, pady=10)
            color_box = Canvas(color_frame, width=box_size, height=box_size, bg=hex_color)
            color_box.pack(fill="both", expand=True)

            color_number_label = tk.Label(color_frame, text=f"Color {i + 1}", font=("Arial", 10), bg="white")
            color_number_label.pack(fill="both")

        self.basic_color_canvas.update_idletasks()
        self.basic_color_canvas.config(scrollregion=self.basic_color_canvas.bbox("all"))   

    def capture_and_process_image(self):

        user_profile_folder = os.path.expanduser("~")

        temp_dir = os.path.join(user_profile_folder, "Color Spy", "temp")

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        cap = cv2.VideoCapture(0) 

        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    tk.messagebox.showinfo("Capture", "Failed to capture a frame.")
                    break

                height, width, _ = frame.shape
                _ = pyautogui.size()

                center_x = width // 2
                center_y = height // 2

                small_image_size = (50, 50) 
                center_x = width // 2
                center_y = height // 2
                top_left = (center_x - small_image_size[0] // 2, center_y - small_image_size[1] // 2)
                bottom_right = (center_x + small_image_size[0] // 2, center_y + small_image_size[1] // 2)

                small_image = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

                image_path = os.path.join(temp_dir, "small_image.jpg")
                cv2.imwrite(image_path, small_image)

                name, hex_value, rgb_value = self.Basic1(image_path)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

      
                cv2.putText(frame, f"Name: {name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Hex: {hex_value}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"RGB: {rgb_value}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow("Live Video (Press Q to exit)", frame)
                if os.path.exists(image_path):
                    os.remove(image_path)

                time.sleep(0.1)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except KeyboardInterrupt:
            tk.messagebox.showinfo("Capture", "Process stopped by you.")

        cap.release()
        cv2.destroyAllWindows()

    def create_color_mixing(self):

        mix_tab = ttk.Frame(self.tabs)
        self.tabs.add(mix_tab, text=" Color Mixing ")

        frame1 = tk.Frame(mix_tab)
        frame1.pack(side="left", padx=10)

        color_label = tk.Label(frame1, text="Enter Color 1 name:")
        color_label.pack(pady=10)

        color_entry = tk.Entry(frame1)
        color_entry.pack()

        search_button = tk.Button(frame1, text="Search Color 1", command=lambda: self.search_color(color_entry, r_slider, g_slider, b_slider, intensity_slider, color_box, result_label))
        search_button.pack(pady=10)

        result_label = tk.Label(frame1, text="", padx=20, pady=20)
        result_label.pack()

        color_box = tk.Label(frame1, text="", width=20, height=5)
        color_box.pack()

        r_slider = tk.Scale(frame1, label="R", from_=0, to=255, orient="horizontal", length=300)
        r_slider.pack(padx=10)
        g_slider = tk.Scale(frame1, label="G", from_=0, to=255, orient="horizontal", length=300)
        g_slider.pack()
        b_slider = tk.Scale(frame1, label="B", from_=0, to=255, orient="horizontal", length=300)
        b_slider.pack()

        intensity_slider = tk.Scale(frame1, label="Intensity", from_=0, to=1, resolution=0.01, orient="horizontal", length=300)
        intensity_slider.pack()

        r_slider.config(command=lambda value: self.update_color_box(r_slider.get(), g_slider.get(), b_slider.get(), intensity_slider, color_box, result_label))
        g_slider.config(command=lambda value: self.update_color_box(r_slider.get(), g_slider.get(), b_slider.get(), intensity_slider, color_box, result_label))
        b_slider.config(command=lambda value: self.update_color_box(r_slider.get(), g_slider.get(), b_slider.get(), intensity_slider, color_box, result_label))


        intensity_slider.config(command=lambda value: self.update_color_box(r_slider.get(), g_slider.get(), b_slider.get(), intensity_slider, color_box, result_label))

        frame2 = tk.Frame(mix_tab)
        frame2.pack(side="right", padx=10)

        color2_label = tk.Label(frame2, text="Enter Color 2 name:")
        color2_label.pack(pady=10)

        color2_entry = tk.Entry(frame2)
        color2_entry.pack()

        search_button2 = tk.Button(frame2, text="Search Color 2", command=lambda: self.search_color2(color2_entry, r2_slider, g2_slider, b2_slider, intensity_slider2, color2_box, result_label2))
        search_button2.pack(pady=10)

        result_label2 = tk.Label(frame2, text="", padx=20, pady=20)
        result_label2.pack()

        color2_box = tk.Label(frame2, text="", width=20, height=5)
        color2_box.pack()

        r2_slider = tk.Scale(frame2, label="R", from_=0, to=255, orient="horizontal", length=300)
        r2_slider.pack()
        g2_slider = tk.Scale(frame2, label="G", from_=0, to=255, orient="horizontal", length=300)
        g2_slider.pack()
        b2_slider = tk.Scale(frame2, label="B", from_=0, to=255, orient="horizontal", length=300)
        b2_slider.pack()

        intensity_slider2 = tk.Scale(frame2, label="Intensity", from_=0, to=1, resolution=0.01, orient="horizontal", length=300)
        intensity_slider2.pack()

        r2_slider.config(command=lambda value: self.update_color_box(r2_slider.get(), g2_slider.get(), b2_slider.get(), intensity_slider2, color2_box, result_label2))
        g2_slider.config(command=lambda value: self.update_color_box(r2_slider.get(), g2_slider.get(), b2_slider.get(), intensity_slider2, color2_box, result_label2))
        b2_slider.config(command=lambda value: self.update_color_box(r2_slider.get(), g2_slider.get(), b2_slider.get(), intensity_slider2, color2_box, result_label2))


        intensity_slider2.config(command=lambda value: self.update_color_box(r2_slider.get(), g2_slider.get(), b2_slider.get(), intensity_slider2, color2_box, result_label2))

        mix_frame = tk.Frame(mix_tab)
        mix_frame.pack(pady=20)

        mix_button = tk.Button(mix_frame, text="Mix Colors", command=lambda: self.mix_colors(r_slider, g_slider, b_slider, intensity_slider, color3_box, result_label3, r2_slider, g2_slider, b2_slider, intensity_slider2, color2_box))
        mix_button.pack()

        result_label3 = tk.Label(mix_frame, text="", padx=20, pady=20)
        result_label3.pack()

        color3_box = tk.Label(mix_frame,text="", width=20, height=5)
        color3_box.pack()

    def search_color(self,color_entry, r_slider, g_slider, b_slider, intensity_slider, color_box, result_label):
        csv = pd.read_csv('colors.csv', header=None, index_col=[1])
        color_name = color_entry.get().strip().lower()
        result_text = ""
    
        for index, row in csv.iterrows():
            if color_name == index.strip().lower():
                r, g, b = row[3], row[4], row[5] 
                r_slider.set(r)
                g_slider.set(g)
                b_slider.set(b)
                intensity_slider.set(1.0)
                self.update_color_box(r, g,b, intensity_slider, color_box, result_label)
                break
        else:
            result_text = f"Color 1 '{color_name}' not found in the CSV file."
            r_slider.set(0)
            g_slider.set(0)
            b_slider.set(0)
            intensity_slider.set(0)
            self.update_color_box(0, 0, 0, intensity_slider, color_box)

        result_label.config(text=result_text)

    def search_color2(self,color2_entry, r2_slider, g2_slider, b2_slider, intensity_slider2, color2_box, result_label2):
        csv = pd.read_csv('colors.csv', header=None, index_col=[1])
        color_name = color2_entry.get().strip().lower()
        result_text = ""
    
        for index, row in csv.iterrows():
            if color_name == index.strip().lower():
                r, g, b = row[3], row[4], row[5] 
                r2_slider.set(r)
                g2_slider.set(g)
                b2_slider.set(b)
                intensity_slider2.set(1.0)
                self.update_color_box(r, g, b, intensity_slider2, color2_box)

                break
        else:
            result_text = f"Color 2 '{color_name}' not found in the CSV file."
            r2_slider.set(0)
            g2_slider.set(0)
            b2_slider.set(0)
            intensity_slider2.set(0)
            self.update_color_box(0, 0, 0, intensity_slider2, color2_box)

        result_label2.config(text=result_text)

    def mix_colors(self,r_slider, g_slider, b_slider, intensity_slider, color3_box, result_label3, r2_slider, g2_slider, b2_slider, intensity_slider2, color2_box):
        r1, g1, b1 = r_slider.get(), g_slider.get(), b_slider.get()
        r2, g2, b2 = r2_slider.get(), g2_slider.get(), b2_slider.get()

        mixed_r = (r1 + r2 * intensity_slider2.get())
        mixed_g = (g1 + g2 * intensity_slider2.get())
        mixed_b = (b1 + b2 * intensity_slider2.get())

        max_component = max(mixed_r, mixed_g, mixed_b)
        if max_component > 255:
            mixed_r = 255 * mixed_r / max_component
            mixed_g = 255 * mixed_g / max_component
            mixed_b = 255 * mixed_b / max_component

        self.update_color_box(mixed_r, mixed_g, mixed_b, intensity_slider, color3_box)
    
        nearest_mixed_color = self.find_nearest_color(mixed_r, mixed_g, mixed_b)
        hexcode = "#{:02X}{:02X}{:02X}".format(int(mixed_r), int(mixed_g), int(mixed_b))
        result_text = f"Name of the mixed color: {nearest_mixed_color}\nRGB color: {int(mixed_r)}, {int(mixed_g)}, {int(mixed_b)}\nHex Color : {hexcode}"
        result_label3.config(text=result_text)

    def update_color_box(self,r, g, b, intensity, color_box, result_label=None):
        r = (r * intensity.get())
        g = (g * intensity.get())
        b = (b * intensity.get())

        r = min(255, max(0, r))
        g = min(255, max(0, g))
        b = min(255, max(0, b))
        color_hex = "#{:02X}{:02X}{:02X}".format(int(r),int(g),int(b))
        color_box.config(bg=color_hex)
    
        if result_label is not None:
            min_diff=1000
            for i in range (len(csv)):
                diff=abs(r-int(csv.loc[i,"R"]))+abs(g-int(csv.loc[i,"G"]))+abs(b-int(csv.loc[i,"B"]))
                if diff<=min_diff:
                    min_diff=diff
                    cname=csv.loc[i,"color_name"]
        
            result_text = f"Name of the color: {cname}\nRGB color: {r}, {g}, {b}\nHex color: {color_hex}"
            result_label.config(text=result_text)

    def find_nearest_color(self,r, g, b):
        min=1000
        for i in range (len(csv)):
            diff=abs(r-int(csv.loc[i,"R"]))+abs(g-int(csv.loc[i,"G"]))+abs(b-int(csv.loc[i,"B"]))
            if diff<=min:
                min=diff
                cname=csv.loc[i,"color_name"]
        return cname

    def update_result_label(self,r, g, b, result_label):
        hexcode = "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))
        result_text = f"RGB color: {int(r)}, {int(g)}, {int(b)}\nHex color: {hexcode}"
        result_label.config(text=result_text)

if __name__ == "__main__":
    csv = pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)
    music_start()
    keyboard.add_hotkey('alt + p', music_start1)
    keyboard.add_hotkey('alt + s', music_stop)
    root = tk.Tk()
    app = ColorSpyApp(root)
    root.mainloop()
    