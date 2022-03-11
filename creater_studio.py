"""
GifCreator Project V1

"""

import tkinter
import os
import glob
import threading
from PIL import Image, ImageColor
from tkinter import colorchooser
from tkinter import filedialog
import Ctkinter

__author__ = 'Elias Rauth'
__date__ = '01.11.2021'
__completed__ = '--.--.----'
__work_time__ = 'still working'
__version__ = '1.0'
__licence__ = 'opensource(common licenced)'

Window_COLOR = "gray30"
GifCreator_VERSION = "GifCreator 1.0"

SelectedColor = "cyan3"
PressedColor = "SpringGreen3"
DeselectedColor = "gray90"


class GifCreatorStartWindow:
    def __init__(self):
        self.master = None
        self.start_window = None
        self.colorchooser_active = False
        self.start_activated = False
        self.open_creation = False
        self.chosen_shape = 0
        self.num_picture_buttons = 0
        self.actual_picture = 0
        # ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # Start-Window #####################################################################################################
    def title_bar(self):
        logo = tkinter.Frame(self.start_window.get_canvas(), bg=Window_COLOR)
        logo_size = 65
        logo_can = Ctkinter.CCanvas(logo, size=(logo_size, logo_size))
        logo_can.create_image(corner="angular", width=logo_size, height=logo_size,
                              pos=(int(logo_size / 2), int(logo_size / 2)),
                              image_path="thump.png", transparent=False, read_from_path=True)
        message = tkinter.Label(logo, text=GifCreator_VERSION, bg="azure", font="Arial")
        logo_can.grid(row=0, column=0)
        message.grid(row=0, column=1)
        logo.place(x=70, y=2)

        pixel_logo = Ctkinter.CCanvas(master=self.master, bg='gray12', size=(350, 81))
        pixel_logo.create_image(corner="angular", width=227, height=41,
                                pos=(227, 41), image_path="logo_pixel_white.png",
                                transparent=True, read_from_path=True)
        pixel_logo.place(x=1150, y=760)

    def creation(self):
        info = tkinter.Label(self.start_window.get_canvas(), text="Name your creation:",
                             bg=Window_COLOR, fg="white")
        self.creation_name = tkinter.Entry(self.start_window.get_canvas(), width=30)

        info.place(x=20, y=80)
        self.creation_name.place(x=20, y=110)
        self.open_button = tkinter.Button(self.start_window.get_canvas(), text="Open", height=1, width=5,
                                          command=self.open_button_pressed)
        self.open_button.place(x=220, y=110)

    def open_button_pressed(self):
        # ToDone Rewrite open-function to directory-structur
        try:
            folder = filedialog.askdirectory(title="Open Project")
            # print("folder: ", folder)
        except FileNotFoundError:
            return

        # Get sizefactor from first savefile
        save_file_location = folder + '/0.txt'
        # print("file for shape: ", save_file_location) # debugging
        try:
            save_file = open(save_file_location, "r")
        except FileNotFoundError:
            return
        content = save_file.readlines()
        self.chosen_shape = (int(content[0]))
        # print("read sizefactor: ", self.chosen_shape) # debugging
        save_file.close()
        self.file_location = folder
        # print("self.file_location: ", self.file_location) # debugging

        # Get the colorlist from first savefile
        save_color_list = content[1].split(",")
        # print(save_color_list)

        for i in range(0, 10):
            self.color_buttons[i].CButton.itemconfig(self.color_buttons[i].polygon, fill=save_color_list[i])
            self.color_buttons[i].bg = save_color_list[i]
            self.color_buttons_colors[i] = save_color_list[i]

        # Get the right buttons
        self.open_creation = True
        self.start_editing(self.chosen_shape)

        # Edit edit_buttons_colors
        for _ in glob.glob(folder + '/*.txt'):
            # print(self.num_picture_buttons) # debugging
            self.read_picture(self.num_picture_buttons)
            self.create_picture_button_command()
        self.actual_picture = self.num_picture_buttons - 1
        # print("ende open: ", self.num_picture_buttons) # debugging

        # Disable the Start-Buttons
        self.button_8x8.config(state="disabled")
        self.button_16x16.config(state="disabled")
        self.button_32x32.config(state="disabled")
        self.button_64x64.config(state="disabled")
        self.open_button.config(state="disabled")

        self.start_activated = True
        self.start_button_label.config(text="Save")
        self.start_button_label.place_configure(x=60, y=10)
        self.creation_name.insert(0,
                                  self.file_location.split("/")[len(self.file_location.split("/")) - 1].split(".")[0])

        """
        file_location = filedialog.askdirectory(title="Open Project")
        print("open folder: ", file_location)
        files = os.listdir(file_location)
        print(files)
        self.filename = file_location
        for file in os.listdir(file_location):
            save_file = file_location + '/' + file
            print("files in for-loop: ", save_file)
            save_file = open(save_file, "r")

            content = save_file.readlines()
            # Take sizefactor from savefile
            self.chosen_shape = (int(content[0]))
            save_file.close()

        print("read form: ", self.chosen_shape)
        self.start_activated = True
        self.start_editing(self.chosen_shape)
        self.read_picture(self.num_picture_buttons)
        # self.creation_name.insert(0, self.filename.split("/")[len(self.filename.split("/")) - 1].split(".")[0])
        """
        """
        old function:
        try:
            file = filedialog.askopenfilename(title="Open Project", filetypes=[("text files", "*.txt"), ])
            savefile = open(file, "r")
            content = savefile.readlines()
            # Take sizefactor from savefile
            self.chosen_shape = (int(content[0]))
            self.start_editing(self.chosen_shape)
            self.start_activated = True

            self.filename = file
            print(self.filename)
            self.creation_name.insert(0, self.filename.split("/")[len(self.filename.split("/"))-1].split(".")[0])

            # print(content[1])
            edit_color_list = content[2].split(",")
            # print(edit_color_list)

            for i in range(0, self.chosen_shape * self.chosen_shape):
                self.edit_buttons[i].CButton.itemconfig(self.edit_buttons[i].polygon, fill=edit_color_list[i])
                self.edit_buttons[i].bg = edit_color_list[i]
                self.edit_buttons_colors[i] = edit_color_list[i]

            save_color_list = content[1].split(",")
            # print(save_color_list)

            for i in range(0, 10):
                self.color_buttons[i].CButton.itemconfig(self.color_buttons[i].polygon, fill=save_color_list[i])
                self.color_buttons[i].bg = save_color_list[i]
                self.color_buttons_colors[i] = save_color_list[i]

            savefile.close()

            self.button_8x8.config(state="disabled")
            self.button_16x16.config(state="disabled")
            self.button_32x32.config(state="disabled")
            self.button_64x64.config(state="disabled")
            self.open_button.config(state="disabled")

            self.start_button_label.config(text="Save")
            self.start_button_label.place_configure(x=60, y=10)

        except FileNotFoundError:
            print("send return")
            return
        """
    """
    def checkbox_public(self):
        self.var = tkinter.BooleanVar()
        self.var.set(True)
        info = tkinter.Label(self.start_window.get_canvas(), text="Do you want to share your creation with others?",
                             bg=Window_COLOR, fg="white")
        public = tkinter.Checkbutton(self.start_window.get_canvas(), text="public", bg=Window_COLOR, fg="white",
                                     selectcolor=Window_COLOR,
                                     activebackground=Window_COLOR, activeforeground="white", variable=self.var,
                                     command=lambda: print(self.var.get()))
        info.place(x=25, y=150)
        public.place(x=120, y=175)
    """

    def creation_size(self):
        info = tkinter.Label(self.start_window.get_canvas(), text="Choose a formfactor:",
                             bg=Window_COLOR, fg="white")
        buttons = tkinter.Frame(self.start_window.get_canvas(), bg=Window_COLOR)
        self.button_8x8 = tkinter.Button(buttons, text="8 x 8", height=1, width=5, activebackground=PressedColor,
                                         command=self.button_8x8_pressed, bg=DeselectedColor)
        self.button_16x16 = tkinter.Button(buttons, text="16 x 16", height=1, width=5, activebackground=PressedColor,
                                           command=self.button_16x16_pressed, bg=DeselectedColor)
        self.button_32x32 = tkinter.Button(buttons, text="32 x 32", height=1, width=5, activebackground=PressedColor,
                                           command=self.button_32x32_pressed, bg=DeselectedColor)
        self.button_64x64 = tkinter.Button(buttons, text="64 x 64", height=1, width=5, activebackground=PressedColor,
                                           command=self.button_64x64_pressed, bg=DeselectedColor)

        self.button_8x8.grid(row=0, column=0)
        self.button_16x16.grid(row=0, column=1)
        self.button_32x32.grid(row=1, column=0)
        self.button_64x64.grid(row=1, column=1)

        info.place(x=20, y=160)
        buttons.place(x=95, y=200)

    def startbutton(self):
        """
        info = tkinter.Label(self.start_window.get_canvas(), text="Do you want to start editing?", bg=Window_COLOR,
                             fg="white")
        """
        start_button = Ctkinter.CButton(self.start_window, height=40, width=150, rounded_corners="rounded",
                                        bg="cyan3", highlight_color="cyan2", pressing_color="cyan3",
                                        command=self.start_button_pressed)

        self.start_button_label = tkinter.Label(start_button.get_canvas(), text="Start editing", fg="gray15",
                                                bg="cyan3", font=("Helvetica", 10))
        start_button.set_button_atributes(self.start_button_label, None)
        self.start_button_label.place(x=40, y=10)
        # info.place(x=65, y=280)
        start_button.place(x=65, y=280)

    def start_button_pressed(self):
        if self.start_activated is False:
            # print("Start pressed")
            if self.chosen_shape == 0 and self.creation_name.get() == '':
                pass
            else:
                t = threading.Thread(target=self.start_editing(self.chosen_shape))
                t.start()
                # self.start_editing(self.chosen_shape)
                self.button_8x8.config(state="disabled")
                self.button_16x16.config(state="disabled")
                self.button_32x32.config(state="disabled")
                self.button_64x64.config(state="disabled")
                self.start_button_label.config(text="Save")
                self.start_button_label.place_configure(x=60, y=10)
                self.start_activated = True

        else:
            self.save_picture(self.actual_picture)

    def save_picture(self, picture):
        # ToDo Save and Read Colors in own file per project
        print("saving in: ", self.file_location, picture)
        save_file = open(self.file_location + '/' + str(picture) + ".txt", "w")
        # print("in save_picture_function:", self.edit_buttons_colors)
        # print(self.color_buttons_colors)
        save_file.write(str(self.chosen_shape) + "\n")
        for color in self.color_buttons_colors:
            save_file.write(color + ",")
        save_file.write("\n")
        for color in self.edit_buttons_colors:
            save_file.write(color + ",")
        save_file.close()

    def read_picture(self, picture):
        # ToDone Read Pictures from created folder
        try:
            save_file = open(self.file_location + '/' + str(picture) + ".txt", "r")

            content = save_file.readlines()

            # print(content[1])
            edit_color_list = content[2].split(",")
            # print(edit_color_list)

            for i in range(0, self.chosen_shape * self.chosen_shape):
                self.edit_buttons[i].CButton.itemconfig(self.edit_buttons[i].polygon, fill=edit_color_list[i])
                self.edit_buttons[i].bg = edit_color_list[i]
                self.edit_buttons_colors[i] = edit_color_list[i]

        except FileNotFoundError:
            pass
        """
        save_color_list = content[1].split(",")
        # print(save_color_list)

        for i in range(0, 10):
            self.color_buttons[i].CButton.itemconfig(self.color_buttons[i].polygon, fill=save_color_list[i])
            self.color_buttons[i].bg = save_color_list[i]
            self.color_buttons_colors[i] = save_color_list[i]
        """

    def button_8x8_pressed(self):
        self.button_8x8.config(bg=SelectedColor)
        self.button_16x16.config(bg=DeselectedColor)
        self.button_32x32.config(bg=DeselectedColor)
        self.button_64x64.config(bg=DeselectedColor)
        self.chosen_shape = 8

    def button_16x16_pressed(self):
        self.button_8x8.config(bg=DeselectedColor)
        self.button_16x16.config(bg=SelectedColor)
        self.button_32x32.config(bg=DeselectedColor)
        self.button_64x64.config(bg=DeselectedColor)
        self.chosen_shape = 16

    def button_32x32_pressed(self):
        self.button_8x8.config(bg=DeselectedColor)
        self.button_16x16.config(bg=DeselectedColor)
        self.button_32x32.config(bg=SelectedColor)
        self.button_64x64.config(bg=DeselectedColor)
        self.chosen_shape = 32

    def button_64x64_pressed(self):
        self.button_8x8.config(bg=DeselectedColor)
        self.button_16x16.config(bg=DeselectedColor)
        self.button_32x32.config(bg=DeselectedColor)
        self.button_64x64.config(bg=SelectedColor)
        self.chosen_shape = 64

    # Edit-Window ######################################################################################################
    def edit_field(self):
        self.edit_canvas = Ctkinter.CCanvas(master=self.master, size=(800, 800), max_rad=15, bg="gray15")
        self.edit_canvas.place(x=20, y=20)

    def start_editing(self, size_factor):
        if self.creation_name.get() != '':
            self.file_location = 'Creations/' + self.creation_name.get()
        try:
            os.mkdir(self.file_location)
        except FileExistsError:
            pass
        self.create_picture_buttons()
        # Buttons
        edit_button_frame = tkinter.Frame(self.edit_canvas.get_canvas(), bg="gray15")
        self.edit_buttons = []
        self.edit_buttons_colors = []

        if size_factor == 8:
            x = 0
            y = 0
            for i in range(0, 64):
                self.edit_buttons_colors.append("gray")
                self.edit_buttons.append(Ctkinter.CButton(edit_button_frame, height=60, width=60,
                                                          rounded_corners='angular', bg="gray",
                                                          command=lambda index=i: self.edit_button_command(index)))
                self.edit_buttons[i].grid(row=y, column=x, pady=0, padx=0)
                x += 1
                if x == 8:
                    y += 1
                    x = 0
            edit_button_frame.place(x=150, y=140)

        if size_factor == 16:
            x = 0
            y = 0
            for i in range(0, 16 * 16):
                self.edit_buttons_colors.append("gray")
                self.edit_buttons.append(Ctkinter.CButton(edit_button_frame, height=45, width=45,
                                                          rounded_corners='angular', bg="gray",
                                                          command=lambda index=i: self.edit_button_command(index)))
                self.edit_buttons[i].grid(row=y, column=x, pady=0, padx=0)
                x += 1
                if x == 16:
                    y += 1
                    x = 0
            edit_button_frame.place(x=25, y=25)

        if size_factor == 32:
            x = 0
            y = 0
            for i in range(0, 32 * 32):
                self.edit_buttons_colors.append("gray")
                self.edit_buttons.append(Ctkinter.CButton(edit_button_frame, height=22, width=22,
                                                          rounded_corners='angular', bg="gray",
                                                          command=lambda index=i: self.edit_button_command(index)))
                self.edit_buttons[i].grid(row=y, column=x, pady=0, padx=0)
                x += 1
                if x == 32:
                    y += 1
                    x = 0
            edit_button_frame.place(x=16, y=16)

        if size_factor == 64:
            x = 0
            y = 0
            for i in range(0, 64 * 64):
                self.edit_buttons_colors.append("gray")
                self.edit_buttons.append(Ctkinter.CButton(edit_button_frame, height=10, width=10,
                                                          rounded_corners='angular', bg="gray",
                                                          command=lambda index=i: self.edit_button_command(index)))
                self.edit_buttons[i].grid(row=y, column=x, pady=0, padx=0)
                x += 1
                if x == 64:
                    y += 1
                    x = 0
            edit_button_frame.place(x=16, y=16)

        if not self.open_creation:
            self.create_picture_button_command()

    def edit_button_command(self, index):
        # print(self.actuall_color)
        self.edit_buttons[index].CButton.itemconfig(self.edit_buttons[index].polygon, fill=self.actuall_color)
        self.edit_buttons[index].bg = self.actuall_color
        self.edit_buttons_colors[index] = self.actuall_color

    # Color-Window #####################################################################################################
    def color_field(self):
        self.color_canvas = Ctkinter.CCanvas(master=self.master, size=(300, 300), corners='rounded', max_rad=30,
                                             bg=Window_COLOR)
        self.color_canvas.place(x=1220, y=450)
        ###
        color_label = tkinter.Label(self.color_canvas.get_canvas(), text="Colors", bg=Window_COLOR, fg="white",
                                    font=('Arial', 15))
        color_label.place(x=120, y=5)
        ###
        self.picker_button = Ctkinter.CButton(self.color_canvas,
                                              text="Colorpicker", height=40, width=150, rounded_corners="rounded",
                                              bg="green3", fg="gray15", highlight_color="green2",
                                              pressing_color="green3", outline=("white", 2), command=self.pickermode)
        self.picker_button.place(x=75, y=45)
        ###
        current_color_label = tkinter.Label(self.color_canvas.get_canvas(),
                                            text="Current Color", bg=Window_COLOR, fg="white")
        current_color_label.place(x=110, y=100)
        ###
        self.current_color_can = Ctkinter.CCanvas(self.color_canvas,
                                                  bg='grey', size=(60, 20))
        self.current_color_can.place(x=120, y=125)
        ###
        color_button_frame = tkinter.Frame(self.color_canvas.get_canvas(), bg=Window_COLOR)
        self.color_buttons_colors = []
        self.color_buttons = []

        for i in range(0, 10):
            self.color_buttons_colors.append("gray")
            self.color_buttons.append(Ctkinter.CButton(color_button_frame, height=22, width=22, rounded_corners='round',
                                                       bg="gray",
                                                       command=lambda index=i: self.color_button_command(index)))
            self.color_buttons[i].grid(row=0, column=i, pady=5, padx=0)

        color_button_frame.place(x=30, y=170)

    def pickermode(self):
        if self.colorchooser_active is False:
            self.picker_button._change_outline("blue")
            self.colorchooser_active = True
        else:
            self.picker_button._change_outline("white")
            self.colorchooser_active = False

    def color_button_command(self, index):
        if self.colorchooser_active is True:
            self.actuall_color = self.colorchoose()
            # print(self.actuall_color)
            self.color_buttons[index].CButton.itemconfig(self.color_buttons[index].polygon, fill=self.actuall_color)
            self.color_buttons[index].bg = self.actuall_color
            self.color_buttons_colors[index] = self.actuall_color
        else:
            self.current_color_can.config(bg=self.color_buttons[index].bg)
            self.actuall_color = self.color_buttons[index].bg

    def colorchoose(self):
        chosen_color = colorchooser.askcolor()
        return chosen_color[1]

    # Picture-Window ###################################################################################################
    def picture_field(self):
        self.picture_buttons = []

        self.picture_canvas = Ctkinter.CCanvas(master=self.master, size=(300, 500), corners='rounded', max_rad=30,
                                               bg=Window_COLOR)
        self.picture_canvas.place(x=870, y=50)
        ###
        picture_label = tkinter.Label(self.picture_canvas.get_canvas(), text="Pictures", bg=Window_COLOR, fg="white",
                                      font=('Arial', 15))
        picture_label.place(x=110, y=5)
        ###

    def create_picture_buttons(self):
        add_picture_button = Ctkinter.CButton(self.picture_canvas, text="Add Picture", height=40, width=150,
                                              rounded_corners='rounded',
                                              bg="firebrick3", fg="black", highlight_color="firebrick2",
                                              pressing_color="firebrick3",
                                              command=self.create_picture_button_command)
        add_picture_button.place(x=70, y=45)
        ###
        self.picture_button_frame = Ctkinter.CCanvas(self.picture_canvas.get_canvas(), size=(280, 390),
                                                     bg=Window_COLOR)

        """
        for x in range(0, 8):
            self.picture_buttons.append(Ctkinter.CButton(self.picture_button_frame, height=40, width=150,
                                                         rounded_corners='rounded', bg="gray", text="Picture " + str(x),
                                                         command=lambda index=x: self.picture_button_pressed(index)))
            self.picture_buttons[x].grid(row=x, column=0, pady=0, padx=5)
        """
        self.picture_button_frame.place(x=10, y=98)

    def create_picture_button_command(self):
        # print(self.num_picture_buttons, "of create_picture_button_pressed")
        self.picture_buttons.append(Ctkinter.CButton(self.picture_button_frame,
                                                     height=40, width=150,
                                                     rounded_corners='rounded', bg="gray",
                                                     text="Picture " + str(self.num_picture_buttons),
                                                     command=lambda index=self.num_picture_buttons:
                                                     self.picture_button_command(index)))
        self.picture_buttons[self.num_picture_buttons].grid(row=self.num_picture_buttons, column=0, pady=0, padx=5)
        self.save_picture(self.num_picture_buttons)
        self.num_picture_buttons += 1

    def picture_button_command(self, index):
        # print("old index of picture_button_pressed", index)
        # print(self.actual_picture, "self.actual_picture is")

        self.picture_buttons[self.actual_picture].CButton.itemconfig(self.picture_buttons[index].polygon, fill="gray")
        self.picture_buttons[self.actual_picture].bg = "gray"

        self.save_picture(self.actual_picture)  # Save old picture before switching to the new one
        self.actual_picture = index
        # print("new index of picture_button_pressed", self.actual_picture)
        self.read_picture(self.actual_picture)  # Read from new picture

        self.picture_buttons[index].CButton.itemconfig(self.picture_buttons[index].polygon, fill="green3")
        self.picture_buttons[index].bg = "green3"

    # Export-Window ####################################################################################################
    def export_field(self):
        export_canvas = Ctkinter.CCanvas(master=self.master, size=(300, 170), corners='rounded', max_rad=30,
                                         bg=Window_COLOR)
        export_canvas.place(x=870, y=580)
        ###
        export_label = tkinter.Label(export_canvas.get_canvas(), text="Export", bg=Window_COLOR, fg="white",
                                     font=('Arial', 15))
        export_label.place(x=110, y=5)

        gif_button = Ctkinter.CButton(export_canvas, text="as GIF", height=40, width=150,
                                      rounded_corners='rounded',
                                      bg="gold3", fg="black", highlight_color="gold2",
                                      pressing_color="gold3", command=self.gif_button_pressed)
        gif_button.place(x=70, y=45)

        png_button = Ctkinter.CButton(export_canvas, text="as PNG", height=40, width=150,
                                      rounded_corners='rounded',
                                      bg="DarkOrchid3", fg="black", highlight_color="DarkOrchid2",
                                      pressing_color="DarkOrchid3", command=self.png_button_pressed)
        png_button.place(x=70, y=100)

    def png_button_pressed(self):
        # print("dataname: ", self.creation_name.get())
        color_list = []
        # print("unfertige color-liste in png: ", self.edit_buttons_colors)
        for color in self.edit_buttons_colors:
            color_list.append(ImageColor.getrgb(color))
        # print("color_list in png: ", color_list)
        image = Image.new("RGB", (self.chosen_shape, self.chosen_shape))
        image.putdata(color_list, scale=10000000.0)
        image.save('Creations' + '/' + self.creation_name.get() + ".png")

    def gif_button_pressed(self):
        # print(self.file_location)
        images = []
        # Going through all Images
        for n_image in glob.glob(self.file_location + '/*.txt'):
            # Read Color-list of each picture
            save_file = open(n_image, "r")
            content = save_file.readlines()
            save_file.close()
            color_list = content[2].split(",")
            # print("unfertige color-liste in gif: ", color_list)
            color_list.remove('')
            rgb_colors = []
            for color in color_list:
                rgb_colors.append(ImageColor.getrgb(color))
            # print("color_list in gif: ", rgb_colors)
            # Create Image of each picture and save to images-list
            picture = Image.new("RGB", (self.chosen_shape, self.chosen_shape))
            picture.putdata(rgb_colors, scale=10000000.0)
            images.append(picture)
        images[0].save('Creations' + '/' + self.creation_name.get() + ".gif",
                       save_all=True, append_images=images[1:], optimize=False, duration=700, loop=0)

    # Runs #############################################################################################################
    def run(self, master):
        self.master = master
        self.start_window = Ctkinter.CCanvas(master=self.master, bg=Window_COLOR, size=(300, 350), corners='rounded',
                                             max_rad=30)
        self.title_bar()
        self.creation()
        # self.checkbox_public()
        self.creation_size()
        self.startbutton()
        self.start_window.place(1220, 50)

        self.edit_field()
        self.color_field()
        self.picture_field()
        # self.create_picture_button_pressed()
        self.export_field()


def run(arg,  user):
    GifCreatorStartWindow().run(arg)


if __name__ == '__main__':
    program = GifCreatorStartWindow()
    tkinter.mainloop()
