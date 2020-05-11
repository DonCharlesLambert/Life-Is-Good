from PIL import Image
from PIL import ImageTk
import os
from Status import StatusBar
import random


class Fighter:

    NEXT_TO_THRESHOLD = 35
    MOVE_BACK = 70
    JUMP_HEIGHT = 20

    def __init__(self, name, initial_direction, sprite_canvas, pos):
        self.name = name
        self.canvas = sprite_canvas
        self.direction = initial_direction
        self.opponent = None
        self.status_bar = StatusBar(self, initial_direction)

        self.CANVAS_WIDTH = self.canvas.winfo_reqwidth()
        self.CANVAS_HEIGHT = self.canvas.winfo_reqheight()

        self.animation_no = 0
        self.direction = "right"
        self.action = "stance"

        self.speed = 0.02
        self.health = 0

        self.sprite_img = None
        self.sprite_item = None

        self.sprites = {
            "stance": list(range(0, 4)),
            "run"   : list(range(4, 10)),
            "damage": list(range(10, 12)),
            "fall"  : list(range(10, 15)),
            "attack": list(range(16, 39)),
            "jump"  : [39, 39, 40, 40, 41, 41, 42, 42, 43]
        }
        self.draw_sprite(pos)

    def set_animation_sprites(self, animation_name, image_numbers):
        self.sprites[animation_name] = image_numbers

    def set_opponent(self, player):
        self.opponent = player

    def draw_sprite(self, pos):
        self.get_sprite()
        self.sprite_item = self.canvas.create_image(pos, image=self.sprite_img, anchor="se")

    def redraw_sprite(self):
        self.get_sprite()
        self.canvas.itemconfig(self.sprite_item, image=self.sprite_img)

    def get_sprite(self):
        img_no = self.sprites[self.action][self.animation_no]
        img = Image.open(os.path.join('sprites', self.name, self.direction, str(img_no) + ".png"))
        self.sprite_img = ImageTk.PhotoImage(img)

    # changing direction and action
    def change_state(self, direction, action):
        if self.action == "fall" and not self.end_of_animation():
            pass
        elif self.action == "damage" and not self.end_of_animation():
            pass
        elif self.action == "jump" and not self.end_of_animation():
            if direction != "":
                self.direction = direction
                if self.direction == "right":
                    self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * self.speed * 2, 0)
                else:
                    self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * -self.speed * 2, 0)
        else:
            if (direction != "") and (not direction == self.direction):
                self.direction = direction
                self.animation_no = 0
            if (action != "") and (not action == self.action):
                self.action = action
                self.animation_no = 0
            if direction == "switch":
                if self.direction == "right":
                    self.direction = "left"
                else:
                    self.direction = "right"
                self.animation_no = 0

    def pos(self):
        return self.canvas.coords(self.sprite_item)

    def move(self):
        if self.action == "run":
            if self.direction == "right":
                speed = self.speed
            else:
                speed = -self.speed

            if 0 < self.pos()[0] + self.CANVAS_WIDTH * speed < self.CANVAS_WIDTH:
                self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * speed, 0)

    def move_back(self):
        if self.direction == "right":
            if 0 < self.pos()[0] - self.MOVE_BACK < self.CANVAS_WIDTH:
                self.canvas.move(self.sprite_item, -self.MOVE_BACK, 0)
        else:
            if 0 < self.pos()[0] + self.MOVE_BACK < self.CANVAS_WIDTH:
                self.canvas.move(self.sprite_item, 70, 0)

    # animating the character and moving
    def animate(self):
        if self.end_of_fall():
            self.move_back()
            self.change_state("", "stance")
        elif self.end_of_jump():
            self.change_state("", "stance")
        elif self.action == "jump":
            self.jump_path()
        elif self.received_combo():
            self.change_state("", "fall")
        elif self.being_attacked():
            self.change_state("", "damage")
        elif not self.being_attacked() and self.action == "damage":
            self.change_state("", "stance")

        self.move()
        self.animation_no = (self.animation_no + 1) % (len(self.sprites[self.action]))
        self.redraw_sprite()

    def being_attacked(self):
        if self.opponent is None:
            return False
        elif self.next_to_opponent() and self.opponent.action == "attack":
            return True

    def received_combo(self):
        if self.next_to_opponent() and self.opponent.action == "attack" and self.opponent.end_of_animation():
            return True

    def end_of_animation(self):
        return self.animation_no == len(self.sprites[self.action]) - 1

    def end_of_fall(self):
        if self.action == "fall" and self.end_of_animation():
            return True
        return False

    def jump_path(self):
        if len(self.sprites[self.action]) % 2 == 0:
            if self.animation_no < len(self.sprites[self.action])/2:
                self.canvas.move(self.sprite_item, 0, -self.JUMP_HEIGHT)
            else:
                self.canvas.move(self.sprite_item, 0, self.JUMP_HEIGHT)
        else:
            if self.animation_no < len(self.sprites[self.action])/2 - 1:
                self.canvas.move(self.sprite_item, 0, -self.JUMP_HEIGHT)
            elif self.animation_no != len(self.sprites[self.action]) - 1:
                self.canvas.move(self.sprite_item, 0, self.JUMP_HEIGHT)

    def end_of_jump(self):
        if self.action == "jump" and self.end_of_animation():
            return True
        return False

    def next_to_opponent(self):
        return abs(self.opponent.pos()[0] - self.pos()[0]) < self.NEXT_TO_THRESHOLD


class Bot(Fighter):
    def __init__(self, name, initial_direction, sprite_canvas, pos):
        super(Bot, self).__init__(name, initial_direction, sprite_canvas, pos)

    def animate(self):
        super().animate()
        self.decide_movement()

    def decide_movement(self):
        if self.action == "damage" or self.action == "fall":
            pass
        elif self.opponent.action == "fall":
            self.change_state("switch", "run")
        elif self.action == "attack" and self.opponent.action != "damage":
            self.change_state("", "stance")
        elif self.action == "attack":
            pass
        elif self.next_to_opponent():
            if random.random() < 0.2:
                self.change_state("", "attack")
            else:
                self.change_state("", "stance")
        elif self.opponent.pos()[0] < self.pos()[0]:
            self.change_state("left", "run")
        else:
            self.change_state("right", "run")
