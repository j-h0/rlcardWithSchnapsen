from rlcard.games.schnapsen.schnapsencard import SchnapsenCard


class SchnapsenRound:

    def __init__(self, dealer, num_players, np_random):
    ''' Initialize the round class

    Args:
        dealer (object): the object of UnoDealer
        num_players (int): the number of players in game
    '''
    self.np_random = np_random
    self.dealer = dealer
    self.target = None
    self.current_player = 0
    self.num_players = num_players
    self.direction = 1
    self.played_cards = []
    self.is_over = False
    self.winner = None

    def get_current_player(self) -> GinRummyPlayer or None:
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

    def trumpUnter(self, action: TrumpUnterAction):

    def closing(self, action: ClosingAction):

    def claimSixSix(self, action: SixSixAction):