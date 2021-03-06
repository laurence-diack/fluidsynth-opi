import os
import threading

from oled.device import ssd1306
from oled.render import canvas
from PIL import ImageFont, ImageDraw

class Menu:

    def __init__(self, options=[]):
        self.options = options
        self.highlightOption = None
        self.rowCount = 6

        self.oled = ssd1306(port=3, address=0x3C)

        self.font = ImageFont.truetype('fonts/mobitec.ttf', 8)

        self.renderThread = None

    def set_options(self, options):
        self.options = options
        self.highlightOption = None

    def set_highlight(self, highlight):
        if highlight is None:
            self.highlightOption = None
        elif highlight < 0:
            self.highlightOption = 0
        elif highlight >= len(self.options):
            self.highlightOption = len(self.options) - 1
        else:
            self.highlightOption = highlight

    def change_highlight(self, by):
        self.set_highlight(0 if self.highlightOption is None else self.highlightOption + by)

    def blank(self, draw=False):
        with canvas(self.oled) as draw:
            draw.rectangle((-1, -1, self.oled.width+1, self.oled.height+1), outline=0, fill=0)

    def render(self):
        if self.renderThread is None or not self.renderThread.isAlive():
            self.renderThread = threading.Thread(target=self.__render)
            self.renderThread.start()

    def __render(self):
        self.blank()
        self.__build()

    def __build(self):
        # adjust the start/end positions of the range
        if (self.highlightOption is None) or (self.highlightOption < self.rowCount):
            start = 0
            end = self.rowCount
        elif self.highlightOption >= (len(self.options) - self.rowCount):
            end = len(self.options)
            start = end - self.rowCount
        else:
            start = self.highlightOption
            end = start + self.rowCount

        # draw the menu options
        with canvas(self.oled) as draw:
            top = 0
            for x in range(start, end):
                fill = 1
                if self.highlightOption is not None and self.highlightOption == x:
                    self.draw.rectangle([0, top, self.oled.width, top + 11], outline=0, fill=1)
                    fill = 0
                draw.text((3, top + 1), self.options[x], font=self.font, fill=fill)
                top += 10
