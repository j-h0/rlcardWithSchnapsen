from rlcard.games.schnapsen.schnapsencard import SchnapsenCard
from rlcard.games.schnapsen.dealer import SchnapsenDealer
from .player import SchnapsenPlayer



class SchnapsenRound:

    def __init__(self, dealer_id: int, num_players, np_random):
        ''' Initialize the round class

        The round class maintains the following instances:
            1) dealer: the dealer of the round; dealer has stock_pile and discard_pile
            2) players: the players in the round; each player has his own hand_pile
            3) current_player_id: the id of the current player who has the move
            4) is_over: true if the round is over
            5) going_out_action: knock or gin or None
            6) going_out_player_id: id of player who went out or None
            7) move_sheet: history of the moves of the player (including the deal_hand_move)

        Args:
            dealer (object): the object of UnoDealer
            num_players (int): the number of players in game
        '''
        self.np_random = np_random
        self.dealer_id = dealer_id
        self.dealer = SchnapsenDealer
        self.target = None
        self.is_closed = False
        self.current_player_id = (dealer_id + 1) % 2
        self.is_over = False
        shuffled_deck = self.dealer.shuffled_deck
        self.tricks = {}
        self.winner = None

    def get_current_player(self) -> SChna or None:
        current_player_id = self.current_player_id
        return None if current_player_id is None else self.players[current_player_id]

    def draw_card(self, action: DrawCardAction):
        if(self.is_closed):
            return
        if(len(self.dealer.stock_pile) <= 0):
            is_closed = True
            return
        
        current_player = self.players[self.current_player_id]
        card = self.dealer.stock_pile.pop()
        current_player.hand.append(card=card)

    def marriage(self, action: M
        self.np_random = np_randomarriageAction):
        self.np_random = np_random
    def trumpExchange(self, action: TrumpExchangeAction):
        current_player = self.players[self.current_player_id]
        card = current_player.hand.remove(action.card)
        card = self.dealer.trumpExchange(card)
        current_player.hand.append(card)

    def closing(self, action: ClosingAction):
        self.is_closed = True
        return None

    def claimSixSix(self, action: SixSixAction):
        self.is_over = True
        return None
    
    def playCard(self, action: PlayCardAction):

    
    def get_legal_actions(self, players, player_id, is_first)
        legal_actions = []
        playable_cards = []
        hand = players[player_id].hand

        

        if(is_first):
            if(sum(self.tricks[player_id]) >= 66):
                legal_actions.append(SixSixAction)
        else:
            if(self.is_closed):

                #maybe get playablecards function
                for index, card in enumerate(hand):
                    if(card.suit == played_card_suit):
                        playable_cards.append(index)




