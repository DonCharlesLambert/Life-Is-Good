from PIL import Image
from PIL import ImageTk
import os
from Status import StatusBar
import random


# 🍝
class Fighter:
    # MOVEMENT & COLLISION CONSTANTS
    NEXT_TO_THRESHOLD = 35
    MOVE_BACK = 70
    JUMP_HEIGHT = 20

    # ACTION CONSTANTS
    STANCE = "stance"
    RUN = "run"
    ATTACK = "attack"
    FALL = "fall"
    JUMP = "jump"
    DAMAGE = "damage"

    # DIRECTION CONSTANTS
    RIGHT = "right"
    LEFT = "left"
    SWITCH = "switch"

    def __init__(self, name, initial_direction, sprite_canvas, pos):
        self.name = name
        self.canvas = sprite_canvas
        self.direction = initial_direction
        self.opponent = None
        self.status_bar = StatusBar(self, initial_direction)

        self.CANVAS_WIDTH = self.canvas.winfo_reqwidth()
        self.CANVAS_HEIGHT = self.canvas.winfo_reqheight()

        self.animation_no = 0
        self.direction = self.RIGHT
        self.action = self.STANCE

        self.speed = 0.02
        self.health = 100

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
        self.draw_sprite_img(pos)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''         PRIMARY INTERFACE            '''
    ''''''''''''''''''''''''''''''''''''''''''''

    def stance(self):
        self.change_state("", self.STANCE)

    def right(self):
        self.change_state(self.RIGHT, self.RUN)

    def left(self):
        self.change_state(self.LEFT, self.RUN)

    def attack(self):
        self.change_state("", self.ATTACK)

    def fall(self):
        self.change_state("", self.FALL)

    def jump(self):
        self.change_state("", self.JUMP)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''              SETTERS                 '''
    ''''''''''''''''''''''''''''''''''''''''''''

    def set_animation_sprites(self, animation_name, image_numbers):
        self.sprites[animation_name] = image_numbers

    def set_opponent(self, player):
        self.opponent = player

    ''''''''''''''''''''''''''''''''''''''''''''
    '''              GETTERS                 '''
    ''''''''''''''''''''''''''''''''''''''''''''

    def pos(self):
        return self.canvas.coords(self.sprite_item)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''             CHECKERS                 '''
    ''''''''''''''''''''''''''''''''''''''''''''
    def being_attacked(self):
        if self.opponent is None:
            return False
        elif self.next_to_opponent() and self.opponent.action_is(self.ATTACK):
            return True

    def has_received_combo(self):
        if self.next_to_opponent() and self.opponent.action_is(self.ATTACK) and self.opponent.end_of_animation():
            return True

    def action_is(self, action):
        if self.action == action:
            return True
        return False

    def is_facing(self, direction):
        if self.direction == direction:
            return True
        return False

    def end_of_animation(self):
        return self.animation_no == len(self.sprites[self.action]) - 1

    def end_of_action(self, action):
        if self.action == action and self.end_of_animation():
            return True
        return False

    def action_not_finished(self, action):
        if self.action == action and not self.end_of_animation():
            return True
        return False

    def next_to_opponent(self):
        return abs(self.opponent.pos()[0] - self.pos()[0]) < self.NEXT_TO_THRESHOLD

    ''''''''''''''''''''''''''''''''''''''''''''
    '''           DRAW TO CANVAS             '''
    ''''''''''''''''''''''''''''''''''''''''''''
    def draw_sprite_img(self, pos):
        self.get_sprite_img()
        self.sprite_item = self.canvas.create_image(pos, image=self.sprite_img, anchor="se")

    def redraw_sprite_img(self):
        self.get_sprite_img()
        self.canvas.itemconfig(self.sprite_item, image=self.sprite_img)

    def get_sprite_img(self):
        img_no = self.sprites[self.action][self.animation_no]
        img = Image.open(os.path.join('sprites', self.name, self.direction, str(img_no) + ".png"))
        self.sprite_img = ImageTk.PhotoImage(img)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''               MOVING                 '''
    ''''''''''''''''''''''''''''''''''''''''''''
    def move(self):
        if self.action_is(self.RUN):
            if self.is_facing(self.RIGHT):
                speed = self.speed
            else:
                speed = -self.speed

            if 0 < self.pos()[0] + self.CANVAS_WIDTH * speed < self.CANVAS_WIDTH:
                self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * speed, 0)

    def move_back(self):
        if self.is_facing(self.RIGHT):
            if 0 < self.pos()[0] - self.MOVE_BACK < self.CANVAS_WIDTH:
                self.canvas.move(self.sprite_item, -self.MOVE_BACK, 0)
        else:
            if 0 < self.pos()[0] + self.MOVE_BACK < self.CANVAS_WIDTH:
                self.canvas.move(self.sprite_item, 70, 0)

    def jump_path(self):
        if len(self.sprites[self.action]) % 2 == 0:
            if self.animation_no < len(self.sprites[self.action]) / 2:
                self.canvas.move(self.sprite_item, 0, -self.JUMP_HEIGHT)
            else:
                self.canvas.move(self.sprite_item, 0, self.JUMP_HEIGHT)
        else:
            if self.animation_no < len(self.sprites[self.action]) / 2 - 1:
                self.canvas.move(self.sprite_item, 0, -self.JUMP_HEIGHT)
            elif self.animation_no != len(self.sprites[self.action]) - 1:
                self.canvas.move(self.sprite_item, 0, self.JUMP_HEIGHT)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''         HANDLING USER INPUT          '''
    ''''''''''''''''''''''''''''''''''''''''''''
    # changing direction and action
    def change_state(self, direction, action):
        if self.action_not_finished(self.FALL):
            pass
        elif self.action_not_finished(self.DAMAGE):
            pass
        elif self.action_not_finished(self.JUMP):
            self.move_while_jumping(direction)
        else:
            if (direction != "") and (not direction == self.direction):
                self.direction = direction
                self.animation_no = 0
            if (action != "") and (not action == self.action):
                self.action = action
                self.animation_no = 0
            if direction == "switch":
                if self.is_facing(self.RIGHT):
                    self.direction = self.LEFT
                else:
                    self.direction = self.RIGHT
                self.animation_no = 0

    def move_while_jumping(self, direction):
        if direction != "":
            self.direction = direction
            if self.direction == "right":
                self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * self.speed * 2, 0)
            else:
                self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * -self.speed * 2, 0)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''       HANDLING TIME PASSING          '''
    ''''''''''''''''''''''''''''''''''''''''''''
    # animating the character and moving
    def animate(self):
        if self.end_of_action(self.FALL):
            self.move_back()
            self.stance()

        elif self.end_of_action(self.JUMP):
            self.stance()

        elif self.action_is(self.JUMP):
            self.jump_path()

        elif self.has_received_combo():
            self.fall()

        elif self.being_attacked():
            self.change_state("", "damage")

        elif not self.being_attacked() and self.action == "damage":
            self.stance()

        self.move()
        self.animation_no = (self.animation_no + 1) % (len(self.sprites[self.action]))
        self.redraw_sprite_img()


class Bot(Fighter):
    def __init__(self, name, initial_direction, sprite_canvas, pos):
        super(Bot, self).__init__(name, initial_direction, sprite_canvas, pos)

    def animate(self):
        super().animate()
        self.decide_movement()

    def decide_movement(self):
        if self.action_is(self.DAMAGE) or self.action_is(self.FALL):
            pass

        elif self.opponent.action_is(self.FALL):
            self.change_state(self.SWITCH, self.RUN)

        elif self.action_is(self.ATTACK) and not self.opponent.action_is(self.DAMAGE):
            self.change_state("", self.STANCE)

        elif self.action_is(self.ATTACK):
            pass

        elif self.next_to_opponent():
            self.decide_to_attack()

        else:
            self.run_to_opponent()

    def decide_to_attack(self):
        if random.random() < 0.2:
            self.change_state("", self.ATTACK)
        else:
            self.change_state("", self.STANCE)

    def run_to_opponent(self):
        if self.opponent.pos()[0] < self.pos()[0]:
            self.change_state(self.LEFT, self.RUN)
        else:
            self.change_state(self.RIGHT, self.RUN)
