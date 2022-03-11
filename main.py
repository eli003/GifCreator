import Ctkinter as Ctk
import tkinter as tk

import creater_studio


class StartApp:
    def __init__(self, master, app):
        self.master = master
        self.app = app

    def start_app(self):
        # size= 1533, 862
        self.master.attributes('-fullscreen', True)
        game_canvas = Ctk.CCanvas(self.master, bg='gray12', size=(1533, 862), corners='rounded', max_rad=30)

        self.app(game_canvas)

        close_button = Ctk.CButton(master=game_canvas, bg='red', highlight_color='red', pressing_color='darkred',
                                   width=50, height=25, text='X', font=('Helvetica', 15), fg='white',
                                   rounded_corners='round', command=self.master.destroy, max_rad=None)

        close_button.place(x=1470, y=5)

        game_canvas.place(x=1, y=1)


root = tk.Tk()
root.config(bg='gray24')
root.geometry("+%d+%d" % (800, 100))
studio = creater_studio.GifCreatorStartWindow()

creator = StartApp(root, studio.run)

b = tk.Button(root, command=lambda: creator.start_app(), text='RUN', width=50, height=5,
              bg='blue').pack(padx=100, pady=100)

root.mainloop()
