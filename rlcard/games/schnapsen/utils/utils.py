class Trick:
    def __init__(self, trump, thirstCard, secondCard):
        self.RANK_TO_STRING = {2: "J", 3: "Q", 4: "K", 10: "T", 11: "A"}

class Moves:
    def get_legal_leader_moves(self, game_engine: 'GamePlayEngine'):# game_state: GameState) -> Iterable[Move]:
        """         # all cards in the hand can be played
        cards_in_hand = game_state.leader.hand
        valid_moves: list[Move] = [RegularMove(card) for card in cards_in_hand]
        # trump exchanges
        if not game_state.talon.is_empty():
            trump_jack = Card.get_card(Rank.JACK, game_state.trump_suit)
            if trump_jack in cards_in_hand:
                valid_moves.append(Trump_Exchange(trump_jack))
        # mariages
        for card in cards_in_hand.filter_rank(Rank.QUEEN):
            king_card = Card.get_card(Rank.KING, card.suit)
            if king_card in cards_in_hand:
                valid_moves.append(Marriage(card, king_card)) """
        valid_moves =  []
        return valid_moves

    def get_legal_follower_moves(self, game_engine: 'GamePlayEngine'):# game_state: GameState, partial_trick: Move) -> Iterable[Move]:
        """         hand = game_state.follower.hand
        if partial_trick.is_marriage():
            leader_card = cast(Marriage, partial_trick).queen_card
        else:
            leader_card = cast(RegularMove, partial_trick).card
        if game_state.game_phase() is GamePhase.ONE:
            # no need to follow, any card in the hand is a legal move
            return RegularMove.from_cards(hand.get_cards())
        # information from https://www.pagat.com/marriage/schnaps.html
        # ## original formulation ##
        # if your opponent leads a non-trump:
        #     you must play a higher card of the same suit if you can;
        #     failing this you must play a lower card of the same suit;
        #     if you have no card of the suit that was led you must play a trump;
        #     if you have no trumps either you may play anything.
        # If your opponent leads a trump:
        #     you must play a higher trump if possible;
        #     if you have no higher trump you must play a lower trump;
        #     if you have no trumps at all you may play anything.
        # ## implemented version, realizing that the rules for trump are overlapping with the normal case ##
        # you must play a higher card of the same suit if you can
        # failing this, you must play a lower card of the same suit;
        # --new--> failing this, if the opponen did not play a trump, you must play a trump
        # failing this, you can play anything
        leader_card_score = game_engine.trick_scorer.rank_to_points(leader_card.rank)
        # you must play a higher card of the same suit if you can;
        same_suit_cards = hand.filter_suit(leader_card.suit)
        if same_suit_cards:
            higher_same_suit, lower_same_suit = [], []
            for card in same_suit_cards:
                # TODO this is slightly ambigousm should this be >= ??
                higher_same_suit.append(card) if game_engine.trick_scorer.rank_to_points(card.rank) > leader_card_score else lower_same_suit.append(card)
            if higher_same_suit:
                return RegularMove.from_cards(higher_same_suit)
        # failing this, you must play a lower card of the same suit;
            elif lower_same_suit:
                return RegularMove.from_cards(lower_same_suit)
            raise AssertionError("Somethign is wrong in the logic here. There should be cards, but they are neither placed in the low, nor higher list")
        # failing this, if the opponen did not play a trump, you must play a trump
        trump_cards = hand.filter_suit(game_state.trump_suit)
        if leader_card.suit != game_state.trump_suit and trump_cards:
            return RegularMove.from_cards(trump_cards)
        # failing this, you can play anything
        return RegularMove.from_cards(hand.get_cards()) """
        return True
    

