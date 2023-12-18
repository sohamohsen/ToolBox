import customtkinter as ctk
from panels import *
import matplotlib.pyplot as plt
import cv2
# from main import *

class Menu(ctk.CTkTabview):
    def __init__(self, parent, pos_var, color_var, effect_var, point_var, export_image, ocr_image):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'nsew', pady = 10, padx = 10)

        # tabs
        self.add('Position')
        self.add('Color')
        self.add('Effects')
        self.add('P.P')
        self.add('Export')

        # Widgets
        PositionFrame(self.tab('Position'), pos_var)
        ColorFrame(self.tab('Color'), color_var)
        EffactFrame(self.tab('Effects'), effect_var)
        PointOfProcessingFrame(self.tab('P.P'), point_var)
        ExportFrame(self.tab('Export'), export_image, ocr_image)

class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, pos_var):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        # SliderPanel(self, 'TranslateX', pos_var['rotate'], 0, 360)
        # SliderPanel(self, 'TranslateY', pos_var['rotate'], 0, 360)
        SegmentedPanel(self, 'Invert', pos_var['flip'], FLIP_OPTIONS)
        SwSliderPanel(self, 'Translation', pos_var['translation'], -200, 200, (pos_var['translation_sw'], 'X/Y'))
        SliderPanel(self, 'Rotation', pos_var['rotate'], 0, 360)
        SliderPanel(self, 'Zoom', pos_var['zoom'], 0, 1)
        # SwSliderPanel(self, 'DeSkewing', pos_var['deskewing'], -90, 90, (pos_var['deskewing_sw'], 'X/Y'))
        Sliders2Panel(self, 'Skewing', 'X','y', pos_var['deskewing_X'], pos_var['deskewing_Y'], -1, 1, -1, 1)
        RevertButton(self, 
                    (pos_var['flip'], FLIP_OPTIONS[0]),
                    (pos_var['translation'], TRANSLATION_DEFAULT),
                    (pos_var['translation_sw'], TRANSLATION_SW_DEFAULT),
                    (pos_var['rotate'], ROTATE_DEFAULT),
                    (pos_var['zoom'], ZOOM_DEFAULT),
                    (pos_var['deskewing_X'], DESKEWING_DEFAULT),
                    (pos_var['deskewing_Y'], DESKEWING_DEFAULT))

class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent, color_var):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        SwitchPanel(self, (color_var['grayscale'], 'B/W'), (color_var['invert'], 'Invert'))
        SliderPanel(self, 'Brightness', color_var['brightness'], 0, 5)
        SliderPanel(self, 'Vibrance', color_var['vibrance'], 0, 5)
        SliderPanel(self, 'Histgram EQ', color_var['contrast'], 0, 30)
        # SliderWithButtonPanel(self, 'eq', color_var['eq'], 0, 10, 'Show Hist')
        RevertButton(self, 
                    (color_var['brightness'], BRIGHTNESS_DEFAULT),
                    (color_var['grayscale'], GRAYSCALE_DEFAULT),
                    (color_var['invert'], INVERT_DEFAULT),
                    (color_var['vibrance'], VIBRANCE_DEFAULT),
                    (color_var['contrast'], CONTRAST_DEFAULT),
                    (color_var['eq'], CONTRAST_DEFAULT))
    
class EffactFrame(ctk.CTkFrame):
    def __init__(self, parent, effect_var):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')
        SegmentedPanel(self, 'Find Edges', effect_var['Find_Edges'], FIND_EDGES_OPTIONS)
        DropDownPanel(self, effect_var['effect'], EFFECT_OPTIONS)
        SlidersPanel(self, 'Low pass filter', 'Averaging','Blur (Gaussian)', 'Median Blurring (Salt & paper)', effect_var['blur_averaging'], effect_var['blur'], effect_var['blur_median'], 0, 15, 0, 30, 0, 15)
        # SliderPanel(self, 'Blur', effect_var['blur'], 0, 30)
        # SwitchPanel(self, (effect_var['Thresholding_sw'], 'on/off'))
        # SliderPanel(self, 'Thresholding', effect_var['Thresholding'], 0, 255)
        # SwSliderPanel(self, 'Frequency domain enhancement', effect_var['Freq_domain_enhance'], -100, 100, (effect_var['Freq_domain_enhance_sw'], 'on/off'))
        SwSliderPanel(self, 'Thresholding', effect_var['Thresholding'], 0, 255, (effect_var['Thresholding_sw'], 'on/off'))
        RevertButton(self, 
                    (effect_var['Find_Edges'], FIND_EDGES_OPTIONS[0]),
                    (effect_var['effect'], EFFECT_OPTIONS[0]),
                    (effect_var['blur_averaging'], BLUR_DEFAULT),
                    (effect_var['blur'], BLUR_DEFAULT),
                    (effect_var['blur_median'], BLUR_DEFAULT),
                    (effect_var['Thresholding'], THRESHOLDING_DEFAULT),
                    (effect_var['Thresholding_sw'], THRESHOLDING_SW_DEFAULT))

class PointOfProcessingFrame(ctk.CTkFrame):
    def __init__(self, parent, point_var):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        SliderPanel(self, 'Power transformation', point_var['gamma_corraction'], 0, 3)
        SwitchPanel(self, (point_var['log_value'], 'Logarithmic transformation'))
        SwSliderPanel(self, 'Bit plane slicing', point_var['bit_plane_slicing'], 0, 7, (point_var['bit_plane_slicing_sw'], 'on/off'))
        Sliders2Panel(self, 'Gray level slice', 'Lower threshold','Upper threshold', point_var['lower_threshold'], point_var['higher_threshold'], 0, 255, 0, 255)
        RevertButton(self, 
                    (point_var['gamma_corraction'], GAMMA_DEFAULT),
                    (point_var['log_value'], LOG_VALUE_DEFAULT),
                    (point_var['bit_plane_slicing'], PLATE_NUM_DEFAULT),
                    (point_var['bit_plane_slicing_sw'], THRESHOLDING_SW_DEFAULT),
                    (point_var['lower_threshold'], LOWER_THRESHOLD_DEFAULT),
                    (point_var['higher_threshold'], HIGHER_THRESHOLD_DEFAULT))

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, export_image, ocr_image):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

                # data
        self.name_string = ctk.StringVar()
        self.file_string = ctk.StringVar(value = 'jpg')
        self.path_string = ctk.StringVar()

        # widgets
        FileNamePanel(self, self.name_string, self.file_string)
        FilePathPanel(self, self.path_string)
        OCRButton(self, ocr_image, self.name_string, self.file_string, self.path_string)
        SaveButton(self, export_image, self.name_string, self.file_string, self.path_string)
