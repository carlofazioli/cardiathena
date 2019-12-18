import unittest
from adjudicator.hearts_adjudicator import HeartsAdjudicator
from agent.RandomHeartsAgent import RandomHeartsAgent
from base import GameManager


class TestHeartsState(unittest.TestCase):

    def setUp(self):
        agent_1 = RandomHeartsAgent()
        agent_2 = RandomHeartsAgent()
        agent_3 = RandomHeartsAgent()
        agent_4 = RandomHeartsAgent()
        self.adj = HeartsAdjudicator()
        self.game = GameManager(agent_list=[0, agent_1, agent_2, agent_3, agent_4],
                                adjudicator=self.adj)

    def test_agent_turn_whose_turn(self):
        self.adj.start_game()
        self.adj.state.trick_winner = 4
        self.adj.state.current_player = 4
        self.adj.state.set_encoding(24, '5S')

        agent_index, partial_state = self.adj.agent_turn()
        self.assertEqual(1, agent_index)
        self.adj.state.set_encoding(21, '4H')

        agent_index, partial_state = self.adj.agent_turn()
        self.adj.state.set_encoding(22, '6H')
        self.assertEqual(2, agent_index)

        agent_index, partial_state = self.adj.agent_turn()
        self.adj.state.set_encoding(23, 'JD')
        self.assertEqual(3, agent_index)

        self.adj.state.trick_winner = 2
        agent_index, partial_state = self.adj.agent_turn()
        self.assertEqual(3, agent_index)


if __name__ == "__main__":
    unittest.main()
