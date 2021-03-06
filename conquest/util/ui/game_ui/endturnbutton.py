from util.constants import Constants
from util.ui.button import Button


class EndTurnButton(Button):

    command = "endTurn"

    def __init__(self, x, y):
        Button.__init__(self, x, y, Constants.END_TURN_BUTTON_WIDTH, Constants.END_TURN_BUTTON_HEIGHT, self.command, "End Turn")