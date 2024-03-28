from rlcard.games.schnapsen.schnapsencard import SchnapsenCard

from . import utils as utils

# ====================================
# Action_ids:
#        0 -> trump_exchange
#        1 -> marriage
#        2 -> sixsix
#        3 -> close_talon
#        24 to 27 -> play_card
# ====================================

trump_exchange_action_id = 0
marriage_action_id = 1 # +4 suits 
sixsix_action_id = 5
close_action_id = 6
play_card_action_id = 7


class ActionEvent(object):

    def __init__(self, action_id: int):
        self.action_id = action_id

    def __eq__(self, other):
        result = False
        if isinstance(other, ActionEvent):
            result = self.action_id == other.action_id
        return result

    @staticmethod
    def get_num_actions():
        ''' Return the number of possible actions in the game
        '''
        return close_action_id + 20  

    @staticmethod
    def decode_action(action_id: int) -> 'ActionEvent':
        ''' Action id -> the action_event in the game.

        Args:
            action_id (int): the id of the action

        Returns:
            action (ActionEvent): the action that will be passed to the game engine.
        '''
        if action_id == trump_exchange_action_id:
            action_event = TrumpExchangePlayerAction()
        elif action_id in range(marriage_action_id, marriage_action_id + 4):
            suit_id = action_id - marriage_action_id
            action_event = MarriagePlayerAction(suit = suit_id)
        elif action_id == sixsix_action_id:
            action_event = SixsixAction()
        elif action_id == close_action_id:
            action_event = CloseTalonAction()
        elif action_id in range(play_card_action_id, sixsix_action_id + 24):
            card_id = action_id - play_card_action_id
            card = SchnapsenCard.card(card_id)
            action_event = PlayCardAction(card=card)
        else:
            raise Exception("decode_action: unknown action_id={}".format(action_id))
        return action_event


class TrumpExchangePlayerAction(ActionEvent):

    def __init__(self):
        super().__init__(action_id=trump_exchange_action_id)

    def __str__(self):
        return "trumpexchange"


class MarriagePlayerAction(ActionEvent):

    def __init__(self, suit: int):
        
        super().__init__(action_id=marriage_action_id+suit)
        self.suit = suit

    def __str__(self):
        return "marriage"


class SixsixAction(ActionEvent):

    def __init__(self):
        super().__init__(action_id=sixsix_action_id)

    def __str__(self):
        return "six_six"


class PlayCardAction(ActionEvent):

    def __init__(self, card: SchnapsenCard):
        card_id = card.get_card_id()
        super().__init__(action_id=play_card_action_id + card_id)
        self.card = card

    def __str__(self):
        return "Play {}".format(str(self.card)) 

class CloseTalonAction(ActionEvent):

    def __init__(self):
        super().__init__(action_id=close_action_id)

    def __str__(self):
        return "Close Talon" 