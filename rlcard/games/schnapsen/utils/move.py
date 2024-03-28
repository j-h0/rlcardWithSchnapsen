class Moves:
    def get_legal_leader_moves(self, game_engine: 'GamePlayEngine', game_state: GameState) -> Iterable[Move]:
        # all cards in the hand can be played
        cards_in_hand = game_state.leader.hand
        valid_moves: list[Move] = [RegularMove(card) for card in cards_in_hand]
        # trump exchanges
        if not game_state.talon.is_empty():
            trump_jack = Card.get_card(Rank.JACK, game_state.trump_suit)
            if trump_jack in cards_in_hand:
                valid_moves.append(Trump_Exchange(trump_jack))
        # marriages
        for card in cards_in_hand.filter_rank(Rank.QUEEN):
            king_card = Card.get_card(Rank.KING, card.suit)
            if king_card in cards_in_hand:
                valid_moves.append(Marriage(card, king_card))
            return valid_moves
        

    def get_legal_follower_moves(self, game_engine: 'GamePlayEngine', game_state: GameState, partial_trick: Move) -> Iterable[Move]:
        hand = game_state.follower.hand
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
        return RegularMove.from_cards(hand.get_cards())
    

class Move(ABC):
    """
    A single move during a game. There are several types of move possible: normal moves, trump exchanges, and marriages. They are implmented in classes inheriting from this class.
    """

    cards: list[Card]  # implementation detail: The creation of this list is defered to the derived classes in _cards()
    """The cards played in this move"""

    def is_regular_move(self) -> bool:
        """
        Is this Move a regular move (not a mariage or trump exchange)

        :returns: a bool indicating whether this is a regular move
        """
        return False

    def as_regular_move(self) -> 'RegularMove':
        """Returns this same move but as a Marriage."""
        raise AssertionError("as_regular_move called on a Move which is not a regular move. Check with is_regular_move first.")

    def is_marriage(self) -> bool:
        """
        Is this Move a marriage?

        :returns: a bool indicating whether this move is a marriage
        """
        return False

    def as_marriage(self) -> 'Marriage':
        """Returns this same move but as a Marriage."""
        raise AssertionError("as_marriage called on a Move which is not a Marriage. Check with is_marriage first.")

    def is_trump_exchange(self) -> bool:
        """
        Is this Move a trump exchange move?

        :returns: a bool indicating whether this move is a trump exchange
        """
        return False

    def as_trump_exchange(self) -> 'Trump_Exchange':
        """Returns this same move but as a Trump_Exchange."""
        raise AssertionError("as_marriage called on a Move which is not a Trump_Exchange. Check with is_trump_exchange first.")

    def __getattribute__(self, __name: str) -> Any:
        if __name == "cards":
            # We call the method to compute the card list
            return object.__getattribute__(self, "_cards")()
        return object.__getattribute__(self, __name)

    @abstractmethod
    def _cards(self) -> list[Card]:
        """
        Get the list of cards in this move. This method should not be called direcly, use the cards property instead.
        """


@dataclass(frozen=True)
class Trump_Exchange(Move):
    """A move that implements the exchange of the trump card for a Jack of the same suit."""

    jack: Card
    """The Jack which will be placed at the bottom of the Talon"""

    def __post_init__(self) -> None:
        assert self.jack.rank is Rank.JACK

    def is_trump_exchange(self) -> bool:
        return True

    def as_trump_exchange(self) -> 'Trump_Exchange':
        return self

    def _cards(self) -> list[Card]:
        return [self.jack]

    def __repr__(self) -> str:
        return f"Trump_Exchange(jack={self.jack})"


@dataclass(frozen=True)
class RegularMove(Move):
    """A regular move in the game"""

    card: Card
    """The card which is played"""

    def _cards(self) -> list[Card]:
        return [self.card]

    @staticmethod
    def from_cards(cards: Iterable[Card]) -> list[Move]:
        """Create an iterable of Moves from an iterable of cards."""
        return [RegularMove(card) for card in cards]

    def is_regular_move(self) -> bool:
        return True

    def as_regular_move(self) -> 'RegularMove':
        return self

    def __repr__(self) -> str:
        return f"RegularMove(card={self.card})"


@dataclass(frozen=True)
class Marriage(Move):
    """
    A Move representing a marriage in the game. This move has two cards, a king and a queen of the same suit.
    Right after the marriage is played, the player must play either the queen or the king.
    Because it can only be beneficial to play the queen, it is chosen automatically.
    This Regular move is part of this Move already and does not have to be played separatly.
    """
    queen_card: Card
    """The queen card of this marriage"""
    king_card: Card
    """The king card of this marriage"""
    suit: Suit = field(init=False, repr=False, hash=False)
    """The suit of this marriage, gets derived from the suit of the queen and king."""

    def __post_init__(self) -> None:
        """
        Make sure that the suits of the fields all have the same suit and are a king and a queen.
        Finally, sets the suit field.
        """
        assert self.queen_card.rank is Rank.QUEEN
        assert self.king_card.rank is Rank.KING
        assert self.queen_card.suit == self.king_card.suit
        object.__setattr__(self, "suit", self.queen_card.suit)

    def is_marriage(self) -> bool:
        return True

    def as_marriage(self) -> 'Marriage':
        return self

    def underlying_regular_move(self) -> RegularMove:
        """
        Get the regular move which was played because of the marriage. In this engine this is always the queen card.
        """
        # this limits you to only have the queen to play after a marriage, while in general you would have a choice.
        # This is not an issue since playing the queen give you the highest score.
        return RegularMove(self.queen_card)

    def _cards(self) -> list[Card]:
        return [self.queen_card, self.king_card]

    def __repr__(self) -> str:
        return f"Marriage(queen_card={self.queen_card}, king_card={self.king_card})"
