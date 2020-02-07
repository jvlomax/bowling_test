"""
Test suite for the bowling score tracker.
This suite uses the built in unittest library, but import unittest2 for backward compatibility.

TODO: use pytest paramterize
TODO: use hyptohesis
"""
# python2 doesn't have the context manager for self.assertRaises. We use unittest2 to plug this gap.
from unittest2 import TestCase

from bowling import Game, Frame


class TestGame(TestCase):
    def setUp(self):
        """ Pretty much every single test is going to require a game, so we set one up by default."""
        self.game = Game()

    def test_perfect_game(self):
        """If all 10 frames in a game are strike, we should have a perfect game and should score 300."""
        for _ in range(9):
            self.game.add_frame(Frame(10))
        self.game.add_frame(Frame(10, 10, 10))
        self.assertTrue(self.game.is_perfect_game)
        self.assertEqual(self.game.total_scores, 300)
        self.assertFalse(self.game.is_gutter_game)

    def test_gutter_game(self):
        """If no pins were down in the entire game, we should have a gutter game."""
        for _ in range(10):
            self.game.add_frame(Frame(0, 0))

        self.assertTrue(self.game.is_gutter_game)
        self.assertFalse(self.game.is_perfect_game)

    def test_fill_allowed_if_strike(self):
        """Ensure fill frames are allowed is a strike is rolled on the last frame."""
        for _ in range(9):
            self.game.add_frame(Frame(0, 0))
        self.game.add_frame((Frame(10, 10, 10)))    # Last frame has extra rolls because it's a strike

    def test_fill_allowed_if_spare(self):
        """Ensure fill frames are allowed is a spare is rolled on the last frame."""
        for _ in range(9):
            self.game.add_frame(Frame(0, 0))
        self.game.add_frame((Frame(7, 3, 5)))

    def test_fill_not_allowed_if_not_all_down(self):
        """Fill frames are only allowed if all 10 pins come down in the first 2 rolls."""
        for _ in range(9):
            self.game.add_frame(Frame(0, 0))
        with self.assertRaises(AttributeError):
            self.game.add_frame(Frame(2, 3, 9))

    def test_fill_not_allowed_if_not_last(self):
        """Test that a fill frame is only allowed if it's the last roll."""
        self.game.add_frame(Frame(5, 3))
        with self.assertRaises(AttributeError):
            self.game.add_frame(Frame(10, 10, 10))

    def test_addiing_11_frames(self):
        """Only 11 frames are allowed in any one game of 10-pin bowling"""
        for _ in range(10):
            self.game.add_frame(Frame(4, 3))
        # Adding the 11th frame should raise an exception
        with self.assertRaises(IndexError):
            self.game.add_frame(Frame(10))

    def test_score_with_strike(self):
        """Basic test to ensure strikes are calculated correctly.
        This is test by rolling a strike, followed by a (5, 3) and a (6, 3).
        We should have (10 + 5 + 3) + 8 + 9 points"""
        self.game.add_frame(Frame(10))  # Strike
        self.game.add_frame(Frame(5, 3))
        self.game.add_frame(Frame(6, 3))
        self.assertEqual(self.game.total_score, 35)

    def test_consecutive_strikes(self):
        """
        Ensure score is calculated correctly if we roll several strikes in a row.
        The score should be  (10 + 10 + 10) + (10 + 10 + 5) + (10 + 5 + 3) + 8 + 9 == 102.
        """
        self.game.add_frame(Frame(10))  # Strike
        self.game.add_frame(Frame(10))  # Strike
        self.game.add_frame(Frame(10))  # Strike
        self.game.add_frame(Frame(5, 3))
        self.game.add_frame(Frame(6, 3))
        self.assertEqual(self.game.total_score, 90)

    def test_score_with_spare(self):
        """Basic test to ensure spares are calculated correctly.
        This is done by rolling a spare (10 points) + 8 pins.
        We should end up with (10 + 5) + 8 points.
        """
        self.game.add_frame(Frame(6, 4))    # Spare
        self.game.add_frame(Frame(5, 3))
        self.assertEqual(self.game.total_score, 23)

    def test_score_with_consecutive_spares(self):
        """
        Ensure score is calculated correctly if we roll several spares in a row.
        The score should be  (10 + 2) + (10 + 7) + (10 + 5) + 8 == 66.
        """
        self.game.add_frame(Frame(6, 4))  # Spare
        self.game.add_frame(Frame(2, 8))  # Spare
        self.game.add_frame(Frame(7, 3))  # Spare
        self.game.add_frame(Frame(5, 3))
        self.assertEqual(self.game.total_score, 52)

    def test_score_with_strike_spare_combo(self):
        """
        Ensure score is calculated correctly if we mix spares and strikes in consecutive frames.
        The score should be  (10 + 10) + (10 + 7 + 3) + (10 + 10) (10 + 5 + 5) + 10 == 100.
        """
        self.game.add_frame(Frame(6, 4))    # Spare
        self.game.add_frame(Frame(10))      # Strike
        self.game.add_frame(Frame(7, 3))    # Spare
        self.game.add_frame(Frame(10))      # Strike
        self.game.add_frame(Frame(5, 5))    # Spare
        self.assertEqual(self.game.total_score, 100)


class TestFrame(TestCase):
    def test_valid_frames(self):
        """A basic test for frames to make sure no legal frame don't throw assertions."""
        Frame(1, 7)
        Frame(0, 0)
        Frame(10, 0)
        Frame(0, 10)
        Frame(10)
        Frame(10, 4, 10)    # including fill frame

    def test_invalid_frames(self):
        """
        Ensure an exception is raised we we knock down more than 10 pins, a negative number of pins or a fill frame
        without knocking down 10 pins first.
        """
        with self.assertRaises(AttributeError):
            Frame(9, 2)
            Frame(2, 9)
            Frame(-2)
            Frame(5, -3)    # Ensure there is no funky math going on where 5 - 3 == 2 and it's considered valid
            Frame(2, 2, 5)  # Fill frames are only allowed if the first two rolls add up to 10

    def test_strike(self):
        frame = Frame(10)
        self.assertTrue(frame.is_strike)
        self.assertFalse(frame.is_spare)

    def test_spare(self):
        frame = Frame(5, 5)
        self.assertFalse(frame.is_strike)
        self.assertTrue(frame.is_spare)

    def test_open_frame(self):
        """If there is neither a spare or a strike, the frame should be considered an open frame."""
        frame = Frame(2,5)
        self.assertTrue(frame.is_open_frame)

    def test_not_open_frame(self):
        """Ensure that any Spare or strike means the frame is not open."""
        frame = Frame(10)
        self.assertFalse(frame.is_open_frame)
        frame = Frame(5, 5)
        self.assertFalse(frame.is_open_frame)
