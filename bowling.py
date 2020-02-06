"""
This file holds the classes required to keep track of a game of bowling.
It tries to straddle the thine line between simple and extensible.
"""


class Game:
    def __init__(self):
        self.frames = []

    @property
    def is_perfect_game(self):
        """The game is perfect if all frames are strokes and/or the score is 300"""
        pass

    @property
    def total_scores(self):
        """Calculates the total score for this game.
        The score is not stored anywhere and is just calculated on the fly. This is not meant to be performant.
        If this is going to be used in production, we should start storing the total score as a class attribue instead.
        """
        pass

    def add_frame(self, frame):
        """
        This adds a frame to the game.
        :param Frame frame: A frame with 1 or 2 rolls to add to the game
        :raises IndexError: If more than 10 frames are attempted to be added
        """
        pass


class Frame:
    """
    While it would be simpler to just store everything in a game class, having a separate Frame class
    allows us more freedom to do things like delete frames, edit frames, check for open frames and more.
    Not needed for this test, but it makes the code a lot more extensible.
    """
    def __init__(self, roll1, roll2=None):
        """
        The number in the rolls need to add up to no more than 10. The first roll should always exist, but he second
        roll does not exist if the frame is a strike.
        :param int roll1: The number of pins won in the first roll. Can also be 'strike'
        :param int roll2:  The number of pins on the second roll. Can also be 'spare'
        """
        self.rolls[roll1, roll2]

    @property
    def is_open_frame(self):
        """
        Is this frame an open frame, meaning not a strike or a spare?
        :return: True if all there is no strike or spare in the frame.
        :rtype: bool
        """
        pass

    @property
    def is_strike(self):
        """
        Were all the pins knocked down in the first roll?
        :return: True if this frame is a strike
        :rtype: bool
        """
        pass

    @property
    def is_spare(self):
        """
        Were all the pins knocked down on the second roll?
        :return: True if this frame is a spare
        :rtype: bool
        """
        return

