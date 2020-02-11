from tkinter import *
import os
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
        self.player_one = Player("deidara", self.canvas, (100, 330))

        self.canvas.pack()
        self.canvas.focus_set()
        self.game_window.after(0, self.game)

    def game(self):
        while True:
            self.player_one.animate()
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


class Player:
    animation_no = 0
    speed = 0.02
    direction = "right"
    action = "stance"
    sprites = {
        "stance": [0, 1, 2, 3],
        "run"   : [4, 5, 6, 7, 8, 9],
        "attack": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    }

    def __init__(self, name, sprite_canvas, pos):
        self.name = name
        self.canvas = sprite_canvas
        self.pos = pos
        self.sprite_img = None
        self.sprite_item = None
        self.draw_sprite()

        self.CANVAS_WIDTH = self.canvas.winfo_reqwidth()
        self.CANVAS_HEIGHT = self.canvas.winfo_reqheight()

    def draw_sprite(self):
        self.get_sprite()
        self.sprite_item = self.canvas.create_image(self.pos, image=self.sprite_img)

    def redraw_sprite(self):
        self.get_sprite()
        self.canvas.itemconfig(self.sprite_item, image=self.sprite_img)

    def get_sprite(self):
        img_no = self.sprites[self.action][self.animation_no]
        img = Image.open(os.path.join('sprites', self.name, self.direction, str(img_no) + ".png"))
        self.sprite_img = ImageTk.PhotoImage(img)

    # changing direction and action
    def change_state(self, direction, action):
        if (direction != "") and (not direction == self.direction):
            self.direction = direction
            self.animation_no = 0
        if (action != "") and (not action == self.action):
            self.action = action
            self.animation_no = 0

    def move(self):
        if self.action == "run":
            if self.direction == "right":
                speed = self.speed
            else:
                speed = -self.speed
            self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * speed, 0)

    # animating the character and moving
    def animate(self):
        self.move()
        self.animation_no = (self.animation_no + 1) % (len(self.sprites[self.action]))
        self.redraw_sprite()


root = Tk()
Battle(root)
root.mainloop()

