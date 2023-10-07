import pygame as py


class Console:
    def __init__(self, screen, x, y, width, height, font, max_lines=10, color="black"):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.max_lines = max_lines  # Maximum number of lines to display
        self.color = color
        self.messages = []  # Store the messages

    def add_message(self, text):
        # Add a new message to the console
        self.messages.append(text)

    def draw(self, new_x, new_y, x_shift=8, y_shift=3):
        # Draw the console background
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
            y_down += 20  # This value...

    def clear_message(self):
        self.messages.clear()
