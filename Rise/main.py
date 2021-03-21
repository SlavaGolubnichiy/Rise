# may be an newer copy of Rising_v3
# the difference is in that in Rising_v3 additional files are located in a package, but here they are in a folder.

# ---------------
# TODO:
#   .
#   1. Implement game objects size and font size dependent from screen size    !!!
#
#   ------------------
#   .
#   .
#   .
#   9. Compile python programs for Windows_x32 using pyinstaller:
#       9.1 Open "Terminal"
#       9.2 type in command: pyinstaller Rising.py
#       9.3 Try to run your app. You will see "import pkg_resourses as res" error (if run from cmd.exe)
#       9.4 Fixing "import pkg_resources as res" error:
#           9.4.1 Open programname.spec in your project venv folder
#           9.4.2 Find "Analysis" section -> find hiddenimports= parameter
#           9.4.3 edit this line like that: hiddenimports=['pkg_resources.py2_warn']
#       9.5 type the following command in Terminal: pyinstaller programname.spec    !!!
#       9.6 Open "your_project_folder/dist/" - here will be programname folder with your compiled program
#       9.7 Don't forget to copy all additional files from project folder to "dist" folder (files such as icon.png etc.)
#   2. Wohooooo!!! You can share your program with friends.


# What is done [Update_1.0.1 notes]
#
# Fixed:
#   1. "Controls" button was opening and immediately closing when the key 'C' was pressed. Now it is correctly
#       responds a single keypress.
#   2. Multiple improvements focused on better future development.
#   3. Wind appearance and behaviour were changed for more realistic.
#
# Added features:
#   1. "Increasing difficulty" added to the game. More enemies are coming !!!
#       Game starts with 10 enemies. Enemies number depends on score from 10 to 999.
#   2. "Pocket for bonus" added to the game. It will be shown at this pocket as the player picks up any bonus.
#       It's brightness shows the time of bonus activeness that remains.
#   3. "NEW BEST" message added. It pops up when a new "Max score" is set.
#   4. Game window got a new designed icon!
#   5. Game start is performed in full screen mode.




import pygame
import sys
import ctypes
import random


# classes

class game_proc:
    def __init__(self):
        self.pygame_clock           = pygame.time.Clock()
        self.lock_fps               = 60
        self.frame_counter          = 0
        self.do_render_game         = True
        self.is_game_paused         = False
        self.game_paused_counter    = 0
        self.do_reset_world         = False
        self.is_quit                = False
        self.game_over              = False
        self.was_bootscreen         = False

    def get_pygame_clock(self):
        return self.pygame_clock

    def get_lock_fps(self):
        return self.lock_fps

    def get_frame_counter(self):
        return self.frame_counter

    def get_do_render_game(self):
        return self.do_render_game

    def get_is_game_paused(self):
        return self.is_game_paused

    def get_game_paused_counter(self):
        return self.game_paused_counter

    def get_do_reset_world(self):
        return self.do_reset_world

    def get_is_quit(self):
        return self.is_quit

    def get_game_over(self):
        return self.game_over

    def get_was_bootscreen(self):
        return self.was_bootscreen

    def set_pygame_clock(self, new_pygame_clock):
        self.pygame_clock = new_pygame_clock

    def set_lock_fps(self, new_lock_fps):
        if new_lock_fps > 15:
            self.lock_fps = new_lock_fps
        else:
            self.lock_fps = 30

    def set_frame_counter(self, new_frame_counter):
        self.frame_counter = new_frame_counter

    def set_do_render_game(self, new_do_render_game):
        self.do_render_game = new_do_render_game

    def set_is_game_paused(self, new_is_game_paused):
        self.is_game_paused = new_is_game_paused

    def set_game_paused_counter(self, new_game_paused_counter):
        self.game_paused_counter = new_game_paused_counter

    def set_do_reset_world(self, new_do_reset_world):
        self.do_reset_world = new_do_reset_world

    def set_is_quit(self, new_is_quit):
        self.is_quit = new_is_quit

    def set_game_over(self, new_game_over):
        self.game_over = new_game_over

    def set_was_bootscreen(self, new_was_bootscreen):
        self.was_bootscreen = new_was_bootscreen


class rect:
    __rect_count = 0  # class attribute

    def __init__(self):
        self._size          = 10  # object's attributes
        self._pos           = [0, 0]
        self._speed         = 1
        self._color         = [255, 255, 255]
        self.frame_counter  = 0

    def set_pos_x(self, new_x):
        self._pos[0] = new_x

    def set_pos_y(self, new_y):
        self._pos[1] = new_y

    def set_color(self, r, g, b):
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            self._color = (r, g, b)
            return 0
        return -1

    def set_frame_counter(self, new_frame_counter):
        if new_frame_counter >= 0:
            self.frame_counter = new_frame_counter
        else:
            self.frame_counter = -new_frame_counter

    def set_speed(self, pxperframe):
        if 0 < pxperframe:
            self._speed = pxperframe
            return 0
        return -1

    def set_size(self, px):
        if 0 < px:
            self._size = px
            return 0
        return -1

    def get_pos(self):
        return self._pos

    def get_pos_x(self):
        return self._pos[0]

    def get_pos_y(self):
        return self._pos[1]

    def get_speed(self):
        return self._speed

    def get_size(self):
        return self._size

    def get_color_r(self):
        return self._color[0]

    def get_color_g(self):
        return self._color[1]

    def get_color_b(self):
        return self._color[2]

    def move(self, dx, dy):
        self._pos[0] += dx
        self._pos[1] += dy

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, (int(self._pos[0]), int(self._pos[1]), self._size, self._size))


class player(rect):
    def __init__(self):
        super().__init__()
        self.default_size       = 100
        self.default_speed      = 4
        self._size              = self.default_size
        self._pos               = [0, 0]
        self._speed             = 4
        self._color             = (15, 89, 153)
        self.__is_size_buffed   = False
        self.__is_speed_buffed  = False

    def set__is_size_buffed(self, flag: bool):
        self.__is_size_buffed = flag

    def get__is_size_buffed(self):
        return self.__is_size_buffed

    def get_default_size(self):
        return self.default_size

    def set__is_speed_buffed(self, flag):
        self.__is_speed_buffed = flag

    def get__is_speed_buffed(self):
        return self.__is_speed_buffed

    def get_default_speed(self):
        return self.default_speed

    def reset(self):
        self.set_size(self.get_default_size())
        self.set_speed(self.get_default_speed())


