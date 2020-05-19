from tkinter import *
from Player import Fighter
from Bot import Bot
import winsound
from time import sleep
from PIL import Image
from PIL import ImageTk

WIDTH = 600
HEIGHT = 400


class Battle:
    images = []
    PLAYER_ONE_POSITION = (100, 370)
    PLAYER_TWO_POSITION = (400, 370)
    LEFT  = "left"
    RIGHT = "right"

    def __init__(self, game_window):
        self.game_window = game_window
        self.canvas = Canvas(game_window, width=WIDTH, height=HEIGHT)

        self.canvas.bind("<KeyPress>", self.key_press)
        self.canvas.bind("<KeyRelease>", self.key_release)

        self.set_background()
        self.player_one = self.create_kisame(False, self.PLAYER_ONE_POSITION)
        self.player_two = self.create_kakashi(True, self.PLAYER_TWO_POSITION)

        self.canvas.pack()
        self.canvas.focus_set()

        winsound.PlaySound(r'music\LifeIsGood.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        self.game_window.after(0, self.game)

    def game(self):
        self.player_one.set_opponent(self.player_two)
        self.player_two.set_opponent(self.player_one)
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
        self.player_one_controller_press(e)
        self.player_two_controller_press(e)

    def key_release(self, e):
        self.player_one_controller_release(e)
        self.player_two_controller_release(e)

    def player_one_controller_press(self, e):
        if not self.player_one.is_bot:
            if e.char == "d":
                self.player_one.right()
            if e.char == "a":
                self.player_one.left()
            if e.char == " ":
                self.player_one.attack()
            if e.char == "w":
                self.player_one.jump()

    def player_two_controller_press(self, e):
        if not self.player_two.is_bot:
            if e.char == "l":
                self.player_two.right()
            if e.char == "j":
                self.player_two.left()
            if e.char == "k":
                self.player_two.attack()
            if e.char == "i":
                self.player_two.jump()

    def player_one_controller_release(self, e):
        if not self.player_one.is_bot:
            if e.char in ['w', 'a', ' ', 'd']:
                self.player_one.stance()

    def player_two_controller_release(self, e):
        if not self.player_two.is_bot:
            if e.char in ['i', 'j', 'k', 'l']:
                self.player_two.stance()

    def create_fighter(self, ai, name, position):
        direction = self.RIGHT
        if position == self.PLAYER_TWO_POSITION:
            direction = "left"

        if ai:
            fighter = Bot(name, direction, self.canvas, position)
        else:
            fighter = Fighter(name, direction, self.canvas, position)
        return fighter

    def create_deidara(self, ai, position):
        fighter = self.create_fighter(ai, "deidara", position)
        return fighter

    def create_kakashi(self, ai, position):
        fighter = self.create_fighter(ai, "kakashi", position)
        fighter.set_animation_sprites("stance", list(range(0, 6)))
        fighter.set_animation_sprites("run", list(range(6, 12)))
        fighter.set_animation_sprites("damage", list(range(12, 14)))
        fighter.set_animation_sprites("fall", list(range(12, 18)))
        fighter.set_animation_sprites("attack", list(range(18, 31)))
        return fighter

    def create_kisame(self, ai, position):
        fighter = self.create_fighter(ai, "kisame", position)
        fighter.set_animation_sprites("stance", list(range(0, 4)))
        fighter.set_animation_sprites("run", list(range(4, 9)))
        fighter.set_animation_sprites("damage", list(range(9, 11)))
        fighter.set_animation_sprites("fall", list(range(9, 15)))
        fighter.set_animation_sprites("attack", list(range(15, 28)))
        fighter.set_animation_sprites("jump", (list(range(28, 33))+list(range(28, 33))))
        return fighter

    def create_sasori(self, ai, position):
        fighter = self.create_fighter(ai, "sasori", position)
        fighter.set_animation_sprites("stance", list(range(0, 6)))
        fighter.set_animation_sprites("run", list(range(6, 12)))
        fighter.set_animation_sprites("damage", list(range(12, 14)))
        fighter.set_animation_sprites("fall", list(range(12, 18)))
        fighter.set_animation_sprites("attack", list(range(18, 40)))
        fighter.set_animation_sprites("jump", (list(range(40, 45)) + list(range(40, 45))))
        return fighter


root = Tk()
root.title("Life Is Good")
img = PhotoImage(file="sprites\Future\smile.png")
root.iconphoto(False, img)
Battle(root)
root.mainloop()
input()

