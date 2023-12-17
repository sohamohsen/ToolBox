import customtkinter as ctk
from tkinter import filedialog
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

        self.data_var = rotation
        self.data_var.trace('w', self.update_text)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.num_label = ctk.CTkLabel(self, text=rotation.get())
        self.num_label.grid(column=1, row=0, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation,
                      from_=min_value,
                      to=max_value).grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    def update_text(self, *args):
        self.num_label.configure(text = f'{round(self.data_var.get(), 2)}')

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

        self.data_var = rotation
        self.data_var.trace('w', self.update_text)

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
    
    def update_text(self, *args):
        self.num_label.configure(text = f'{round(self.data_var.get(), 2)}')

class SlidersPanel(Panel):
    def __init__(self, parent, text1, text2, text3, text4, rotation1, rotation2, rotation3, min_value1, max_value1, min_value2, max_value2, min_value3, max_value3):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 6), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text1).grid(column=0, row=0, sticky='EW')
        ctk.CTkLabel(self, text=text2).grid(column=0, row=1, sticky='W', padx=5)
        
        self.data_var1 = rotation1
        self.data_var1.trace('w', self.update_value1)

        self.num_label1 = ctk.CTkLabel(self, text=rotation1.get())
        self.num_label1.grid(column=1, row=1, sticky='E', padx=5)
        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation1,
                      from_=min_value1,
                      to=max_value1).grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
       
        self.data_var2 = rotation2
        self.data_var2.trace('w', self.update_value2)
        
        ctk.CTkLabel(self, text=text3).grid(column=0, row=3, sticky='W', padx=5)
        self.num_label2 = ctk.CTkLabel(self, text=rotation2.get())
        self.num_label2.grid(column=1, row=3, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation2,
                      from_=min_value2,
                      to=max_value2).grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        self.data_var3 = rotation3
        self.data_var3.trace('w', self.update_value3)

        ctk.CTkLabel(self, text=text4).grid(column=0, row=5, sticky='W', padx=5)
        self.num_label3 = ctk.CTkLabel(self, text=rotation3.get())
        self.num_label3.grid(column=1, row=5, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation3,
                      from_=min_value3,
                      to=max_value3).grid(row=6, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    # Function to round the slider value to the nearest odd number
    def round_to_odd1(self, *args):
        return self.data_var1.get() - (self.data_var1.get() % 2) + 1
    
    def round_to_odd2(self, *args):
        return self.data_var3.get() - (self.data_var3.get() % 2) + 1

    def update_value1(self, *args):
        # Get the slider's value
        current_value = self.round_to_odd1(float(self.data_var1.get()))

        # Set the slider value to the rounded odd number
        self.num_label1.configure(text=f'{current_value}')

    def update_value2(self, *args):
        # print(value)
        self.num_label2.configure(text = f'{round(self.data_var2.get(), 2)}')

    def update_value3(self, *args):
        # Get the slider's value
        current_value = self.round_to_odd2(float(self.data_var3.get()))
        self.num_label3.configure(text=f'{current_value}')

class SliderWithButtonPanel(Panel):
    def __init__(self, parent, slider_text, rotation, min_value, max_value, button_text):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 2), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.data_var = rotation
        self.data_var.trace('w', self.update_text)

        ctk.CTkLabel(self, text=slider_text).grid(column=0, row=0, sticky='W', padx=5)
        self.num_label = ctk.CTkLabel(self, text=rotation.get())
        self.num_label.grid(column=1, row=0, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation,
                      from_=min_value,
                      to=max_value).grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        ctk.CTkButton(self, text=button_text).grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    def update_text(self, *args):
        self.num_label.configure(text=f'{round(float(self.data_var.get()), 2)}')

