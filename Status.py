from PIL import Image, ImageOps
from PIL import ImageTk
import os
import time

class StatusBar:

    def __init__(self, player, side):
        self.fighter = player
        self.side = side

        self.canvas = player.canvas
        self.CANVAS_WIDTH = self.canvas.winfo_reqwidth()
        self.CANVAS_HEIGHT = self.canvas.winfo_reqheight()

        self.mugshot = self.get_mugshot()
        self.health_bar = self.get_health_bar()
        self.chakra_bar = None
        self.outline = self.get_outline()
        self.canvas_mugshot = None
        self.canvas_health_bar = None
        self.canvas_health_outline = None
        self.canvas_chakra_bar = None
        self.canvas_chakra_outline = None

        self.draw_self()

    def draw_self(self):
        if self.side == "right":
            chakra_bar_pos  = (self.CANVAS_WIDTH * 0.1, self.CANVAS_HEIGHT * 0.03)
            image_pos       = (self.CANVAS_WIDTH * 0.08, self.CANVAS_HEIGHT * 0.1)
            health_bar_pos  = (0, self.CANVAS_HEIGHT * 0.1)
            anchor          = "nw"
        else:
            chakra_bar_pos  = (self.CANVAS_WIDTH * 0.9, self.CANVAS_HEIGHT * 0.03)
            image_pos       = (self.CANVAS_WIDTH * 0.92, self.CANVAS_HEIGHT * 0.1)
            health_bar_pos  = (self.CANVAS_WIDTH, self.CANVAS_HEIGHT * 0.1)
            anchor          = "ne"

        self.canvas_chakra_outline = self.canvas.create_image(chakra_bar_pos, image=self.outline, anchor=anchor)
        self.canvas_chakra_bar = self.canvas.create_image(chakra_bar_pos, image=self.chakra_bar, anchor=anchor)
        self.canvas.create_image(image_pos, image=self.mugshot)
        self.canvas_health_outline = self.canvas.create_image(health_bar_pos, image=self.outline, anchor=anchor)
        self.canvas_health_bar = self.canvas.create_image(health_bar_pos, image=self.health_bar, anchor=anchor)

    def update_chakra(self):
        self.chakra_bar = self.get_chakra_bar()
        self.redraw_chakra()

    def update_health(self):
        img = Image.open(os.path.join('sprites', 'misc', 'health bars', "100.png"))
        img = self.scale_health_bar_img(img)
        img = self.scale_img(img, self.fighter.health / self.fighter.MAX_HEALTH)
        self.health_bar = ImageTk.PhotoImage(img)
        self.redraw_health()

    def redraw_health(self):
        self.canvas.itemconfig(self.canvas_health_bar, image=self.health_bar)

    def redraw_chakra(self):
        self.canvas.itemconfig(self.canvas_chakra_bar, image=self.chakra_bar)

    def get_mugshot(self):
        img = Image.open(os.path.join('sprites', self.fighter.name, "mug.png"))
        img = self.scale_mugshot(img)
        mugshot = ImageTk.PhotoImage(img)
        return mugshot


    def get_outline(self):
        img = Image.open(os.path.join('sprites', 'misc', 'health bars', "outline.png"))
        img = self.scale_health_bar_img(img)
        health_bar = ImageTk.PhotoImage(img)
        return health_bar

    def get_chakra_bar(self):
        img = Image.open(os.path.join('sprites', 'misc', 'health bars', "100c.png"))
        img = self.scale_health_bar_img(img)
        health_bar = ImageTk.PhotoImage(img)
        return health_bar

    def get_health_bar(self):
        img = Image.open(os.path.join('sprites', 'misc', 'health bars', "100.png"))
        img = self.scale_health_bar_img(img)
        health_bar = ImageTk.PhotoImage(img)
        return health_bar

    def scale_health_bar_img(self, img):
        width = int(self.CANVAS_WIDTH * 0.23)
        height = int(width * (img.size[1] / img.size[0]))
        img = img.resize((width, height), Image.ANTIALIAS)
        if self.side == "left":
            img = ImageOps.mirror(img)
        return img

    def scale_mugshot(self, img):
        height = int(self.CANVAS_WIDTH * 0.2)
        width = int(height * (img.size[0] / img.size[1]))
        img = img.resize((width, height), Image.ANTIALIAS)
        return img

    def scale_img(self, img, scale):
        width = int(img.size[0] * scale)
        if width < 1:
            width = 1
        height = img.size[1]
        img = img.resize((width, height), Image.ANTIALIAS)
        return img
