import customtkinter as ctk
from setting import *

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.pack(fill='x', pady=4, ipady=8)

class SliderPanel(Panel):
    def __init__(self, parent, text, rotation, min_value, max_value):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.num_label = ctk.CTkLabel(self, text=rotation.get())
        self.num_label.grid(column=1, row=0, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation,
                      from_=min_value,
                      to=max_value,
                      command=self.update_text).grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    def update_text(self, value):
        # print(value)
        self.num_label.configure(text = f'{round(value, 2)}')

class SegmentedPanel(Panel):
    def __init__(self, parent, text, data_var, options):
        super().__init__(parent)

        ctk.CTkLabel(self, text = text). pack()
        ctk.CTkSegmentedButton(self, variable = data_var, values = options).pack(expand = True, fill = 'both', padx = 4, pady = 4)

class SwitchPanel(Panel):
    def __init__(self, parent, *args):
        super().__init__(parent)

        for var, text in args:
            switch = ctk.CTkSwitch(self, text = text, variable = var, button_color = BLUE, fg_color = SLIDER_BG)
            switch.pack(side = 'left', expand = True, fill = 'both', padx = 5, pady = 5)

class DropDownPanel(ctk.CTkOptionMenu):
     def __init__(self, parent, data_var, options):
        super().__init__(
            master = parent,
            values = options,
            fg_color = DARK_GREY,
            button_color = DROPDOWN_MAIN_COLOR,
            button_hover_color = DROPDOWN_HOVER_COLOR,
            dropdown_fg_color = DROPDOWN_MENU_COLOR, 
            variable = data_var)
        self.pack(fill = 'x', pady = 4)

class SwSliderPanel(Panel):
    def __init__(self, parent, text, rotation, min_value, max_value, *args):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 2), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.num_label = ctk.CTkLabel(self, text=rotation.get())
        self.num_label.grid(column=1, row=0, sticky='E', padx=5)
        
        for var, text in args:
            switch = ctk.CTkSwitch(self, text = text, variable = var, button_color = BLUE, fg_color = SLIDER_BG).grid(column=0, row=1, sticky='W', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation,
                      from_=min_value,
                      to=max_value,
                      command=self.update_text).grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
    
    def update_text(self, value):
        # print(value)
        self.num_label.configure(text = f'{round(value, 2)}')


class SlidersPanel(Panel):
    def __init__(self, parent, text1, text2, text3, text4, rotation1, rotation2, rotation3, min_value1, max_value1, min_value2, max_value2, min_value3, max_value3):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 6), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text1).grid(column=0, row=0, sticky='EW')

        ctk.CTkLabel(self, text=text2).grid(column=0, row=1, sticky='W', padx=5)
        
        self.num_label1 = ctk.CTkLabel(self, text=rotation1.get())
        self.num_label1.grid(column=1, row=1, sticky='E', padx=5)
        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation1,
                      from_=min_value1,
                      to=max_value1,
                      command=self.update_value1).grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ctk.CTkLabel(self, text=text3).grid(column=0, row=3, sticky='W', padx=5)
        self.num_label2 = ctk.CTkLabel(self, text=rotation2.get())
        self.num_label2.grid(column=1, row=3, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation2,
                      from_=min_value2,
                      to=max_value2,
                      command=self.update_value2).grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        ctk.CTkLabel(self, text=text4).grid(column=0, row=5, sticky='W', padx=5)
        self.num_label3 = ctk.CTkLabel(self, text=rotation3.get())
        self.num_label3.grid(column=1, row=5, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation3,
                      from_=min_value3,
                      to=max_value3,
                      command=self.update_value3).grid(row=6, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    def update_value2(self, value):
        # print(value)
        self.num_label2.configure(text = f'{round(value, 2)}')

    # Function to round the slider value to the nearest odd number
    def round_to_odd(self, value):
        return value - (value % 2) + 1

    def update_value1(self, value):
        # Get the slider's value
        current_value = self.round_to_odd(float(value))

        # Set the slider value to the rounded odd number
        self.num_label1.configure(text=f'{current_value}')

    def update_value3(self, value):
        # Get the slider's value
        current_value = self.round_to_odd(float(value))
        self.num_label3.configure(text=f'{current_value}')


class SliderWithButtonPanel(Panel):
    def __init__(self, parent, slider_text, rotation, min_value, max_value, button_text):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 2), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=slider_text).grid(column=0, row=0, sticky='W', padx=5)
        self.num_label = ctk.CTkLabel(self, text=rotation.get())
        self.num_label.grid(column=1, row=0, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation,
                      from_=min_value,
                      to=max_value,
                      command=self.update_text).grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        ctk.CTkButton(self, text=button_text).grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    def update_text(self, value):
        self.num_label.configure(text=f'{round(float(value), 2)}')


class Sliders2Panel(Panel):
    def __init__(self, parent, text1, text2, text3, rotation1, rotation2, min_value1, max_value1, min_value2, max_value2):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 4), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text1).grid(column=0, row=0, sticky='EW', padx=5)

        ctk.CTkLabel(self, text=text2).grid(column=0, row=1, sticky='W', padx=5)
        
        self.num_label = ctk.CTkLabel(self, text=rotation1.get())
        self.num_label.grid(column=1, row=1, sticky='E', padx=5)
        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation1,
                      from_=min_value1,
                      to=max_value1,
                      command=self.update_text).grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ctk.CTkLabel(self, text=text3).grid(column=0, row=3, sticky='W', padx=5)
        self.num_label = ctk.CTkLabel(self, text=rotation2.get())
        self.num_label.grid(column=1, row=3, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation2,
                      from_=min_value2,
                      to=max_value2,
                      command=self.update_text).grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    def update_text(self, value):
        # print(value)
        self.num_label.configure(text = f'{round(value, 2)}')

    # Function to round the slider value to the nearest odd number
    def round_to_odd(self, value):
        return value - (value % 2) + 1

    def update_value(self, value):
        # Get the slider's value
        current_value = self.round_to_odd(float(value))

        # Set the slider value to the rounded odd number
        self.num_label.configure(text=f'{current_value}')


