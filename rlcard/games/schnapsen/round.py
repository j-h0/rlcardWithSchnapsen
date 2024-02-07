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
        self.current_player_id = (dealer_id + 1) % 2
        self.is_over = False
        shuffled_deck = self.dealer.shuffled_deck
        self.played_cards = []
        self.is_over = False
        self.winner = None

    def get_current_player(self) -> SChna or None:
        current_player_id = self.current_player_id
        return None if current_player_id is None else self.players[current_player_id]

    def draw_card(self, action: DrawCardAction):
        # when current_player takes DrawCardAction step, the move is recorded and executed
        # current_player keeps turn
        current_player = self.players[self.current_player_id]
        if not len(current_player.hand) == 10:
            raise GinRummyProgramError("len(current_player.hand) is {}: should be 10.".format(len(current_player.hand)))
        card = self.dealer.stock_pile.pop()
        self.move_sheet.append(DrawCardMove(current_player, action=action, card=card))
        current_player.add_card_to_hand(card=card)

    def marriage(self, action: MarriageAction):
        return None

    def trumpExchange(self, action: TrumpExchangeAction):
        current_player = self.players[self.current_player_id]
        card = current_player.hand.remove(action.card)
        card = self.dealer.trumpExchange(card)
        current_player.hand.append(card)

    def closing(self, action: ClosingAction):
        return None

    def claimSixSix(self, action: SixSixAction):
        return None