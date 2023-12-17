import cv2
import numpy as np
import customtkinter as ctk
import pytesseract
import matplotlib.pyplot as plt

from image_wedges import *
from PIL import Image, ImageTk
from menu import Menu

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
            'deskewing_X': ctk.DoubleVar(value=DESKEWING_DEFAULT),
            'deskewing_Y': ctk.DoubleVar(value=DESKEWING_DEFAULT),
            'flip': ctk.StringVar(value=FLIP_OPTIONS[0])
        }
        self.color_var = {
            'brightness': ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'grayscale': ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            'invert': ctk.BooleanVar(value=INVERT_DEFAULT),
            'eq': ctk.IntVar(value=CONTRAST_DEFAULT),  # New contrast parameter
            'hist': ctk.BooleanVar(value=HIST_BUTTON_DEFAULT),
            'contrast': ctk.IntVar(value=CONTRAST_DEFAULT),  # New contrast parameter
            'vibrance': ctk.DoubleVar(value=VIBRANCE_DEFAULT)
        }
        self.effect_var = {
            'blur': ctk.DoubleVar(value=BLUR_DEFAULT),
            'blur_averaging': ctk.IntVar(value=BLUR_DEFAULT),
            'blur_median': ctk.IntVar(value=BLUR_DEFAULT),
            'Thresholding_sw': ctk.BooleanVar(value=THRESHOLDING_SW_DEFAULT),
            'Thresholding': ctk.DoubleVar(value=THRESHOLDING_DEFAULT),
            'Freq_domain_enhance': ctk.DoubleVar(value=FREQ_DOMAIN_ENHANCE_DEFALT),
            'Freq_domain_enhance_sw': ctk.BooleanVar(value=THRESHOLDING_SW_DEFAULT),
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0]),
            'Find_Edges': ctk.StringVar(value=FIND_EDGES_OPTIONS[0])
        }
        self.point_var = {
            'gamma_corraction': ctk.DoubleVar(value=GAMMA_DEFAULT),
            'bit_plane_slicing': ctk.IntVar(value=PLATE_NUM_DEFAULT),
            'bit_plane_slicing_sw': ctk.BooleanVar(value=THRESHOLDING_SW_DEFAULT),
            'log_value': ctk.IntVar(value=LOG_VALUE_DEFAULT),
            'lower_threshold': ctk.IntVar(value=LOWER_THRESHOLD_DEFAULT),
            'higher_threshold': ctk.IntVar(value=HIGHER_THRESHOLD_DEFAULT)
        }
        # tracing
        combined_vars = list(self.pos_var.values()) + list(self.color_var.values()) + list(self.effect_var.values()) + list(self.point_var.values())
        for var in combined_vars:
            var.trace('w', self.manipulate_image)

    def emboss_filter(image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply the emboss kernel
        emboss_kernel = np.array([[0, -1, -1],
                                [1,  0, -1],
                                [1,  1,  0]])
        embossed_image = cv2.filter2D(gray, -1, emboss_kernel)

        # Convert back to BGR for display purposes
        embossed_image = cv2.cvtColor(embossed_image, cv2.COLOR_GRAY2BGR)

        return embossed_image

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

        # Skewing
            # skew_factor_x = 0.5  # Adjust the skew factor for X-axis (positive values tilt right, negative values tilt left)
            # skew_factor_y = 0.2  # Adjust the skew factor for Y-axis (positive values tilt down, negative values tilt up)

            # Define the skew matrix
            skew_matrix = np.float32([[1, self.pos_var['deskewing_X'].get(), 0], [self.pos_var['deskewing_Y'].get(), 1, 0]])

            # Apply the skew transformation
            self.image = cv2.warpAffine(self.image, skew_matrix, (width, height), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))


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

        # Histgram equliztion
        contrast_value = float(self.color_var['contrast'].get())  # Get the blur value
        if contrast_value > 0:
            # Perform histogram equalization based on slider value
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.equalizeHist(self.image)
            alpha = self.color_var['contrast'].get() / 10.0  # Scale the slider value
            self.image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=0)
            
        # Blur Gaussian
        blur_value = float(self.effect_var['blur'].get())  # Get the blur value
        if blur_value > 0:
            # Adjust filter size based on image size and blur strength
            filter_size = int(min(5 * blur_value, 31))  # Ensure the maximum size is 31
            filter_size = filter_size if filter_size % 2 != 0 else filter_size + 1  # Ensure the size is odd
            self.image = cv2.GaussianBlur(self.image, (filter_size, filter_size), 0)

        # Filters
        match self.effect_var['effect'].get():
            case 'Emboss': 
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                emboss_kernel = np.array([[0, -1, -1],
                                          [1,  0, -1],
                                          [1,  1,  0]])
                self.image = cv2.filter2D(self.image, -1, emboss_kernel)
                self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
            
            case 'Histgoram': 
                # Check if the image is grayscale or colored
                if len(self.image.shape) < 3 or self.image.shape[2] == 1:
                    # Grayscale image
                    hist = cv2.calcHist([self.image], [0], None, [256], [0, 256])
                    plt.plot(hist, color='black')
                    plt.title('Grayscale Histogram')
                    plt.xlabel('Pixel value')
                    plt.ylabel('Frequency')
                    plt.show()
                else:
                    # Colored image
                    colors = ('b', 'g', 'r')
                    for i, col in enumerate(colors):
                        hist = cv2.calcHist([self.image], [i], None, [256], [0, 256])
                        plt.plot(hist, color=col)
                        plt.xlim([0, 256])

                    plt.title('Color Histogram')
                    plt.xlabel('Pixel value')
                    plt.ylabel('Frequency')
                    plt.show()

        # Create an averaging kernel
        kernel_size = float(self.effect_var['blur_averaging'].get())  # Get the blur value
        kernel_size = int(kernel_size)  # Convert to integer
        # Ensure the kernel size is odd
        kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)

        # Apply the filter using OpenCV filter2D function
        self.image = cv2.filter2D(self.image, -1, kernel)
        self.image = np.uint8(np.absolute(self.image))
        
        if self.effect_var['blur_median'].get() < 3:
            pass
        else:
            median_kernel_size = int(self.effect_var['blur_median'].get())  # Get the blur value
            median_kernel_size = median_kernel_size if median_kernel_size % 2 != 0 else median_kernel_size + 1
            self.image = cv2.medianBlur(self.image, median_kernel_size)
            # self.image = np.uint8(np.absolute(self.image))

        # # Contrast adjustment (OpenCV equivalent)
        # contrast_value = self.color_var['contrast'].get()
        # self.image = cv2.addWeighted(self.image, 1 + contrast_value * 0.01, self.image, -contrast_value * 0.01, 0)

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

        # Power Transformation
        gamma = self.point_var['gamma_corraction'].get()
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        # Apply gamma transformation
        self.image = cv2.LUT(self.image, table)

        # Log Tran
        # Apply the logarithmic transformation
        if self.point_var['log_value'].get():
            c = 255 / np.log(1 + np.max(self.image))
            log_transformed = c * np.log(1 + self.image)
            # Convert floating-point pixels to unsigned 8-bit integer
            self.image = np.uint8(log_transformed)

        if self.point_var['bit_plane_slicing_sw'].get():
            plane = self.point_var['bit_plane_slicing'].get()
            transformed_image = (self.image >> plane) & 1
            transformed_image *= 255  # Scale the image values to 0-255 for display
            self.image = np.uint8(transformed_image)

        # # Fraquance domain enhancement
        # if self.effect_var['Freq_domain_enhance_sw'].get():
        #     pass
        if self.color_var['grayscale'].get():
            lower_threshold = self.point_var['lower_threshold'].get()
            upper_threshold = self.point_var['higher_threshold'].get()
            mask = cv2.inRange(self.image, lower_threshold, upper_threshold)
            self.image = cv2.bitwise_and(self.image, self.image, mask=mask) 
        else: 
            pass            

        self.place_image()

    def reset_default(self):
        pass

    def on_hist_click(self):
        # Convert the image to grayscale if it's a color image
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # Compute the histogram using OpenCV
            histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

            # Plot the histogram using Matplotlib
            plt.figure(figsize=(8, 6))
            plt.plot(histogram, color='black')
            plt.title('Grayscale Histogram')
            plt.xlabel('Pixel value')
            plt.ylabel('Frequency')
            plt.show()

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
        self.menu = Menu(self, self.pos_var, self.color_var, self.effect_var, self.point_var, self.export_image, self.ocr_image)

        self.image_output.grid(row=0, column=1, sticky='nsew')
        self.close_button.place(x=0, y=0)  # Adjust the position of the close button

    def close_edit(self):
        # hide the image and the close button
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        self.init_parameters()


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

    def export_image(self, name, file, path):
        export_string = f'{path}/{name}.{file}'
        print(export_string)
        cv2.imwrite(export_string, self.image)

    def ocr_image(self, name, file, path):
        export_string = f'{path}/{name}.{file}'

        # Read image from which text needs to be extracted
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        # Specify structure shape and kernel size. 
        # Kernel size increases or decreases the area 
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect 
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                        cv2.CHAIN_APPROX_NONE)

        # Creating a copy of image
        im2 = self.image.copy()

        # A text file is created and flushed
        file = open("recognized.txt", "w+")
        file.write("")
        file.close()

        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            
            # Open the file in append mode
            file = open("recognized.txt", "a")
            
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            
            # Appending the text into file
            file.write(text)
            file.write("\n")
            
            # Close the file
            file.close
        print(export_string)
    def export_image(self, name, file, path):
        export_string = f'{path}/{name}.{file}'
        print(export_string)
        cv2.imwrite(export_string, self.image)

    def ocr_image(self, name, file, path):
        export_string = f'{path}/{name}.{file}'

        # Read image from which text needs to be extracted
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        # Specify structure shape and kernel size. 
        # Kernel size increases or decreases the area 
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect 
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                        cv2.CHAIN_APPROX_NONE)

        # Creating a copy of image
        im2 = self.image.copy()

        # A text file is created and flushed
        file = open("recognized.txt", "w+")
        file.write("")
        file.close()

        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            
            # Open the file in append mode
            file = open("recognized.txt", "a")
            
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            
            # Appending the text into file
            file.write(text)
            file.write("\n")
            
            # Close the file
            file.close
        print(export_string)




App()