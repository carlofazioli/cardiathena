import numpy as np

def trick_lead(cards_played):

    # cards_played = self.state.values[self.state.values > 20]
    cards_played_length = len(cards_played) - 1

    # no cards have been played yet, no trick leader can be inferred
    if len(cards_played) == 0:
        print("empty")
        return None

    # All for players have played, trick leader can no longer be inferred
    if len(cards_played) == 4:
        print("Can't infer trick leader")
        return None

    sorted_cards_played = np.sort(cards_played)
    print(sorted_cards_played)

    # Find trick leader
    for i in range(0, cards_played_length):
        if (sorted_cards_played[i + 1] - sorted_cards_played[i]) >= 2:
            return sorted_cards_played[i+1]
        elif i == cards_played_length - 1:
            return sorted_cards_played[0]


# Change the values of cards_played to test
cards_played = [24, 21, 22, 23]
values = np.array(cards_played)
print(trick_lead(values))

