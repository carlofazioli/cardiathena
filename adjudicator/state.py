import numpy as np
"""Basic Implementation of the Card Game State"""


class State(object):

    """State DOCSTRING"""

    def __init__(self):
        self.card_vector = np.zeros((1, 52), dtype=int)
        self.Lookup_table = self.build_lookup_table()

    def __repr__(self):
        """ How we want to represent the class"""
        ret = ""
        for row in self.card_vector:
            for column in row:
                ret+=" "+str(column)
        return ret

    """ Change the Encoding of one of the card"""
    def setEncoding(self,encoding , card):
        index = int(self.Lookup_table[card])
        print(index)
        print(self.card_vector.shape)
        self.card_vector[0,index]=encoding

        """Function for the agent . Enter a player from 0-3 and it will blank
        out everything that does not belong to that player"""
    def Hide_encoding(self,player):
        player_1=[1,11,21]
        player_2=[2,12,22]
        player_3=[3,13,23]
        player_4=[4,14,24]
        players = [player_1,player_2,player_3,player_4]
        ret = self.card_vector
        nrow=0
        ncolumn=0
        for row in ret:

            for column in row:
                if column in players[player]:
                    continue
                else:
                    ret[nrow,ncolumn]=0
                ncolumn+=1
            nrow==1

        return ret

    """For now the table data is being read from a taxt file but i 
    think it may be a good idea to hard code this section"""
    def build_lookup_table(self):
        file_db = open("Card_State_Map.txt" , "r+")
        ret = {}
        for line in file_db:
            split = line.split(",")
            ret[split[0]]=split[1]
        return ret

"""Testing"""

Game_State_d = Game_State()
print(Game_State_d)
Game_State_d.setEncoding(11,"2C")
print(Game_State_d)
Game_State_d.setEncoding(20,"AD")
print(Game_State_d)


