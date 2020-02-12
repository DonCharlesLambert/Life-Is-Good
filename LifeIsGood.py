from tkinter import *
from Player import Fighter
import winsound
from time import sleep
from PIL import Image
from PIL import ImageTk

WIDTH = 600
HEIGHT = 400


class Battle:
    images = []

    def __init__(self, game_window):
        self.game_window = game_window
        self.canvas = Canvas(game_window, width=WIDTH, height=HEIGHT)

        self.canvas.bind("<KeyPress>", self.key_press)
        self.canvas.bind("<KeyRelease>", self.key_release)

        self.set_background()
        self.player_one = Fighter("deidara", "left", self.canvas, (400, 330))
        self.player_two = Fighter("sasori", "right", self.canvas, (100, 330))

        self.canvas.pack()
        self.canvas.focus_set()

        winsound.PlaySound(r'music\LifeIsGood.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        self.game_window.after(0, self.game)

    def game(self):
        while True:
            self.player_one.animate()
            self.player_two.animate()
            self.canvas.update()
            sleep(0.1)

    def set_background(self):
        img = Image.open(r'sprites\misc\rocks.png')
        img = img.resize((self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.images.append(bg_image)

    def key_press(self, e):
        if e.char == "d":
            self.player_one.change_state("right", "run")
        if e.char == "a":
            self.player_one.change_state("left", "run")
        if e.char == " ":
            self.player_one.change_state("", "attack")

    def key_release(self, e):
        self.player_one.change_state("", "stance")


root = Tk()
Battle(root)
root.mainloop()

