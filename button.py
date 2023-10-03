import pygame as py


class Button:

    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, button_color, outline_size=2, outline_color=(0, 0, 0)):
        py.draw.rect(self.screen, py.Color(button_color), py.Rect(self.x, self.y, self.width, self.height), self.height)
        py.draw.rect(self.screen, py.Color(outline_color), py.Rect(self.x, self.y, self.width, self.height),
                     outline_size)

    def add_text(self, font, text="", text_color=(0, 0, 0), x_shift=0, y_shift=0):
        self.screen.blit(font.render(text, 1, text_color), (self.x + x_shift, self.y + y_shift))

    def clicked(self, x, y):
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)


