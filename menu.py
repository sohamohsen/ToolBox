import customtkinter as ctk
from panels import *
import matplotlib.pyplot as plt
import cv2
# from main import *

class Menu(ctk.CTkTabview):
    def __init__(self, parent, pos_var, color_var, effect_var, point_var):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'nsew', pady = 10, padx = 10)

        # tabs
        self.add('Position')
        self.add('Color')
        self.add('Effects')
        self.add('P.P')

        # Widgets
        PositionFrame(self.tab('Position'), pos_var)
        ColorFrame(self.tab('Color'), color_var)
        EffactFrame(self.tab('Effects'), effect_var)
        PointOfProcessingFrame(self.tab('P.P'), point_var)


class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, pos_var):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        # SliderPanel(self, 'TranslateX', pos_var['rotate'], 0, 360)
        # SliderPanel(self, 'TranslateY', pos_var['rotate'], 0, 360)
        SegmentedPanel(self, 'Invert', pos_var['flip'], FLIP_OPTIONS)
        SwSliderPanel(self, 'Translation', pos_var['translation'], -200, 200, (pos_var['translation_sw'], 'X/Y'))
        SliderPanel(self, 'Rotation', pos_var['rotate'], 0, 360)
        SliderPanel(self, 'Zoom', pos_var['zoom'], -5, 5)
        # SwSliderPanel(self, 'DeSkewing', pos_var['deskewing'], -90, 90, (pos_var['deskewing_sw'], 'X/Y'))
        Sliders2Panel(self, 'Skewing', 'X','y', pos_var['deskewing_X'], pos_var['deskewing_Y'], -1, 1, -1, 1)


class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent, color_var):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        SwitchPanel(self, (color_var['grayscale'], 'B/W'), (color_var['invert'], 'Invert'))
        SliderPanel(self, 'Brightness', color_var['brightness'], 0, 5)
        SliderPanel(self, 'Vibrance', color_var['vibrance'], 0, 5)
        SliderWithButtonPanel(self, 'eq', color_var['eq'], 0, 10, 'Show Hist')
                            #  (parent, slider_text, rotation, min_value, max_value, button_text
    


class EffactFrame(ctk.CTkFrame):
    def __init__(self, parent, effect_var):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')
        SegmentedPanel(self, 'Find Edges', effect_var['Find_Edges'], FIND_EDGES_OPTIONS)
        DropDownPanel(self, effect_var['effect'], EFFECT_OPTIONS)
        # SliderPanel(self, 'Blur', effect_var['blur'], 0, 30)
        SlidersPanel(self, 'Low pass filter', 'Averaging','Blur (Gaussian)', 'Median Blurring (Salt & paper)', effect_var['blur_averaging'], effect_var['blur'], effect_var['blur_median'], 0, 15, 0, 30, 0, 15)
        SliderPanel(self, 'Histgram EQ', effect_var['contrast'], 0, 30)
        # SwitchPanel(self, (effect_var['Thresholding_sw'], 'on/off'))
        # SliderPanel(self, 'Thresholding', effect_var['Thresholding'], 0, 255)
        SwSliderPanel(self, 'Thresholding', effect_var['Thresholding'], 0, 255, (effect_var['Thresholding_sw'], 'on/off'))

class PointOfProcessingFrame(ctk.CTkFrame):
    def __init__(self, parent, point_var):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        SliderPanel(self, 'Power transformation', point_var['gamma_corraction'], 0, 3)
        SwitchPanel(self, (point_var['log_value'], 'Logarithmic transformation'))
        SwSliderPanel(self, 'Bit plane slicing', point_var['bit_plane_slicing'], 0, 7, (point_var['bit_plane_slicing_sw'], 'on/off'))
        Sliders2Panel(self, 'Gray level slice', 'Lower threshold','Upper threshold', point_var['lower_threshold'], point_var['higher_threshold'], 0, 255, 0, 255)



