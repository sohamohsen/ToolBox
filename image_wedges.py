import customtkinter as ctk
from tkinter import filedialog, Canvas
import cv2
from setting import*

class ImageImport(ctk.CTkFrame):

    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=0, sticky='nsew')
        self.import_func = import_func

        ctk.CTkButton(self, text='Choose image', command = self.open_dialog).pack(expand=True)

    def open_dialog(self):
        # Replace this with the logic to choose the image path
        path = filedialog.askopenfile().name
        self.import_func(path)

# class CaptureImage(ctk.CTkFrame):

#     def __init__(self, parent, import_func):
#         super().__init__(master=parent)
#         self.grid(column=0, columnspan=2, row=1, sticky='nsew')
#         self.import_func = import_func

#         ctk.CTkButton(self, text='Capture Image', command = self.capture_image).pack(expand=True)

#     def capture_image(self):
#     # Capture an image from the camera using OpenCV
#         camera = cv2.VideoCapture(0)
#         _, image = camera.read()
#         camera.release()

#     # Convert the captured image to a format compatible with PIL
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         pil_image = Image.fromarray(image)
#         captured_image = pil_image.save("captured_image.png")

#     # Display the captured image
#         self.import_func(captured_image)

class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master = parent, background = BACKGROUND_COLOR, bd = 0, highlightthickness = 0, relief = 'ridge')
        self.grid(row = 0, column = 1, sticky = 'nsew', padx = 10, pady = 10)
        self.bind('<Configure>', resize_image)

class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master = parent, 
            command = close_func,
            text = 'x', 
            text_color = WHITE, 
            fg_color = 'transparent', 
            width = 40, height = 40,
            corner_radius = 0,
            hover_color = CLOSE_RED)
        self.place(relx = 0.99, rely = 0.01, anchor = 'ne')
