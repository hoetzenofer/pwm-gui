import os
os.chdir(os.path.dirname(__file__))

import pygame as pg
import json
from ext import Button, ButtonToggle, InputField

with open("config.json", "r") as file:
    jdata = json.load(file)

pg.init()

# SETUP
grid_size = jdata["grid-size"]
grid_element = jdata["grid-element"]
window_scale = grid_size[0] * grid_element, grid_size[1] * grid_element

screen = pg.display.set_mode(window_scale)
clock = pg.time.Clock()

cs = jdata["img"]["img-folder"] + "//" + jdata["img"]["color-scheme"] + "//"
font = jdata["font"]

# BUTTONS
button_start_clock = ButtonToggle(
    f"{cs}button_big.png",
    f"{cs}button_big_highlight.png",
    f"{cs}button_big_pressed.png",
    "START", "STOP", font, 5, (255, 255, 255),
    (30, 48)
)

button_single_step = Button(
    f"{cs}button_small.png",
    f"{cs}button_small_highlight.png",
    f"{cs}button_small_pressed.png",
    "0", "1", font, 5, (255, 255, 255),
    (12, 48)
)

# INPUT FIELDS
input_frequency = InputField(
    f"{cs}textfield_mid.png",
    f"{cs}textfield_mid_active.png",
    "CLK", font, 4, (255, 255, 255), int, 4,
    (14, 20)
)

input_ti = InputField(
    f"{cs}textfield_mid.png",
    f"{cs}textfield_mid_active.png",
    "Ti", font, 4, (255, 255, 255), None, 3,
    (14, 31)
)

input_gpio = InputField(
    f"{cs}textfield_small.png",
    f"{cs}textfield_small_active.png",
    "PIN", font, 4, (255, 255, 255), int, 2,
    (40, 20)
)

# FUNKTIONS
def draw_text(text, pos, font_name, font_size, color, align=None):
    font = pg.font.Font("font//" + font_name, font_size * 5)
    rendered_font = font.render(text, True, color)
    text_rect = rendered_font.get_rect()

    if align == "l":
        text_rect.midleft = (pos[0] * grid_element, pos[1] * grid_element)
    elif align == "r":
        text_rect.midright = (pos[0] * grid_element, pos[1] * grid_element)
    else:
        text_rect.center = (pos[0] * grid_element, pos[1] * grid_element)
    
    screen.blit(rendered_font, text_rect)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break

        mouse_pos = pg.mouse.get_pos()

        # buttons hovered?
        button_start_clock.is_hover(mouse_pos)
        button_single_step.is_hover(mouse_pos)
        
        # buttons clicked?
        if button_start_clock.is_clicked(event):
            print("PWM Clock running!")

        if button_single_step.is_clicked(event):
            print("call function2")

        # input field event happening? (clicked? text input?)
        input_frequency.handle_event(event)
        input_ti.handle_event(event)
        input_gpio.handle_event(event)

    screen.fill(jdata["scheme-data"][jdata["img"]["color-scheme"]]["background-color"])

    try:
        pwm_frequency = int(input_frequency.text)

    except:
        pass

    # main start
    draw_text("PWM Clock Config", (grid_size[0] / 2, 6), "minecraft.ttf", 8, (255, 255, 255))

    draw_text("Hz", (24, 20), "minecraft.ttf", 5, (255, 255, 255), "l")
    draw_text("%", (24, 31), "minecraft.ttf", 5, (255, 255, 255), "l")

    button_start_clock.draw(screen) 
    button_single_step.draw(screen) 

    input_frequency.draw(screen)
    input_ti.draw(screen)
    input_gpio.draw(screen)

    print(button_start_clock.is_active)
    # main end

    pg.display.update()
    clock.tick(60)

os._exit(0)
