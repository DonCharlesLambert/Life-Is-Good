from PIL import Image, ImageOps
from PIL import ImageTk
import os


class StatusBar:

    def __init__(self, player, side):
        self.fighter = player
        self.side = side

        self.canvas = player.canvas
        self.CANVAS_WIDTH = self.canvas.winfo_reqwidth()
        self.CANVAS_HEIGHT = self.canvas.winfo_reqheight()

        self.mugshot = self.get_mugshot()
        self.health_bar = self.get_health_bar()
        self.canvas_mugshot = None
        self.canvas_health_bar = None

        self.draw_self()

    def draw_self(self):
        if self.side == "right":
            self.canvas.create_image((self.CANVAS_WIDTH * 0.08, self.CANVAS_HEIGHT * 0.1), image=self.mugshot)
            self.canvas.create_image((self.CANVAS_WIDTH * 0.1, self.CANVAS_HEIGHT * 0.27), image=self.health_bar)
        else:
            self.canvas.create_image((self.CANVAS_WIDTH * 0.92, self.CANVAS_HEIGHT * 0.1), image=self.mugshot)
            self.canvas.create_image((self.CANVAS_WIDTH * 0.9, self.CANVAS_HEIGHT * 0.27), image=self.health_bar)

    def redraw_self(self):
        self.health_bar = self.get_health_bar()
        self.canvas.itemconfig(self.canvas_health_bar, image=self.health_bar)

    def get_mugshot(self):
        img = Image.open(os.path.join('sprites', self.fighter.name, "mug.png"))
        img = self.scale_mugshot(img)
        mugshot = ImageTk.PhotoImage(img)
        return mugshot

    def get_health_bar(self):
        img = Image.open(os.path.join('sprites', 'misc', 'health bars', "100.png"))
        img = self.scale_health_bar_img(img)
        health_bar = ImageTk.PhotoImage(img)
        return health_bar

    def scale_health_bar_img(self, img):
        width = int(self.CANVAS_WIDTH * 0.2)
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
