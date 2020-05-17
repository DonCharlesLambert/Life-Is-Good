from PIL import Image
from PIL import ImageTk
import os
from Status import StatusBar


# 🍝
class Fighter:
    # FOLDER CONSTANT
    SPRITE_FOLDER = 'sprites'

    # MOVEMENT & COLLISION CONSTANTS
    NEXT_TO_THRESHOLD = 35
    MOVE_BACK = 70
    JUMP_HEIGHT = 20

    # HEALTH CONSTANTS
    MAX_HEALTH = 100
    DAMAGE_PER_SECOND = 1

    # ACTION CONSTANTS
    STANCE = "stance"
    RUN = "run"
    ATTACK = "attack"
    FALL = "fall"
    JUMP = "jump"
    DAMAGE = "damage"
    DEAD = "dead"

    # DIRECTION CONSTANTS
    RIGHT = "right"
    LEFT = "left"
    SWITCH = "switch"
    REMAIN = ""

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
        self.health = self.MAX_HEALTH
        self.dead = False

        self.sprite_img = None
        self.sprite_item = None

        self.sprites = {
            self.STANCE : list(range(0, 4)),
            self.RUN    : list(range(4, 10)),
            self.DAMAGE : list(range(10, 12)),
            self.FALL   : list(range(10, 15)),
            self.ATTACK : list(range(16, 39)),
            self.JUMP   : [39, 39, 40, 40, 41, 41, 42, 42, 43]
        }
        self.draw_sprite_img(pos)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''         PRIMARY INTERFACE            '''
    ''''''''''''''''''''''''''''''''''''''''''''

    def stance(self):
        self.change_state(self.REMAIN, self.STANCE)

    def right(self):
        self.change_state(self.RIGHT, self.RUN)

    def left(self):
        self.change_state(self.LEFT, self.RUN)

    def away(self):
        self.change_state(self.SWITCH, self.RUN)

    def attack(self):
        self.change_state(self.REMAIN, self.ATTACK)

    def jump(self):
        self.change_state(self.REMAIN, self.JUMP)

    def damage(self):
        self.change_state(self.opponent.backside(), self.DAMAGE)

    def fall(self):
        self.change_state(self.REMAIN, self.FALL)

    def die(self):
        self.dead = True
        self.change_state(self.REMAIN, self.FALL)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''              SETTERS                 '''
    ''''''''''''''''''''''''''''''''''''''''''''

    def set_animation_sprites(self, animation_name, image_numbers):
        self.sprites[animation_name] = image_numbers

    def set_opponent(self, player):
        self.opponent = player

    def switch_direction(self):
        if self.is_facing(self.RIGHT):
            self.direction = self.LEFT
        else:
            self.direction = self.RIGHT
        self.animation_no = 0

    ''''''''''''''''''''''''''''''''''''''''''''
    '''              GETTERS                 '''
    ''''''''''''''''''''''''''''''''''''''''''''

    def pos(self):
        return self.canvas.coords(self.sprite_item)

    def backside(self):
        return self.RIGHT if self.direction == self.LEFT else self.LEFT

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
        img = Image.open(os.path.join(self.SPRITE_FOLDER, self.name, self.direction, str(img_no) + ".png"))
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
        if self.dead:
            self.action = action
        elif self.action_not_finished(self.FALL):
            pass
        elif self.action_not_finished(self.DAMAGE):
            pass
        elif self.action_not_finished(self.JUMP):
            self.move_while_jumping(direction)
        else:
            if (direction != self.REMAIN) and (not direction == self.direction):
                self.direction = direction
                self.animation_no = 0
            if (action != self.REMAIN) and (not action == self.action):
                self.action = action
                self.animation_no = 0
            if direction == self.SWITCH:
                self.switch_direction()

    def move_while_jumping(self, direction):
        if direction != self.REMAIN:
            self.direction = direction
            if self.direction == self.RIGHT:
                self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * self.speed * 2, 0)
            else:
                self.canvas.move(self.sprite_item, self.CANVAS_WIDTH * -self.speed * 2, 0)

    ''''''''''''''''''''''''''''''''''''''''''''
    '''       HANDLING TIME PASSING          '''
    ''''''''''''''''''''''''''''''''''''''''''''
    # animating the character and moving
    def animate(self):
        if self.dead and self.end_of_action(self.FALL):
            return

        elif self.action_is(self.DAMAGE):
            self.take_damage()

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
            self.damage()

        elif not self.being_attacked() and self.action_is(self.DAMAGE):
            self.stance()

        self.move()
        self.animation_no = (self.animation_no + 1) % (len(self.sprites[self.action]))
        self.redraw_sprite_img()

    def take_damage(self):
        self.health -= self.DAMAGE_PER_SECOND
        self.status_bar.update()
        if self.health <= 0:
            self.die()
