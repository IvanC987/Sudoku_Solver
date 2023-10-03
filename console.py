import pygame as py


class Console:
    def __init__(self, screen, x, y, width, height, font, max_lines=10):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.max_lines = max_lines  # Maximum number of lines to display
        self.messages = []  # Store the messages

    def add_message(self, text, color):
        # Add a new message to the console
        self.messages.append((text, color))
        # Ensure that the number of messages doesn't exceed the maximum
        if len(self.messages) > self.max_lines:
            self.messages.pop(0)  # Remove the oldest message

    def draw(self):
        # Draw the console background
        py.draw.rect(self.screen, py.Color("#FFFAC7"), py.Rect(self.x, self.y, self.width, self.height))
        py.draw.rect(self.screen, py.Color("black"), py.Rect(self.x, self.y, self.width, self.height), 2)

        # Display the messages within the console bounds
        y_offset = self.height - self.font.get_height() - 5
        for message, color in reversed(self.messages):
            text_surface = self.font.render(message, True, color)
            self.screen.blit(text_surface, (self.x + 5, self.y + y_offset))
            y_offset -= self.font.get_height()  # Move up for the next message