class enemy(rect):
    def __init__(self):
        super().__init__()
        self.default_size           = 50
        self.default_speed_mul      = 0.2
        self.default_speed          = 4
        self.__speed_mul            = self.default_speed_mul
        self._size                  = 50
        self._pos                   = [0, 0]
        self._speed                 = 4
        self._color                 = (153, 29, 23)
        self.__is_size_buffed       = False
        self.__is_speed_mul_buffed  = False

    def set__is_size_buffed(self, flag: bool):
        self.__is_size_buffed = flag

    def get__is_size_buffed(self):
        return self.__is_size_buffed

    def get_default_size(self):
        return self.default_size

    def set__is_speed_mul_buffed(self, flag):
        self.__is_speed_mul_buffed = flag

    def get__is_speed_mul_buffed(self):
        return self.__is_speed_mul_buffed

    def get_default_speed_mul(self):
        return self.default_speed_mul

    def get_speed_mul(self):
        return self.__speed_mul

    def set_speed_mul(self, new_mul):
        self.__speed_mul = new_mul

    def get_default_speed(self):
        return self.default_speed

    def reset(self):
        self.set_size(self.get_default_size())
        self.set_speed(self.get_default_speed())


class bonus(rect):
    """
        This class is defined for game bonuses objects.
        You can define the same attributes as rect class has for it,
        but also, you have to define a bonus_type of this bonus
        using __type.

        __type value    code                description
        0               "player_smaller"    player rectangle gets smaller size
        1               "enemies_smaller"   enemies rectangles get smaller size
        2               "player_faster"     player rectangle gets faster (increased speed)
        ...
    """

    def __init__(self):
        super().__init__()
        self._size          = 20
        self._pos           = [0, 0]
        self._speed         = 7
        self._color         = (23, 153, 73)
        self.__typesnumber  = 4
        self.__type         = 0
        self.frames_count   = 0
        self.is_stopped     = False

    def set_type(self, __type):
        """
            You have to define a bonus_type of any bonus you create.

            __type value    code                desccription
            0               "player_smaller"    player rectangle gets smaller size
            1               "enemies_smaller"   enemies rectangles get smaller size
            2               "player_faster"     player rectangle gets faster (increased speed)
            ...
        """
        if 0 < __type < self.__typesnumber:
            self.__type = __type
            return 0
        return -1

    def get_type(self):
        return self.__type

    def set_is_stopped(self, new_is_stopped):
        self.is_stopped = new_is_stopped

    def get_is_stopped(self):
        return self.is_stopped

    def buff(self, p_player: player, enemies_list):
        if self.__type == 0:        # player size x0.5
            if not p_player.get__is_size_buffed():
                p_player.set_size(p_player.get_size() // 2)
                p_player.set__is_size_buffed(True)
        elif self.__type == 1:      #  enemies size x0.5
            for i in range(0, len(enemies_list)):
                enemies_list[i].set_size(enemies_list[i].get_size() // 2)
                enemies_list[i].set__is_size_buffed(True)
        elif self.__type == 2:      # player speed x2
            p_player.set_speed(int(p_player.get_speed() + 2))
            p_player.set__is_speed_buffed(True)
        elif self.__type == 3:      # enemies speed x1.5
            for i in range(0, len(enemies_list)):
                enemies_list[i].set_speed_mul(enemies_list[i].get_speed_mul() * 1.5)
                enemies_list[i].set__is_speed_mul_buffed(True)

    def debuff(self, p_player: player, enemies_list):
        if self.__type == 0:
            p_player.set__is_size_buffed(False)
            p_player.set_size(p_player.get_default_size())
        elif self.__type == 1:
            for i in range(0, len(enemies_list)):
                enemies_list[i].set__is_size_buffed(False)
                enemies_list[i].set_size(enemies_list[i].get_default_size())
        elif self.__type == 2:
            p_player.set__is_speed_buffed(False)
            p_player.set_speed(p_player.default_speed)
        elif self.__type == 3:
            for i in range(0, len(enemies_list)):
                enemies_list[i].set__is_speed_mul_buffed(False)
                enemies_list[i].set_speed_mul(enemies_list[i].get_default_speed_mul())


class true_rect:

    def __init__(self):
        self.size_x         = 0     # object's attributes
        self.size_y         = 0
        self.pos_x          = 0
        self.pos_y          = 0
        self.color          = [128, 128, 128]

    def set_size_x(self, px):
        if 0 <= px:
            self.size_x = px
            return 0
        return -1

    def set_size_y(self, px):
        if 0 <= px:
            self.size_y = px
            return 0
        return -1

    def set_pos_x(self, new_pos_x):
        self.pos_x = new_pos_x

    def set_pos_y(self, new_pos_y):
        self.pos_y = new_pos_y

    def set_color(self, r, g, b):
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            self.color = (r, g, b)
            return 0
        return -1

    def get_size_x(self):
        return self.size_x

    def get_size_y(self):
        return self.size_y

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y

    def get_color(self):
        return self.color

    def get_color_r(self):
        return self.color[0]

    def get_color_g(self):
        return self.color[1]

    def get_color_b(self):
        return self.color[2]

    def move(self, dx, dy):
        self.pos_x += dx
        self.pos_y += dy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (int(self.pos_x), int(self.pos_y), self.size_x, self.size_y))


class wind_obj:
    """
        Description
            This class is defined for game wind object, which is represented by a rectangle
            ("wind" class inherits from "rect" class).
            Also, it contains and provides some variables needed to make wind work in a game.

        :param:
            start_pos_x     - wind object start position
            start_pos_y     - wind object start position
            start_size      - wind object start size
            color           - color of wind rectangle

        Description:
            -1 < wind_speed < 0 = adequate left wind
            0 < wind_speed < 1 = adequate right wind

        usage:
    """

    def __init__(self):
        super().__init__()
        self.speed          = 0
        self.is_wind        = False
        self.does_moves     = False
        self.sign           = 1     # right wind by default
        self.dx             = 1
        self.frame_counter  = 0

        self.rect_array_size    = 0
        self.rect_array: list   = [true_rect]

    def get_speed(self):
        return self.speed

    def get_is_wind(self):
        return self.is_wind

    def get_does_moves(self):
        return self.does_moves

    def get_sign(self):
        return self.sign

    def get_dx(self):
        return self.dx

    def get_color(self):
        if 0 < self.rect_array_size:
            return self.rect_array[0].get_color()
        else:
            return -1

    def get_frame_counter(self):
        return self.frame_counter

    def get_rect_array_size(self):
        return self.rect_array_size

    def get_rect_array(self):
        return self.rect_array

    def set_speed(self, new_speed):
        self.speed = new_speed

    def set_is_wind(self, new_is_wind):
        self.is_wind = new_is_wind

    def set_does_moves(self, new_does_moves):
        self.does_moves = new_does_moves

    def set_sign(self, new_sign):
        self.sign = new_sign

    def set_dx(self, new_dx):
        self.dx = new_dx

    def set_frame_counter(self, new_frame_counter):
        if 0 <= new_frame_counter:
            self.frame_counter = new_frame_counter
            return 0
        else:
            self.frame_counter = 0
            return -1

    def set_rect_array(self, new_rect_array):
        self.rect_array = new_rect_array
        self.rect_array_size = len(new_rect_array)
        for i in range(0, self.rect_array_size, 1):
            self.rect_array[i].set_color(0, 0, 50)      # wind color

    def rect_array_append(self, new_true_rect):
        self.rect_array.append(new_true_rect)
        self.rect_array_size = len(self.rect_array)
        self.rect_array[self.rect_array_size - 1].set_color(0, 0, 50)

    def draw_true_rects(self, screen):
        for i in range(0, self.rect_array_size, 1):
            pygame.draw.rect(screen, self.rect_array[i].get_color(), (int(self.rect_array[i].get_pos_x()), int(self.rect_array[i].get_pos_y()), self.rect_array[i].get_size_x(), self.rect_array[i].get_size_y()))


# TEST ---- not used yet

class ingame_obj:
    def __init__(self):
        self.frame_counter = 0

    def get_frame_counter(self):
        return self.frame_counter

    def set_frame_counter(self, new_frame_counter_value):
        self.frame_counter = new_frame_counter_value


class font_obj:
    """
    usage:
        my_font.set_font(pygame_font)
        my_font.set_size(size)
        my_font.set_color((255,255,255))
        texture0 = my_font.render("This is text0")
        texture1 = my_font.render("This is text1")

    """

    def __init__(self):
        self.font_size      = 16
        self.font           = pygame.font.SysFont("Segoe UI", self.font_size)
        self.text_color     = (255, 255, 255)

    def get_font_size(self):
        return self.font_size

    def get_font(self):
        return self.font

    def get_text_color(self):
        return self.text_color

    def set_font_size(self, new_font_size):
        self.font_size = new_font_size

    def set_font(self, new_pygame_font):
        self.font = new_pygame_font

    def set_text_color(self, new_text_color):
        self.text_color = new_text_color

# TEST ---- not used yet


class text_obj:
    """
    usage:
        pygame.font.init()      # important !!!

        my_text = text_obj()
        my_text.set_font(pygame_font)
        my_text.set_font_size(size)
        my_text.set_text("This is my text")
        my_text.set_text_color((255, 255, 255))
        my_text.draw_on(some_screen_surface, x, y)

    """

    def __init__(self, text_str):
        self.font_size      = 24
        self.font           = pygame.font.SysFont("Segoe UI", self.font_size)
        self.text           = text_str
        self.text_color     = (255, 255, 255)
        self.text_texture   = self.font.render(self.text, True, self.text_color)

    def get_font_size(self):
        return self.font_size

    def get_font(self):
        return self.font

    def get_text(self):
        return self.text

    def get_text_color(self):
        return self.text_color

    def get_texture(self):
        return self.text_texture

    def set_font_size(self, new_font_size):
        self.font_size = new_font_size
        self.font = pygame.font.SysFont("Segoe UI", self.font_size)
        self.text_texture = self.font.render(self.text, True, self.text_color)

    def set_text(self, text):
        self.text = text
        self.text_texture = self.font.render(self.text, True, self.text_color)

    def set_text_color(self, new_text_color):
        self.text_color = new_text_color
        self.text_texture = self.font.render(self.text, True, self.text_color)


class pocket_for_bonus:
    """
    usage:
        pocket = pocket_for_bonus()
        pocket.set_size(size)
        pocket.set_inactive_color(r,g,b)
        pocket.set_active_color(r,g,b)
        pocket.set_color(r,g,b)
    """
    pass


# functions


def detect_collision(rect1_pos, rect1_size, rect2_pos, rect2_size):
    a_x = rect1_pos[0]
    a_y = rect1_pos[1]
    b_x = rect2_pos[0]
    b_y = rect2_pos[1]

    if (a_x <= b_x < (a_x + rect1_size)) or (b_x <= a_x < (b_x + rect2_size)):
        if (a_y <= b_y < (a_y + rect1_size)) or (b_y <= a_y < (b_y + rect2_size)):
            return True
    return False


def is_collision(p_player: rect, e_enemy: rect):
    p_x = p_player.get_pos_x()
    p_y = p_player.get_pos_y()
    e_x = e_enemy.get_pos_x()
    e_y = e_enemy.get_pos_y()

    if (p_x <= e_x < (p_x + p_player.get_size())) or (e_x <= p_x < (e_x + e_enemy.get_size())):
        if (p_y <= e_y < (p_y + p_player.get_size())) or (e_y <= p_y < (e_y + e_enemy.get_size())):
            return True
    return False


def is_dot_in_area(x, y, width, height):
    if 0 <= x <= width and 0 <= y <= height:
        return True
    return False


def randomize_enemies(enemies_list, GAME_SCREEN_WIDTH):
    for i in (0, len(enemies_list) - 1, 1):
        enemies_list[i].set_pos_x(random.randint(0, GAME_SCREEN_WIDTH - enemies_list[i].get_size()))
        enemies_list[i].set_pos_y(-enemies_list[i].get_size())
        enemies_list[i].set_speed(random.randint(4, 18) * enemies_list[i].get_speed_mul())


def randomize_wind(wind_object):
    wind_object.set_does_moves(0)
    wind_object.set_sign(bool(random.randint(0, 2)))
    if wind_object.get_is_wind():
        wind_object.set_does_moves(True)
        if not wind_object.get_sign():
            wind_object.set_speed(1)
        else:
            wind_object.set_speed(-1)
    else:
        wind_object.set_speed(0)


def game_objects_reset(some_player, enemies_list, bonuses_list, some_wind, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT):
    some_player.set_pos_x(GAME_SCREEN_WIDTH // 2)
    some_player.set_pos_y(GAME_SCREEN_HEIGHT - 2 * some_player.get_size())

    for i in range(0, len(enemies_list)):
        enemies_list[i].set_pos_x(random.randint(0, GAME_SCREEN_WIDTH - enemies_list[i].get_size()))
        enemies_list[i].set_pos_y(-enemies_list[i].get_size())
        enemies_list[i].set_speed(random.randint(4, 18) * enemies_list[i].get_speed_mul())

    for i in range(0, len(bonuses_list)):
        bonuses_list[i].set_pos_x(random.randint(0, GAME_SCREEN_WIDTH - bonuses_list[i].get_size()))
        bonuses_list[i].set_pos_y(-bonuses_list[i].get_size())

    # wind ---

    #    -1 < wind_speed < 0 = adequate left wind
    #     0 < wind_speed < 1 = adequate right wind

    some_wind.set_speed(0.2)
    for i in range(0, some_wind.get_rect_array_size()):
        some_wind.rect_array[i].set_pos_x(-GAME_SCREEN_HEIGHT)
        some_wind.rect_array[i].set_pos_y(0)

    if some_wind.frame_counter >= 5:  # 3 - is a number of attempts after that wind starts to possibly happen
        some_wind.is_wind = bool(random.randint(0, 2))
    else:
        some_wind.is_wind = False
        some_wind.frame_counter = some_wind.frame_counter + 1

    randomize_wind(some_wind)
    some_wind.set_dx(1)


def calc_score_font_size(start_font_size_value, score_value):
    """
        usage:
        font_size = calc_score_font_size(24, score_value)
    """
    score_font_size = start_font_size_value
    if 999 < score_value < 9999:
        score_font_size = start_font_size_value - 8
    elif 9999 < score_value < 99999:
        score_font_size = start_font_size_value - 16
    return score_font_size


def does_any_line_moves(do_wind_lines_move_flags_array):
    res = False
    for i in range(0, len(do_wind_lines_move_flags_array), 1):
        res = res or do_wind_lines_move_flags_array[i]
        if res:
            break
    return res



# ------------------------------------------------------------ main

# ---------------------- constants


RED = (255, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = (0, 0, 0)

user32 = ctypes.windll.user32       # getting user screen size (width, height)

SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

# SCREEN_WIDTH = 1280     # debug mode
# SCREEN_HEIGHT = 480     # debug mode

if SCREEN_WIDTH < 1280:
    SCREEN_WIDTH = 1280
if SCREEN_HEIGHT < 720:
    SCREEN_HEIGHT = 720



# ---------------------- variables

# variables values at game start
if True:
    game = game_proc()
    game.set_lock_fps(120)
    game.set_do_render_game(False)
    game.set_is_game_paused(True)
    game.set_do_reset_world(True)

    score = 0
    score_pos_x = 0
    score_pos_y = 0
    score_pos_x_rel = 30
    score_pos_y_rel = 5
    is_score_printed = False
    max_score = 0
    gravity_k = 1
    game.set_frame_counter(0)

    default_enemies_number = 10
    enemies_number = 10
    bonuses_number = 2

    is_any_bonus_active = False
    active_bonus_index = 0
    bonus_timer_seconds = 10
    bonus_timer_frames = bonus_timer_seconds * game.get_lock_fps()


    # -------------------------- game objects

    # creating game objects
    p = player()
    enemies = [enemy() for i in range(0, enemies_number)]
    bonuses = [bonus() for i in range(0, bonuses_number)]

    pocket_for_bonus = true_rect()
    pocket_for_bonus.set_color(15, 89, 153)
    pocket_for_bonus.set_size_x(0)
    pocket_for_bonus.set_size_y(4)
    pocket_for_bonus.set_pos_x(p.get_pos_x() + 5)
    pocket_for_bonus.set_pos_y(p.get_pos_y() + p.get_size() - 5)
    size_x_decrement = 0
    pocket_for_bonus_size_x_aux0 = 0

    # wind ---
    wind = wind_obj()

    #    -1 < wind_speed < 0 = adequate left wind
    #     0 < wind_speed < 1 = adequate right wind

    wind.frame_counter = 0
    wind.set_is_wind(False)

    # randomize_wind(wind)

    wind_timer = 0
    generate_wind_period_sec = 10   # 30 seconds
    wind.set_dx(1)

    wind_true_rects_number = 10
    wind_true_rects = [true_rect() for i in range(0, wind_true_rects_number)]
    wind.set_rect_array(wind_true_rects)
    aux_pos_y = SCREEN_HEIGHT // wind.get_rect_array_size()
    for i in range(0, wind.get_rect_array_size(), 1):
        wind.rect_array[i].set_size_x(200)
        wind.rect_array[i].set_size_y(2)
        wind.rect_array[i].set_pos_x(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + wind.rect_array[i].get_size_x()))
        wind.rect_array[i].set_pos_y(aux_pos_y)
        wind.rect_array[i].set_color(12, 63, 146)
        aux_pos_y = aux_pos_y + SCREEN_HEIGHT // wind.get_rect_array_size()

    wind_started = False
    do_wind_lines_move_flags = [False for i in range(0, wind.get_rect_array_size(), 1)]



    # game window and font ---
    pygame.init()       # has to be before pygame.font usage
    pygame.display.set_caption("Rise")
    icon = pygame.image.load("rise_icon.png")
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(False)

    userscreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)


    # game text ---
    pygame.font.init()  # text displaying

    Score_text = text_obj(str(score))
    Score_text.set_font_size(int(60 * p.get_size() / p.get_default_size()))   # independent formula

    Bonus_text = text_obj("")
    Bonus_text.set_font_size(24)
    Bonus_timer_text = text_obj("")
    Bonus_timer_text.set_font_size(24)

    # Controls HELP text ---
    do_show_controls = False
    Help_text0 = text_obj("Controls: C")    # default text font size = 24
    Help_text1 = text_obj("")
    Help_text2 = text_obj("")

    # Encourage message text ---
    encrg_frames_counter = 0      # lock_fps = 120 -> Encrg_msg will appear on a screen for 2 seconds.
    is_encrg_out = False
    Encrg_msg = text_obj("")
    Encrg_msg.set_font_size(64)

    was_encrg0 = False  # 10 < score < 50
    was_encrg1 = False  # 50 < score < 100
    was_encrg2 = False  # 100 < score < 200
    was_encrg3 = False  # 200 < score < 500
    was_encrg4 = False  # 500 < score < 800
    was_encrg5 = False  # 800 < score < 999
    was_encrg6 = False  # 999 < score

    # Developer name
    game.set_was_bootscreen(False)
    dev_name_text_counter = 0
    dev_name_screen_time_s = 3

    dev_name_text0 = text_obj("Go Slava")
    dev_name_text1 = text_obj("game")
    dev_name_text0.set_font_size(64)
    dev_name_text1.set_font_size(36)

    game_paused_time_sec = dev_name_screen_time_s

    # max score text
    max_score_text = text_obj("Max score: " + str(max_score))
    max_score_text.set_font_size(24)

    show_new_best_flag = False

    new_best_text = text_obj("")
    new_best_text.set_font_size(96)


# frame_loop ---
while not game.get_is_quit():

    """ pre_game_mechanics section """

    if not do_show_controls:
        Help_text1.set_text("")
        Help_text2.set_text("")
    else:
        Help_text1.set_text("Move: Up, Down, Right, Left arrows")
        Help_text2.set_text("Quit: Esc")

    # encourage player_user text messages
    if not is_encrg_out:
        encrg_msg_random = random.randint(0, 3)
        is_encrg_out = True

        if 10 < score:
            if not was_encrg0:
                if encrg_msg_random == 0:
                    Encrg_msg.set_text("Good start!")
                elif encrg_msg_random == 1:
                    Encrg_msg.set_text("First blood!")
                else:
                    Encrg_msg.set_text("Go go go!")
                was_encrg0 = True

                add_enemies_number = 2     # 2
                for i in range(0, add_enemies_number, 1):
                    enemies.append(enemy())
                    if enemies[0].get__is_size_buffed():
                        enemies[enemies_number + i].set_size(enemies[0].get_size())
                    if enemies[0].get__is_speed_mul_buffed():
                        enemies[enemies_number + i].set_speed_mul(enemies[0].get_speed_mul())
                enemies_number += add_enemies_number

        elif 50 < score:
            if not was_encrg1:
                if encrg_msg_random == 0:
                    Encrg_msg.set_text("Poltinnik!")
                elif encrg_msg_random == 1:
                    Encrg_msg.set_text("Well done!")
                else:
                    Encrg_msg.set_text("Nice move!")
                was_encrg1 = True

                add_enemies_number = 3     # 3
                for i in range(0, add_enemies_number, 1):
                    enemies.append(enemy())
                    if enemies[0].get__is_size_buffed():
                        enemies[enemies_number + i].set_size(enemies[0].get_size())
                    if enemies[0].get__is_speed_mul_buffed():
                        enemies[enemies_number + i].set_speed_mul(enemies[0].get_speed_mul())
                enemies_number += add_enemies_number

        elif 100 < score:
            if not was_encrg2:
                if encrg_msg_random == 0:
                    Encrg_msg.set_text("Cool!")
                elif encrg_msg_random == 1:
                    Encrg_msg.set_text("Great job!")
                else:
                    Encrg_msg.set_text("Great!")
                was_encrg2 = True

                add_enemies_number = 4     # 4
                for i in range(0, add_enemies_number, 1):
                    enemies.append(enemy())
                    if enemies[0].get__is_size_buffed():
                        enemies[enemies_number + i].set_size(enemies[0].get_size())
                    if enemies[0].get__is_speed_mul_buffed():
                        enemies[enemies_number + i].set_speed_mul(enemies[0].get_speed_mul())
                enemies_number += add_enemies_number

        elif 200 < score:
            if not was_encrg3:
                if encrg_msg_random == 0:
                    Encrg_msg.set_text("Cool!")
                elif encrg_msg_random == 1:
                    Encrg_msg.set_text("Extreme!")
                else:
                    Encrg_msg.set_text("Awesome!")
                was_encrg3 = True

                add_enemies_number = 5     # 5
                for i in range(0, add_enemies_number, 1):
                    enemies.append(enemy())
                    if enemies[0].get__is_size_buffed():
                        enemies[enemies_number + i].set_size(enemies[0].get_size())
                    if enemies[0].get__is_speed_mul_buffed():
                        enemies[enemies_number + i].set_speed_mul(enemies[0].get_speed_mul())
                enemies_number += add_enemies_number

        elif 500 < score:
            if not was_encrg4:
                if encrg_msg_random == 0:
                    Encrg_msg.set_text("Pro!")
                elif encrg_msg_random == 1:
                    Encrg_msg.set_text("Fantastic!")
                else:
                    Encrg_msg.set_text("Wow...")
                was_encrg4 = True

                add_enemies_number = 7     # 7
                for i in range(0, add_enemies_number, 1):
                    enemies.append(enemy())
                    if enemies[0].get__is_size_buffed():
                        enemies[enemies_number + i].set_size(enemies[0].get_size())
                    if enemies[0].get__is_speed_mul_buffed():
                        enemies[enemies_number + i].set_speed_mul(enemies[0].get_speed_mul())
                enemies_number += add_enemies_number

        elif 800 < score:
            if not was_encrg5:
                if encrg_msg_random == 0:
                    Encrg_msg.set_text("Super!")
                elif encrg_msg_random == 1:
                    Encrg_msg.set_text("Cheater?!")
                else:
                    Encrg_msg.set_text("Brilliant!")
                was_encrg5 = True

                add_enemies_number = 9     # 9
                for i in range(0, add_enemies_number, 1):
                    enemies.append(enemy())
                    if enemies[0].get__is_size_buffed():
                        enemies[enemies_number + i].set_size(enemies[0].get_size())
                    if enemies[0].get__is_speed_mul_buffed():
                        enemies[enemies_number + i].set_speed_mul(enemies[0].get_speed_mul())
                enemies_number += add_enemies_number

        elif 999 < score:
            if not was_encrg6:
                if encrg_msg_random == 0:
                    Encrg_msg.set_text("Outstanding!")
                elif encrg_msg_random == 1:
                    Encrg_msg.set_text("Unbelievable!")
                else:
                    Encrg_msg.set_text("Incredible!")
                was_encrg6 = True

                add_enemies_number = 11     # 11
                for i in range(0, add_enemies_number, 1):
                    enemies.append(enemy())
                    if enemies[0].get__is_size_buffed():
                        enemies[enemies_number + i].set_size(enemies[0].get_size())
                    if enemies[0].get__is_speed_mul_buffed():
                        enemies[enemies_number + i].set_speed_mul(enemies[0].get_speed_mul())
                enemies_number += add_enemies_number

        else:
            is_encrg_out = False
    else:
        if encrg_frames_counter < 200:
            encrg_frames_counter += 1
        else:
            is_encrg_out = False
            encrg_frames_counter = 0
            Encrg_msg.set_text("")

    score_pos_x = p.get_pos_x() + score_pos_x_rel
    score_pos_y = p.get_pos_y() + score_pos_y_rel

    pocket_for_bonus.set_size_x(0)
    pocket_for_bonus.set_pos_x(p.get_pos_x() + 5)
    pocket_for_bonus.set_pos_y(p.get_pos_y() + p.get_size() - 5)


    # ------------------------------------------------------ end of const section

    # variables values at each attempt start
    if game.get_do_reset_world():
        game.set_frame_counter(0)
        game.set_game_over(False)
        max_score_text.set_text("Max score: " + str(max_score))
        score = 0
        score_pos_x_rel = 30
        score_pos_y_rel = 5
        is_score_printed = False
        Score_font_scale = p.get_size() / p.get_default_size()

        # timer of active bonus
        if is_any_bonus_active:
            bonuses[active_bonus_index].debuff(p, enemies)
            # reset Bonus_text and Bonus_timer_text
            Bonus_text.set_text("")
            Bonus_timer_text.set_text("")
            if bonuses[active_bonus_index].get_type() == 0:
                # reset Score_text scale
                Score_text.set_font_size(int(Score_text.get_font_size() / Score_font_scale))
            is_any_bonus_active = False
            bonuses[active_bonus_index].frames_count = 0
            pocket_for_bonus_size_x_aux0 = 0
            pocket_for_bonus.set_size_x(0)

        is_any_bonus_active = False
        active_bonus_index = 0

        enemies_number = default_enemies_number
        enemies.clear()
        for i in range(0, enemies_number, 1):
            enemies.append(enemy())

        # type randomization must be after debuff section !!!
        for j in range(0, len(bonuses)):
            bonuses[j].set_type(random.randint(0, 3))
            # change the same line in calculate_game_mechanics section to get particular bonus


        # -------------------------- game objects

        # start parameters initialization

        game_objects_reset(p, enemies, bonuses, wind, SCREEN_WIDTH, SCREEN_HEIGHT)
        score_pos_x = p.get_pos_x() + score_pos_x_rel
        score_pos_y = p.get_pos_y() + score_pos_y_rel

        """ wind """
        wind.frame_counter = 0
        wind.set_is_wind(False)
        wind.set_does_moves(False)
        # randomize_wind(wind)
        wind_timer = 0
        wind.set_dx(1)

        wind_true_rects_number = 10
        wind_true_rects = [true_rect() for i in range(0, wind_true_rects_number)]
        wind.set_rect_array(wind_true_rects)
        aux_pos_y = SCREEN_HEIGHT // wind.get_rect_array_size()
        for i in range(0, wind.get_rect_array_size(), 1):
            wind.rect_array[i].set_size_x(200)
            wind.rect_array[i].set_size_y(2)
            wind.rect_array[i].set_pos_x(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + wind.rect_array[i].get_size_x()))
            wind.rect_array[i].set_pos_y(aux_pos_y)
            wind.rect_array[i].set_color(12, 63, 146)
            aux_pos_y = aux_pos_y + SCREEN_HEIGHT // wind.get_rect_array_size()

        wind_started = False
        for i in range(0, len(do_wind_lines_move_flags), 1):
            do_wind_lines_move_flags[i] = False

        # font ---
        Score_text.set_font_size(int(60 * p.get_size() / p.get_default_size()))   # independent formula
        Score_text.set_text(str(score))

        new_best_text.set_text("")

        Bonus_text.set_text("")
        Bonus_timer_text.set_text("")

        was_encrg0 = False  # 10 < score < 50
        was_encrg1 = False  # 50 < score < 100
        was_encrg2 = False  # 100 < score < 200
        was_encrg3 = False  # 200 < score < 500
        was_encrg4 = False  # 500 < score < 800
        was_encrg5 = False  # 800 < score < 999
        was_encrg6 = False  # 999 < score

        game.set_do_reset_world(False)



    """ game mechanics calculation """
    if not game.get_is_game_paused():
        Score_font_scale = p.get_size() / p.get_default_size()
        game.set_frame_counter(game.get_frame_counter() + 1)
        Score_text.set_text(str(score))

        # move player, enemies and bonuses
        if 0 <= p.get_pos_x() <= SCREEN_WIDTH-p.get_size():
            p.move(wind.get_speed(), 0)
        if 0 <= p.get_pos_y() <= SCREEN_HEIGHT-p.get_size():
            p.move(0, gravity_k*1)

        for i in range(0, len(enemies)):
            if -enemies[i].get_size() <= enemies[i].get_pos_x() < SCREEN_WIDTH and -enemies[i].get_size() <= enemies[i].get_pos_y() < SCREEN_WIDTH:
                enemies[i].move(int(wind.get_speed()), enemies[i].get_speed())
            else:
                enemies[i].set_speed(random.randint(4, 18) * enemies[i].get_speed_mul())
                enemies[i].set_pos_x(random.randint(0, SCREEN_WIDTH - enemies[i].get_size()))
                enemies[i].set_pos_y(-enemies[i].get_size())
                score += 1
                # score = int(score * 1.5)      # for debuging

        if 0 <= score <= 9:
            score_pos_x_rel = 33 * p.get_size() // p.get_default_size()
            score_pos_y_rel = 2 * p.get_size() // p.get_default_size()
        elif 9 < score < 99:
            score_pos_x_rel = 18 * p.get_size() // p.get_default_size()
        elif 99 < score < 999:
            score_pos_x_rel = 5 * p.get_size() // p.get_default_size()
        elif 999 < score < 9999:
            Score_text.set_font_size(46 * p.get_size() // p.get_default_size())
            score_pos_y_rel = 12 * p.get_size() // p.get_default_size()
        elif 9999 < score < 99999:
            Score_text.set_font_size(34 * p.get_size() // p.get_default_size())
            score_pos_y_rel = 20 * p.get_size() // p.get_default_size()
        elif 99999 < score < 999999:
            Score_text.set_font_size(30 * p.get_size() // p.get_default_size())
            score_pos_y_rel = 25 * p.get_size() // p.get_default_size()
        elif 999999 < score:
            print("You win the game! The whole game!"
                  "You crazy professional zadrot of MLG PRO gaming warleague."
                  "You can make a screenshot, delete the game and go to your friends"
                  "and say what a megasuper professional awesome intelligent super-duper gamer You are."
                  "Congratulations from developers!")

        """ bonuses movement logic """
        for i in range(0, len(bonuses)):
            if not is_any_bonus_active:
                bonuses[i].set_is_stopped(False)
                if -bonuses[i].get_size() <= bonuses[i].get_pos_x() < SCREEN_WIDTH and -bonuses[i].get_size() <= bonuses[i].get_pos_y() < SCREEN_WIDTH:
                    bonuses[i].move(int(wind.get_speed()), bonuses[i].get_speed())
                else:
                    bonuses[i].set_pos_x(random.randint(0, SCREEN_WIDTH - bonuses[i].get_size()))
                    bonuses[i].set_pos_y(-bonuses[i].get_size())
                    bonuses[i].set_speed(random.randint(10, 18) / 2)
                    if not is_any_bonus_active:
                        for j in range(0, len(bonuses)):
                            bonuses[j].set_type(random.randint(0, 3))   # 0 and 3 included
                            # change the same line in do_reset_world section to get particular bonus
            else:
                if not bonuses[i].get_is_stopped():
                    if -bonuses[i].get_size() <= bonuses[i].get_pos_x() < SCREEN_WIDTH and -bonuses[i].get_size() <= bonuses[i].get_pos_y() < SCREEN_WIDTH:
                        if active_bonus_index != i:
                            bonuses[i].move(int(wind.get_speed()), bonuses[i].get_speed())
                    else:
                        bonuses[i].set_is_stopped(True)

        # wind_bringer movement and logic
        if 0 <= wind_timer <= generate_wind_period_sec * game.get_lock_fps() or does_any_line_moves(do_wind_lines_move_flags):
            if wind.get_is_wind():
                if not wind_started:
                    for i in range(0, len(do_wind_lines_move_flags), 1):  # set flags that all winds move now
                        do_wind_lines_move_flags[i] = True
                    wind_started = True
                for i in range(0, wind.get_rect_array_size(), 1):
                    if do_wind_lines_move_flags[i]:
                        if not wind.get_sign():
                            if -wind.rect_array[i].get_size_x() <= wind.rect_array[i].get_pos_x() <= SCREEN_WIDTH:
                                # move right
                                if wind.get_dx() < 1:
                                    wind.set_dx(wind.get_dx() + 0.01)
                                wind.rect_array[i].move(wind.get_speed() * 8, 0)
                            else:
                                # teleport to the left
                                wind.rect_array[i].set_pos_x(random.randint(-2 * wind.rect_array[i].get_size_x(), -wind.rect_array[i].get_size_x()))
                                if generate_wind_period_sec * game.get_lock_fps() <= wind_timer:
                                    do_wind_lines_move_flags[i] = False
                        else:
                            if -wind.rect_array[i].get_size_x() <= wind.rect_array[i].get_pos_x() <= SCREEN_WIDTH:
                                # move left
                                if wind.get_dx() < 1:
                                    wind.set_dx(wind.get_dx() + 0.01)
                                wind.rect_array[i].move(wind.get_speed() * 8, 0)
                            else:
                                # teleport to the right
                                wind.rect_array[i].set_pos_x(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + wind.rect_array[i].get_size_x()))
                                if generate_wind_period_sec * game.get_lock_fps() <= wind_timer:
                                    do_wind_lines_move_flags[i] = False
            wind_timer += 1
        else:
            was_wind = wind.get_is_wind()
            wind.set_is_wind(bool(random.randint(0, 1)))
            if wind.get_is_wind():
                if was_wind:                 # if wind was and will be
                    if not wind.get_sign():     # if was right wind
                        wind.set_sign(False)        # set_wind(right)
                    else:                       # if was left wind
                        wind.set_sign(True)         # set_wind(left)
                else:                       # else if wind wasn't and will be
                    wind.set_sign(bool(random.randint(0, 1)))
            wind_started = False
            if wind.get_is_wind():
                for i in range(0, len(do_wind_lines_move_flags), 1):    # set flags that all winds move now
                    do_wind_lines_move_flags[i] = True
                if not wind.get_sign():
                    wind.set_speed(1)
                else:
                    wind.set_speed(-1)
            else:
                for i in range(0, len(do_wind_lines_move_flags), 1):  # set flags that all winds don't move now
                    do_wind_lines_move_flags[i] = False
                wind.set_speed(0)
            wind_timer = 0




        # detect collisions of player with enemies
        for i in range(0, len(enemies)):
            if is_collision(p, enemies[i]):
                game.set_game_over(True)
                game.set_is_game_paused(True)
                break

        # detect collisions of player with bonuses
        if not is_any_bonus_active:
            for i in range(0, len(bonuses)):
                if is_collision(p, bonuses[i]):
                    bonuses[i].buff(p, enemies)

                    pocket_for_bonus_size_x_aux0 = (p.get_size() - 10) * p.get_size() // p.get_default_size()
                    pocket_for_bonus.set_size_x((p.get_size() - 10) * p.get_size() // p.get_default_size())
                    pocket_for_bonus.set_color(0, 255, 0)
                    size_x_decrement = (p.get_size() - 10) / bonus_timer_frames

                    active_bonus_index = i
                    is_any_bonus_active = True
                    bonuses[active_bonus_index].set_pos_x(random.randint(0, SCREEN_WIDTH))
                    bonuses[active_bonus_index].set_pos_y(-bonuses[i].get_size())
                    if bonuses[active_bonus_index].get_type() == 0:      # if bonus = player_smaller
                        # change Score_text scale
                        Score_font_scale = p.get_size() / p.get_default_size()
                        Score_text.set_font_size(int(Score_text.get_font_size() * Score_font_scale))
                        # Render "Player size x0.5"
                        Bonus_text.set_text("Player size x0.5")
                    elif bonuses[active_bonus_index].get_type() == 1:   # if bonus = enemies small
                        # Render "Enemies size x0.5"
                        Bonus_text.set_text("Enemies size x0.5")
                    elif bonuses[active_bonus_index].get_type() == 2:
                        # Render "Player speed x2"
                        Bonus_text.set_text("Player speed x2")
                    elif bonuses[active_bonus_index].get_type() == 3:
                        # Render "Enemies speed x1.5"
                        Bonus_text.set_text("Enemies speed x1.5")
                    break




        # timer of active bonus
        if is_any_bonus_active:
            # Bonus_timer_text.set_text(str(int(bonus_timer_seconds - bonuses[active_bonus_index].frames_count/game.get_lock_fps())) + " s")
            if bonuses[active_bonus_index].frames_count >= bonus_timer_frames:
                bonuses[active_bonus_index].debuff(p, enemies)

                pocket_for_bonus_size_x_aux0 = 0
                pocket_for_bonus.set_size_x(0)
                pocket_for_bonus.set_color(15, 89, 153)
                size_x_decrement = 0

                # reset Bonus_text and Bonus_timer_text
                Bonus_text.set_text("")
                Bonus_timer_text.set_text("")
                if bonuses[active_bonus_index].get_type() == 0:
                    # reset Score_text scale
                    Score_text.set_font_size(int(Score_text.get_font_size() / Score_font_scale))
                is_any_bonus_active = False
                bonuses[active_bonus_index].frames_count = 0
            else:
                bonuses[active_bonus_index].frames_count += 1
                pocket_for_bonus_size_x_aux0 = pocket_for_bonus_size_x_aux0 - size_x_decrement
                pocket_for_bonus.set_size_x(int(pocket_for_bonus_size_x_aux0))





    """ post_game_mechanics section """

    # draw and update frame
    userscreen.fill(BACKGROUND_COLOR)
    if game.get_do_render_game():
        # draw enemies (the farthest layer), bonuses (farther layer) and player (near layer)
        wind.draw_true_rects(userscreen)
        for i in range(0, enemies_number):
            enemies[i].draw(userscreen)
        p.draw(userscreen)
        for i in range(0, bonuses_number):
            bonuses[i].draw(userscreen)

        pocket_for_bonus.draw(userscreen)

        # draw text on a screen
        userscreen.blit(Score_text.get_texture(), (score_pos_x, score_pos_y))
        userscreen.blit(Bonus_text.get_texture(), (10, SCREEN_HEIGHT - 50))
        userscreen.blit(Bonus_timer_text.get_texture(), (280, SCREEN_HEIGHT - 50))
        userscreen.blit(Help_text0.get_texture(), (10, 10))  # (10,  10) -----\
        userscreen.blit(Help_text1.get_texture(), (10, 40))  # (+0; +30) <----|
        userscreen.blit(Help_text2.get_texture(), (10, 70))  # (+0; +60) <----|
        userscreen.blit(Encrg_msg.get_texture(), (SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2 - Encrg_msg.get_font_size()))
        userscreen.blit(max_score_text.get_texture(), (SCREEN_WIDTH - 200, SCREEN_HEIGHT - max_score_text.get_font_size() - 10))
        userscreen.blit(new_best_text.get_texture(), (SCREEN_WIDTH // 2 - (new_best_text.get_font_size() // 4) * len(new_best_text.get_text()), SCREEN_HEIGHT // 2 - new_best_text.get_font_size()))
    else:
        userscreen.blit(dev_name_text0.get_texture(), (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - dev_name_text0.get_font_size()))
        userscreen.blit(dev_name_text1.get_texture(), (SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT // 2 - dev_name_text1.get_font_size() + 6))

    game.get_pygame_clock().tick(game.get_lock_fps())
    pygame.display.update()

    # keybuttons processing ---

    # pressed and held keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not game.get_is_game_paused():
            if (p.get_pos_x() - p.get_speed()) > 0:
                p.move(-p.get_speed(), 0)
    if keys[pygame.K_RIGHT]:
        if not game.get_is_game_paused():
            if (p.get_pos_x() + p.get_size() + p.get_speed()) < SCREEN_WIDTH:
                p.move(p.get_speed(), 0)
    if keys[pygame.K_UP]:
        if not game.get_is_game_paused():
            if (p.get_pos_y() - p.get_speed()) > 0:
                p.move(0, -p.get_speed())
    if keys[pygame.K_DOWN]:
        if not game.get_is_game_paused():
            if (p.get_pos_y() + p.get_size() + p.get_speed()) < SCREEN_HEIGHT:
                p.move(0, p.get_speed())

    # single pressed keys
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                do_show_controls = not do_show_controls
#            if event.key == pygame.K_p:
#                is_quit=False          # for debugging specified game events
            if event.key == pygame.K_ESCAPE:
                game.set_is_quit(True)
                break

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # new game state calculation
    if game.get_game_over() and not game.get_is_game_paused():
        game.set_is_game_paused(True)
        game_paused_time_sec = 1
        game.set_game_paused_counter(0)

    if game.get_is_game_paused():
        if score > max_score:
            new_best_text.set_text("NEW BEST!")

        if game.get_game_paused_counter() < game_paused_time_sec * game.get_lock_fps():
            game.set_game_paused_counter(game.get_game_paused_counter() + 1)
        else:
            game.set_game_over(False)
            game.set_is_game_paused(False)
            game.set_do_reset_world(True)
            game.set_game_paused_counter(0)

    # boot screen calc
    if not game.get_was_bootscreen():
        if dev_name_text_counter < (dev_name_screen_time_s * game.get_lock_fps()):         # pause game when boot screen
            dev_name_text_counter += 1
        else:
            game.set_do_render_game(True)
            game.set_is_game_paused(False)
            game.set_was_bootscreen(True)
            game.set_game_paused_counter(0)
            game_paused_time_sec = 1




# } end of frame loop






    if game.get_game_over() and not is_score_printed:
        if score > max_score:
            max_score = score
        print("Your score = ", score)
        is_score_printed = True




pygame.quit()
sys.exit()
