import unittest
from adjudicator.state import State
import numpy as np


class TestState(unittest.TestCase):

    def setUp(self):
        self.state = State()

    def test_shuffle(self):
        self.assertIsNotNone(self.state.card_vector)
        self.assertFalse(np.all(self.state.card_vector == np.array([1] * 13 + [2] * 13 + [3] * 13 + [4] * 13)))

    def test_set_and_get_encoding(self):
        self.state.set_encoding(11, 'AH')
        self.assertEqual(self.state.card_vector[-1], 11)
        self.assertEqual(self.state.get_encoding('AH'), 11)
