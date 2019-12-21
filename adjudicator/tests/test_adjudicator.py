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

    def test_pass_round(self):
        round_number = 0
        self.adj.start_game()
        while not self.adj.is_finished():
            # New round, check passing
            if self.adj.lead_suit == -2:
                for i in range(0, 4):
                    agent_index, partial_state = self.adj.agent_turn()
                    p_action = self.game.agent_list[agent_index].get_action(partial_state)
                    state = self.adj.step_game(p_action)
                round_number += 1
                print(round_number)
                # Passing CW
                if self.adj.state.pass_type == 0:
                    self.assertTrue(list(x for x in self.adj.pass_actions[0] if self.adj.state.values[x] == 2))
                    self.assertTrue(list(x for x in self.adj.pass_actions[1] if self.adj.state.values[x] == 3))
                    self.assertTrue(list(x for x in self.adj.pass_actions[2] if self.adj.state.values[x] == 4))
                    self.assertTrue(list(x for x in self.adj.pass_actions[3] if self.adj.state.values[x] == 1))
                # Passing CCW
                elif self.adj.state.pass_type == 1:
                    self.assertTrue(list(x for x in self.adj.pass_actions[0] if self.adj.state.values[x] == 4))
                    self.assertTrue(list(x for x in self.adj.pass_actions[1] if self.adj.state.values[x] == 1))
                    self.assertTrue(list(x for x in self.adj.pass_actions[2] if self.adj.state.values[x] == 2))
                    self.assertTrue(list(x for x in self.adj.pass_actions[3] if self.adj.state.values[x] == 3))
                # Passing Straight
                elif self.adj.state.pass_type == 2:
                    self.assertTrue(list(x for x in self.adj.pass_actions[0] if self.adj.state.values[x] == 3))
                    self.assertTrue(list(x for x in self.adj.pass_actions[1] if self.adj.state.values[x] == 4))
                    self.assertTrue(list(x for x in self.adj.pass_actions[2] if self.adj.state.values[x] == 1))
                    self.assertTrue(list(x for x in self.adj.pass_actions[3] if self.adj.state.values[x] == 2))
                # No pass
                elif self.adj.state.pass_type == 3:
                    self.assertTrue(list(x for x in self.adj.pass_actions[0] if self.adj.state.values[x] == 1))
                    self.assertTrue(list(x for x in self.adj.pass_actions[1] if self.adj.state.values[x] == 2))
                    self.assertTrue(list(x for x in self.adj.pass_actions[2] if self.adj.state.values[x] == 3))
                    self.assertTrue(list(x for x in self.adj.pass_actions[3] if self.adj.state.values[x] == 4))

            agent_index, partial_state = self.adj.agent_turn()
            p_action = self.game.agent_list[agent_index].get_action(partial_state)
            state = self.adj.step_game(p_action)

    def test_player_turns_trick_winner(self):
        self.adj.start_game()
        # Set Trick 1, player 4 wins trick
        self.adj.state.set_encoding(11, '2C')
        self.adj.state.set_encoding(12, '3C')
        self.adj.state.set_encoding(13, '4C')
        self.adj.state.set_encoding(14, '5C')
        self.adj.state.trick_winner = 4
        self.adj.state.trick_number = 2
        self.adj.state.current_player = 4
        self.adj.lead_suit = 0
        self.assertEqual(4, self.adj.state.current_player)

        # Set Trick 2, player 4 plays, player 1 is next player
        agent_index, partial_state = self.adj.agent_turn()
        p_action = self.game.agent_list[agent_index].get_action(partial_state)
        state = self.adj.step_game(p_action)
        self.assertEqual(1, state.current_player)

        # Player 1 plays, player 2 is next player
        agent_index, partial_state = self.adj.agent_turn()
        p_action = self.game.agent_list[agent_index].get_action(partial_state)
        state = self.adj.step_game(p_action)
        self.assertEqual(2, state.current_player)

        # Player 1 plays, player 2 is next player
        agent_index, partial_state = self.adj.agent_turn()
        p_action = self.game.agent_list[agent_index].get_action(partial_state)
        state = self.adj.step_game(p_action)
        self.assertEqual(3, state.current_player)

        # Player 4 plays, trick_winner is the next player and starts next trick
        agent_index, partial_state = self.adj.agent_turn()
        p_action = self.game.agent_list[agent_index].get_action(partial_state)
        state = self.adj.step_game(p_action)
        self.assertEqual(state.trick_winner, state.current_player)

"""

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
"""

if __name__ == "__main__":
    unittest.main()