class Sliders2Panel(Panel):
    def __init__(self, parent, text1, text2, text3, rotation1, rotation2, min_value1, max_value1, min_value2, max_value2):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 4), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text1).grid(column=0, row=0, sticky='EW', padx=5)

        self.data_var1 = rotation1
        self.data_var1.trace('w', self.update_text1)

        ctk.CTkLabel(self, text=text2).grid(column=0, row=1, sticky='W', padx=5)
        self.num_label1 = ctk.CTkLabel(self, text=rotation1.get())
        self.num_label1.grid(column=1, row=1, sticky='E', padx=5)
        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation1,
                      from_=min_value1,
                      to=max_value1).grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        self.data_var2 = rotation2
        self.data_var2.trace('w', self.update_text2)
        
        ctk.CTkLabel(self, text=text3).grid(column=0, row=3, sticky='W', padx=5)
        self.num_label2 = ctk.CTkLabel(self, text=rotation2.get())
        self.num_label2.grid(column=1, row=3, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=rotation2,
                      from_=min_value2,
                      to=max_value2).grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    def update_text1(self, *args):
        # print(value)
        self.num_label1.configure(text = f'{round(self.data_var1.get(), 2)}')

    def update_text2(self, *args):
        # print(value)
        self.num_label2.configure(text = f'{round(self.data_var2.get(), 2)}')

class RevertButton(ctk.CTkButton):
    def __init__ (self, parent, *args):
        super().__init__(master = parent, text = 'Revert', command = self.revert)
        self.pack(side = 'bottom', pady = 10)
        self.args = args

    def revert(self):
        for var, value in self.args:
            var.set(value)

class FileNamePanel(Panel):
    def __init__(self, parent, name_string, file_string):
        super().__init__(parent=parent)

        # Data
        self.file_string = file_string
        self.name_string = name_string
        self.name_string.trace('w', self.update_text)

        # check boxes for file format
        ctk.CTkEntry(self, textvariable=self.name_string).pack(fill='x', padx=20, pady=5)
        frame = ctk.CTkFrame(self, fg_color='transparent')
        jpg_check = ctk.CTkCheckBox(frame, text='jpg', variable = self.file_string,command = lambda: self.click('jpg'), onvalue = 'jpg', offvalue = 'png')
        png_check = ctk.CTkCheckBox(frame, text='png', variable = self.file_string,command = lambda: self.click('png'), onvalue = 'png', offvalue = 'jpg')
        jpg_check.pack(side='left', fill='x', expand=True)
        png_check.pack(side='left', fill='x', expand=True)
        frame.pack(expand=True, fill='x', padx=20)

        # preview text
        self.output = ctk.CTkLabel(self, text='')
        self.output.pack()

    def click(self, value):
        self.file_string.set(value)
        self.update_text()

    def update_text(self, *args):
        if self.name_string.get():
            text = self.name_string.get().replace(' ', '_') + '.' + self.file_string.get()
            self.output.configure(text=text)

class FilePathPanel(Panel):
    def __init__(self, parent, path_string):
        super().__init__(parent=parent)
        self.path_string = path_string

        ctk.CTkButton(self, text = 'Open Explorer', command = self.open_file_dialog).pack(pady = 5)
        ctk.CTkEntry(self, textvariable = self.path_string).pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def open_file_dialog(self):
        self.path_string.set(filedialog.askdirectory())

class SaveButton(ctk.CTkButton):
    def __init__(self, parent, export_image, name_string, file_string, path_string):
        super().__init__(master = parent, text = 'save', command = self.save)
        self.pack(side = 'bottom', pady = 10)

        self.export_image = export_image
        self.name_string = name_string
        self.file_string = file_string
        self.path_string = path_string

    def save(self):
        self.export_image(
                self.name_string.get(),
                self.file_string.get(),
                self.path_string.get()
        )

class OCRButton(ctk.CTkButton):
    def __init__(self, parent, ocr_image, name_string, file_string, path_string):
        super().__init__(master = parent, text = 'ocr', command = self.ocr)
        self.pack(side = 'bottom', pady = 10)

        self.ocr_image = ocr_image
        self.name_string = name_string
        self.file_string = file_string
        self.path_string = path_string

    def ocr(self):
        self.ocr_image(
                self.name_string.get(),
                self.file_string.get(),
                self.path_string.get()
        )
