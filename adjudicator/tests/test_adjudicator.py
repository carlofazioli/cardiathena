import unittest
from adjudicator.hearts_adjudicator import HeartsAdjudicator
from agent.RandomHeartsAgent import RandomHeartsAgent
from agent.RandomHeartsAgent import HeartsAction
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
        self.adj.state.set_encoding(24, 'JS')

        agent_index, partial_state = self.adj.agent_turn()
        self.assertEqual(1, agent_index)
        self.adj.state.set_encoding(21, '4H')

        agent_index, partial_state = self.adj.agent_turn()
        self.adj.state.set_encoding(22, '6H')
        self.assertEqual(2, agent_index)

        agent_index, partial_state = self.adj.agent_turn()
        self.adj.state.set_encoding(23, '5S')
        self.assertEqual(3, agent_index)

        self.adj.state.trick_winner = 2
        agent_index, partial_state = self.adj.agent_turn()
        self.assertEqual(3, agent_index)

    def test_find_max(self):
        adj = HeartsAdjudicator()
        adj.start_game()
        # should ignore that obnoxious value
        fake_action = HeartsAction(100000)
        adj.step_game(fake_action)

        fake_action.card_index = 0
        adj.step_game(fake_action)

        fake_action.card_index = 38
        adj.step_game(fake_action)

        fake_action.card_index = 50
        adj.step_game(fake_action)

        fake_action.card_index = 20
        adj.step_game(fake_action)

if __name__ == "__main__":
    unittest.main()
