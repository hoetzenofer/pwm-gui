import os
os.chdir(os.path.dirname(__file__))

import pygame as pg
import json
import string

with open("config.json", "r") as file:
    jdata = json.load(file)

grid_size = jdata["grid-size"][0], jdata["grid-size"][1]
grid_element = jdata["grid-element"]

class Button:
    def __init__(self, normal_image: str, hover_image: str, active_image: str, text_standby: str, text_active: str, font_path: str, font_size: int, font_color: tuple[int, int, int], position: tuple[int, int]):
        self.normal_image = pg.transform.scale(pg.image.load(normal_image), (pg.image.load(normal_image).get_width() * grid_element, pg.image.load(normal_image).get_height() * grid_element))
        self.hover_image = pg.transform.scale(pg.image.load(hover_image), (pg.image.load(hover_image).get_width() * grid_element, pg.image.load(hover_image).get_height() * grid_element))
        self.pressed_image = pg.transform.scale(pg.image.load(active_image), (pg.image.load(active_image).get_width() * grid_element, pg.image.load(active_image).get_height() * grid_element))
        self.text = text_standby
        self.text_standby = text_standby
        self.text_active = text_active
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color
        self.position = position[0] * grid_element, position[1] * grid_element

        self.is_hovered = False
        self.is_pressed = False

    def draw(self, surface):
        if self.is_pressed:
            surface.blit(self.pressed_image, self.normal_image.get_rect(center=self.position))
        elif self.is_hovered:
            surface.blit(self.hover_image, self.normal_image.get_rect(center=self.position))
        else:
            surface.blit(self.normal_image, self.normal_image.get_rect(center=self.position))

        # drawing text
        font = pg.font.Font(self.font_path, self.font_size * 5).render(self.text, True, self.font_color)
        text_rect = font.get_rect(center=self.position)
        surface.blit(font, text_rect.topleft)

    def is_hover(self, mouse_pos):
        button_rect = self.normal_image.get_rect(center=self.position)
        self.is_hovered = button_rect.collidepoint(mouse_pos)           # mouse colliding with hitbox?

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_pressed = True
            if self.text_active != None:
                self.text = self.text_active
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered:
                self.is_pressed = False
                self.text = self.text_standby
                return True
            self.is_pressed = False
        return False
    
class ButtonToggle:
    def __init__(self, normal_image: str, hover_image: str, active_image: str, text_standby: str, text_active: str, font_path: str, font_size: int, font_color: tuple[int, int, int], position: tuple[int, int]):
        self.normal_image = pg.transform.scale(pg.image.load(normal_image), (pg.image.load(normal_image).get_width() * grid_element, pg.image.load(normal_image).get_height() * grid_element))
        self.hover_image = pg.transform.scale(pg.image.load(hover_image), (pg.image.load(hover_image).get_width() * grid_element, pg.image.load(hover_image).get_height() * grid_element))
        self.pressed_image = pg.transform.scale(pg.image.load(active_image), (pg.image.load(active_image).get_width() * grid_element, pg.image.load(active_image).get_height() * grid_element))
        self.text = text_standby
        self.text_standby = text_standby
        self.text_active = text_active
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color
        self.position = position[0] * grid_element, position[1] * grid_element

        self.is_hovered = False
        self.is_active = False

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.pressed_image, self.normal_image.get_rect(center=self.position))
        elif self.is_hovered:
            surface.blit(self.hover_image, self.normal_image.get_rect(center=self.position))
        else:
            surface.blit(self.normal_image, self.normal_image.get_rect(center=self.position))

        # drawing text
        font = pg.font.Font(self.font_path, self.font_size * 5).render(self.text, True, self.font_color)
        text_rect = font.get_rect(center=self.position)
        surface.blit(font, text_rect.topleft)

    def is_hover(self, mouse_pos):
        button_rect = self.normal_image.get_rect(center=self.position)
        self.is_hovered = button_rect.collidepoint(mouse_pos)           # mouse colliding with hitbox?

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_active = not self.is_active
            if self.text_active != None:
                if self.is_active == True:
                    self.text = self.text_active
                else:
                    self.text = self.text_standby
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            return True
        return False
    
class InputField:
    def __init__(self, normal_image: str, active_image: str, standard_value: str, font_path: str, font_size: int, font_color: tuple[int, int, int], input_type, max_input: int, position: tuple[int, int]):
        self.normal_image = pg.transform.scale(pg.image.load(normal_image), (pg.image.load(normal_image).get_width() * grid_element, pg.image.load(normal_image).get_height() * grid_element))
        self.active_image = pg.transform.scale(pg.image.load(active_image), (pg.image.load(active_image).get_width() * grid_element, pg.image.load(active_image).get_height() * grid_element))
        self.standard_value = standard_value
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color
        self.input_type = input_type
        self.max_input = max_input
        self.position = position[0] * grid_element, position[1] * grid_element

        self.is_active = False
        self.text = standard_value
        self.font = pg.font.Font(None, self.font_size)

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.active_image, self.normal_image.get_rect(center=self.position))
        else:
            surface.blit(self.normal_image, self.normal_image.get_rect(center=self.position))

        # render written text
        font = pg.font.Font(self.font_path, self.font_size * 5).render(self.text, True, self.font_color)
        text_rect = font.get_rect(center=(self.position[0], self.position[1]))
        surface.blit(font, text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            textfield_rect = self.normal_image.get_rect(center=self.position)

            if textfield_rect.collidepoint(mouse_pos):
                self.is_active = True                   # set field to active if clicked
                if self.text == self.standard_value:    # checking if value is standard text
                    self.text = ""                      # if so reset value

            else:
                self.is_active = False                  # set field to inactive if clicked somewhere else

        if event.type == pg.KEYDOWN and self.is_active:
            if len(self.text) >= self.max_input and event.key != pg.K_BACKSPACE:
                self.text = ""

            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]

            elif self.input_type == int and event.unicode in string.digits:             # is input a number?
                self.text += event.unicode                                              # if so add input to text

            elif self.input_type == str and event.unicode in string.ascii_letters:      # is input a char?
                self.text += event.unicode                                              # if so add input to text

            elif self.input_type == None:
                self.text += event.unicode
