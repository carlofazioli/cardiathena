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
        
    def test_hide_encoding(self):
        self.state.set_encoding(12, '5S')
        self.state.set_encoding(13, 'JD')
        self.state.set_encoding(21, '6H')
        expected_p1_state = [i for i in self.state.values]
        self.assertTrue(np.all(self.state.values == np.array(expected_p1_state)))
        for x in range(52):
            if expected_p1_state[x] != 1:
                expected_p1_state[x] = 0

        expected_p1_state[43] = 21
        expected_p1_state[22] = 13
        expected_p1_state[29] = 12
        p1_state = self.state.hide_encoding(1)
        self.assertTrue(np.all(p1_state == np.array(expected_p1_state)))


if __name__ == "__main__":
    unittest.main()
