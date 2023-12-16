import cv2
import numpy as np
import customtkinter as ctk
from image_wedges import *
from PIL import Image, ImageTk, ImageOps, ImageEnhance
from menu import Menu
import matplotlib.pyplot as plt



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')  # Default appearance mode
        self.geometry('1000x600')
        self.title('ToolBox')
        self.minsize(800, 500)
        

        # sliders
        self.init_parameters()

        # canvas data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # Layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # Widgets
        self.create_widgets()

        # Run
        self.mainloop()

    def init_parameters(self):
        self.pos_var = {
            'rotate': ctk.DoubleVar(value=ROTATE_DEFAULT),
            'zoom': ctk.DoubleVar(value=ZOOM_DEFAULT),
            'translation_sw': ctk.BooleanVar(value=TRANSLATION_SW_DEFAULT),
            'translation': ctk.IntVar(value=TRANSLATION_DEFAULT),
            'deskewing_sw': ctk.BooleanVar(value=DESKEWING_SW_DEFAULT),
            'deskewing': ctk.DoubleVar(value=DESKEWING_DEFAULT),
            'flip': ctk.StringVar(value=FLIP_OPTIONS[0])
        }
        self.color_var = {
            'brightness': ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'grayscale': ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            'invert': ctk.BooleanVar(value=INVERT_DEFAULT),
            'eq': ctk.IntVar(value=CONTRAST_DEFAULT),  # New contrast parameter
            'hist': ctk.BooleanVar(value=HIST_BUTTON_DEFAULT),
            'vibrance': ctk.DoubleVar(value=VIBRANCE_DEFAULT)
        }
        self.effect_var = {
            'blur': ctk.DoubleVar(value=BLUR_DEFAULT),
            'blur_averaging': ctk.IntVar(value=BLUR_DEFAULT),
            'contrast': ctk.IntVar(value=CONTRAST_DEFAULT),  # New contrast parameter
            'Thresholding_sw': ctk.BooleanVar(value=THRESHOLDING_SW_DEFAULT),
            'Thresholding': ctk.DoubleVar(value=THRESHOLDING_DEFAULT),
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0]),
            'Find_Edges': ctk.StringVar(value=FIND_EDGES_OPTIONS[0])
        }
        # tracing
        combined_vars = list(self.pos_var.values()) + list(self.color_var.values()) + list(self.effect_var.values())
        for var in combined_vars:
            var.trace('w', self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original.copy()
        
        global tty, ttx
        ty = 0
        tx = 0
        
        # Rotate (using OpenCV)
        rotation_angle = self.pos_var['rotate'].get()
        height, width = self.image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), rotation_angle, 1)
        self.image = cv2.warpAffine(self.image, rotation_matrix, (width, height))

        zoom_factor = self.pos_var['zoom'].get()
        if abs(zoom_factor - 1) > 0.01:
            resized_width = int(self.image.shape[1] * zoom_factor)
            resized_height = int(self.image.shape[0] * zoom_factor)
            if resized_width > 0 and resized_height > 0:  # Ensure valid resizing dimensions
                self.image = cv2.resize(self.image, (resized_width, resized_height), interpolation=cv2.INTER_AREA)

        # Translation operation
        if self.pos_var['translation_sw'].get():
            ty = self.pos_var['translation'].get()
            translation_matrix = np.float32([[1, 0, ttx], [0, 1, ty]])
            self.image = cv2.warpAffine(self.image, translation_matrix, (width, height))
            tty = ty
        else:
            tx = self.pos_var['translation'].get()
            translation_matrix = np.float32([[1, 0, tx], [0, 1, tty]])
            self.image = cv2.warpAffine(self.image, translation_matrix, (width, height))
            ttx = tx

        # Flip (using OpenCV)
        flip_mode = self.pos_var['flip'].get()
        if flip_mode == 'X':
            self.image = cv2.flip(self.image, 1)
        elif flip_mode == 'Y':
            self.image = cv2.flip(self.image, 0)
        elif flip_mode == 'Both':
            self.image = cv2.flip(self.image, -1)

        # Brightness (OpenCV equivalent)
        brightness_value = self.color_var['brightness'].get()
        self.image = cv2.convertScaleAbs(self.image, alpha=brightness_value, beta=0)

        # Vibrance (OpenCV equivalent)
        vibrance_value = self.color_var['vibrance'].get()
        self.image = cv2.convertScaleAbs(self.image, alpha=1 + vibrance_value, beta=0)

        # Grayscale (OpenCV equivalent)
        if self.color_var['grayscale'].get():
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Invert (OpenCV equivalent)
        if self.color_var['invert'].get():
            self.image = cv2.bitwise_not(self.image)

        # GaussianBlur
        contrast_value = float(self.effect_var['contrast'].get())  # Get the blur value
        if contrast_value > 0:
            # Perform histogram equalization based on slider value
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.equalizeHist(self.image)
            alpha = self.effect_var['contrast'].get() / 10.0  # Scale the slider value
            self.image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=0)
            
        # # Create an averaging kernel
        # kernel_size = float(self.effect_var['blur'].get())  # Get the blur value
        # kernel_size = int(kernel_size)  # Convert to integer
        # # Ensure the kernel size is odd
        # kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        # kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)

        # # Apply the filter using OpenCV filter2D function
        # self.image = cv2.filter2D(self.image, -1, kernel)
        # self.image = np.uint8(np.absolute(self.image))



        # Contrast adjustment (OpenCV equivalent)
        contrast_value = self.effect_var['contrast'].get()
        self.image = cv2.addWeighted(self.image, 1 + contrast_value * 0.01, self.image, -contrast_value * 0.01, 0)

        # Edge detecting
        detect_option = self.effect_var['Find_Edges'].get()
        if detect_option == 'Laplacian':
            # self.image = cv2.flip(self.image, 1)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.Laplacian(self.image, cv2.CV_64F)
            self.image = np.uint8(np.absolute(self.image))

        elif detect_option == 'Sobel_X':
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.Sobel(self.image, cv2.CV_64F, 1, 0)
            self.image = np.uint8(np.absolute(self.image))

        elif detect_option == 'Sobel_Y':
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.Sobel(self.image, cv2.CV_64F, 0, 1)
            self.image = np.uint8(np.absolute(self.image))

        elif detect_option == 'Sobel':
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            sobelx = cv2.Sobel(self.image, cv2.CV_64F, 1, 0)
            sobely = cv2.Sobel(self.image, cv2.CV_64F, 0, 1)
            self.image = cv2.bitwise_or(sobelx, sobely)
            self.image = np.uint8(np.absolute(self.image))

        # Thresholding operation
        if self.effect_var['Thresholding_sw'].get():
                # iS_THRESHOLD_ON = True
                threshold_value = self.effect_var['Thresholding'].get()  # Get the threshold value from the slider
                ret, self.image = cv2.threshold(self.image, threshold_value, 255, cv2.THRESH_BINARY)

        # # Check if the "Show Hist" button is pressed
        # if self.color_var['hist'].get():
        #     # Convert the image to grayscale if it's a color image
        #     gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        #     # Compute the histogram using OpenCV
        #     histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

        #     # Plot the histogram using Matplotlib
        #     plt.figure(figsize=(8, 6))
        #     plt.plot(histogram, color='black')
        #     plt.title('Grayscale Histogram')
        #     plt.xlabel('Pixel value')
        #     plt.ylabel('Frequency')
        #     plt.show()

        self.place_image()

    def create_widgets(self):
        self.image_import = ImageImport(self, self.import_image)
        self.image_import.grid(row=0, column=0, sticky='nsew')

    def import_image(self, path):
        self.original = cv2.imread(path)
        self.image = self.original
        self.image_ratio = self.image.shape[1] / self.image.shape[0]

        # Hide the "Choose image" button
        self.image_import.grid_forget()

        # Display the image and close button
        self.image_output = ImageOutput(self, self.resize_image)
        self.close_button = CloseOutput(self, self.close_edit)
        self.menu = Menu(self, self.pos_var, self.color_var, self.effect_var)

        self.image_output.grid(row=0, column=1, sticky='nsew')
        self.close_button.place(x=0, y=0)  # Adjust the position of the close button

    def close_edit(self):
        # hide the image and the close button
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()

        # recreate the import button at its previous position
        self.create_widgets()

    def resize_image(self, event):
        # current canvas ratio
        canvas_ratio = event.width / event.height

        # update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        # resize
        if canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
        self.manipulate_image()

    def place_image(self):
        # Resize the image
        resized_image = cv2.resize(self.image, (self.image_width, self.image_height))
        resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        self.image_tk = ImageTk.PhotoImage(Image.fromarray(resized_image))

        # Clear the canvas and place the resized image
        self.image_output.delete('all')
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

    

App()