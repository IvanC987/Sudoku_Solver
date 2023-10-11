import pygame as py


class Button:
    """
    This custom class creates the button widget, used within the sudoku program
    """

    def __init__(self, screen: py.surface, x: int, y: int, width: int, height: int) -> None:
        """
        This function

        :param screen: This variable takes in the surface that we are using
        :param x: x coordinate
        :param y: y coordinate
        :param width: width of the button
        :param height: height of the button
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, button_color: str, outline_size=2, outline_color=(0, 0, 0)) -> None:
        """
        This function draws the button onto the provided surface

        :param button_color: Color of the button
        :param outline_size: Size of the button
        :param outline_color: Outline color is set to black by default
        :return: None
        """
        py.draw.rect(self.screen, py.Color(button_color), py.Rect(self.x, self.y, self.width, self.height), self.height)
        py.draw.rect(self.screen, py.Color(outline_color), py.Rect(self.x, self.y, self.width, self.height),
                     outline_size)

    def add_text(self, font, text="", text_color=(0, 0, 0), x_shift=0, y_shift=0) -> None:
        """
        This function adds text, labeling the created button

        :param font: The font being used
        :param text: Text to be added on the button, if desired
        :param text_color: Text color is set to black by default
        :param x_shift: Due to the size of font/button, the label may need to be shifted
        :param y_shift: Same as x
        :return: None
        """
        self.screen.blit(font.render(text, 1, text_color), (self.x + x_shift, self.y + y_shift))

    def clicked(self, x, y) -> None:
        """
        Checks if the button is clicked

        :param x: x coordinate of where the mouse clicked
        :param y: y coordinate of where the mouse clicked
        :return: None
        """
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)
