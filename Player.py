from PIL import Image
from PIL import ImageTk
import os
from Status import StatusBar

class Fighter:
    animation_no = 0
    direction = "right"
    action = "stance"

    speed = 0.02
    health = 0

    sprite_img = None
    sprite_item = None
    sprites = {
        "stance": [0, 1, 2, 3],
        "run"   : [4, 5, 6, 7, 8, 9],
        "attack": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    }

    def __init__(self, name, initial_direction, sprite_canvas, pos):
        self.name = name
        self.canvas = sprite_canvas
        self.pos = pos
        self.direction = initial_direction

        self.draw_sprite()
        self.status_bar = StatusBar(self, initial_direction)

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
