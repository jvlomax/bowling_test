"""
This file holds the classes required to keep track of a game of bowling.
It tries to straddle the thine line between simple and extensible.

The decision was made early to create a separate Frame class. While it's completely fine and probably simpler
to just have the one Game class and just track the rolls directly on it, I feel having the Frame class
fits the rules of the game more closely. It also allows for additional features like marking split in frames,
resetting frames if there was an issue with it, and other frame specific actions.

It also allows for more idiomatic python by having properties like `frame.is_strike`
"""

# Constants to prevent as many magic numbers hanging around. Pure coincidence that they are the same
MAX_FRAMES = 10
NUM_PINS = 10


class Game:
    def __init__(self):
        # Making frames "private" as we don't want anyone outside the class messing around with it.
        self._frames = []

    @property
    def is_perfect_game(self):
        """
        The game is perfect if all frames are strikes and the score is 300.
        Note: This is slightly expensive since we have to calculate the score all 10 frames.

        :return: True if all frames are strikes and the score is 300
        :rtype: bool
        """
        return all([frame.is_strike for frame in self._frames]) and self.total_score == 300

    @property
    def is_gutter_game(self):
        """
        If there is no score at all, the game is considered a gutter game.
        TODO: Double check bowling rules if it's only conisdered a gutter game if all frames are complete

        :return: True if there is currently no score for this game
        :rtype: bool
        """
        return self.total_score == 0

    @property
    def total_score(self):
        """
        Calculates the total score for this game.

        The score is not stored anywhere and is just calculated on the fly. This is not meant to be quick.
        If this is going to be used in production, we should start storing the total score as a class attribute either
        on the game object, or on each individual frame instead.

        :return: The total score for this game in it's current state
        :rtype: int
        """
        score = 0
        for idx, frame in enumerate(self._frames):
            # Process scoring rules for a strike
            if frame.is_strike:
                score += sum(frame.rolls)
                # We also want to add the next two rolls if they exist
                if len(self._frames) > (idx + 1):
                    score += sum(self._frames[idx + 1].rolls[:2])

                    # If that next frame happened to be a strike,
                    # we also need look at the next next frame to get the first roll from it
                    if self._frames[idx + 1].is_strike and len(self._frames) > (idx + 2):
                        score += self._frames[idx + 2].rolls[0]

            # Process rule for a spare
            elif frame.is_spare:
                score += sum(frame.rolls)
                # If the next frame exists, we get the first roll from it, and add it to the score for this frame.
                if len(self._frames) > idx + 1:
                    score += self._frames[idx + 1].rolls[0]
            # for open frames, we just add the sum of the rolls
            else:
                score += sum(frame.rolls)

        return score

    def add_frame(self, frame):
        """
        This adds a frame to the game.

        :param Frame frame: A frame with 1 or 2 rolls to add to the game.
        :raises IndexError: If more than 10 frames are attempted to be added.
        :raises AttributeError: If there are 3 rolls in the frame, but the 10 pins were not downed in the first 2 rolls
                                OR this is not the last frame.
        """
        if len(self._frames) >= MAX_FRAMES:
            raise IndexError('Can not add more than {} frames to a game'.format(MAX_FRAMES))

        # The last roll is the fill roll. It can only be added as the last frame.
        if frame.rolls[-1]:
            if len(self._frames) != MAX_FRAMES - 1 or not sum(frame.rolls[:2]) >= NUM_PINS:
                raise AttributeError(
                    'Extra rolls are only allowed as the last roll, or if all 10 pins were downed in the first 2 throws'
                )
        self._frames.append(frame)


class Frame:
    """
    While it would be simpler to just store everything in a game class, having a separate Frame class
    allows us more freedom to do things like delete frames, edit frames, check for open frames and more.
    Not needed for this tech test, but it makes the code a lot more extensible and allows for additional post review
    features.

    This class is meant to be fairly dumb, and just server as a container for the rolls. All the as much logic
    as possible should be in the Game class.
    """
    def __init__(self, roll1, roll2=0, fill_roll=0):
        """
        The number in the rolls need to add up to no more than 10. The first roll should always exist, but he second
        roll does not exist if the frame is a strike.
        :param int roll1: The number of pins won in the first roll.
        :param int roll2:  The number of pins on the second roll.
        :param int fill_roll: Only used in the last frame if a player gets a spare or a strike.
        :raises AttributeError: raises and exception if the number of pins the total number of pins is over 10
                                or is negative
        """
        if (roll1 + roll2 > 10 and not fill_roll) or roll1 < 0 or roll2 < 0:
            raise AttributeError('The sum of first tww rolls must be between 0 and 10')
        if fill_roll > 10 or fill_roll < 0:
            raise AttributeError('The fill roll can only be between 0 and 10')

        self.rolls = [roll1, roll2, fill_roll]

    def __repr__(self):
        return str(self.rolls)

    @property
    def is_open_frame(self):
        """
        Is this frame an open frame, meaning not a strike or a spare?
        :return: True if all there is no strike or spare in the frame.
        :rtype: bool
        """
        return sum(self.rolls) < 10

    @property
    def is_strike(self):
        """
        Were all the pins knocked down in the first roll?
        :return: True if this frame is a strike
        :rtype: bool
        """
        return self.rolls[0] == 10

    @property
    def is_spare(self):
        """
        Were all the pins knocked down on the second roll?
        :return: True if this frame is a spare
        :rtype: bool
        """
        return sum(self.rolls[:2]) == 10 and not self.is_strike
