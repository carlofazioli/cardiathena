import unittest
from adjudicator.state import HeartsState
import numpy as np


class TestHeartsState(unittest.TestCase):

    def setUp(self):
        self.state = HeartsState()

    def test_shuffle(self):
        self.assertIsNotNone(self.state.values)
        self.assertFalse(np.all(self.state.values == np.array([1] * 13 + [2] * 13 + [3] * 13 + [4] * 13)))

    def test_set_and_get_encoding(self):
        self.state.set_encoding(11, 'AH')
        self.assertEqual(self.state.values[-1], 11)
        self.assertEqual(self.state.get_encoding('AH'), 11)
