import pygame as py


class Console:
    """
    This is a custom class that creates the "console" which prints out messages to the user based on certain
    events/actions that has happened within the sudoku program
    """

    def __init__(self, screen: py.surface, x: int, y: int, width: int, height: int, font: py.font,
                 max_lines=10, color="black") -> None:
        """
        Constructs the console object

        :param screen: The screen surface that this console widget would be placed upon
        :param x: x coordinate position of console
        :param y: y coordinate position of console
        :param width: Width of console
        :param height: Height of console
        :param font: The font that would be used within this object
        :param max_lines: The number of lines that can be displayed at once, can be adjusted as needed
        :param color: Color of this widget
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.max_lines = max_lines
        self.color = color
        self.messages = []

    def add_message(self, text: str) -> None:
        """
        Add a new message to the console

        :param text: A text to be printed out on the console
        :return: None
        """
        self.messages.append(text)

    def draw(self, new_x: int, new_y: int, x_shift=8, y_shift=3) -> None:
        """
        This draws the console and messages within the self.message variable

        :param new_x: This represents the new x coordinate as needed
        :param new_y: This represents the new y coordinate as needed
        :param x_shift: Shifting the console horizontally if needed
        :param y_shift: Shifting the console vertically if needed
        :return:
        """
        self.x = new_x
        self.y = new_y
        y_down = 0
        py.draw.rect(self.screen, py.Color("#FFFAC7"), py.Rect(self.x, self.y, self.width, self.height))
        py.draw.rect(self.screen, py.Color("black"), py.Rect(self.x, self.y, self.width, self.height), 2)
        if len(self.messages) > 12:  # Here, the console can only hold around 12 line of messages, change if needed
            self.messages = self.messages[len(self.messages)-12:]
        for i in self.messages:
            self.screen.blit(self.font.render(i, 1, self.color),
                             (self.x + x_shift, self.y + y_shift + y_down))
            y_down += 20  # This value moves each message down by 20 pixels

    def clear_message(self) -> None:
        """
        Clears the message list

        :return: None
        """
        self.messages.clear()
