from rlcard.games.schnapsen.schnapsencard import SchnapsenCard as Card
from rlcard.games.schnapsen.utils.schnapsen_action_event import ActionEvent, PlayCardAction, TrumpExchangePlayerAction, MarriagePlayerAction, SixsixAction
from dataclasses import dataclass, field
from enum import Enum
from random import Random
from typing import Iterable, List, Optional, Tuple, Union, cast, Any
import numpy as np

def filter_hand_by_suit(hand, suit):
        suited_handcards = []
        for card in hand:
            if card.suit == suit:
                suited_handcards.append(card)
        return suited_handcards

def filter_hand(hand, rank, suit = None):
        suited_handcards = []
        for card in hand:
            if card.rank == rank:
                if(suit is None):
                    suited_handcards.append(card)
                else:
                    if card.suit == suit:
                        suited_handcards.append(card)
        return suited_handcards

def getPlayCardMoves(hand):
    valid_moves = []
    for card in hand:
        valid_moves.append(PlayCardAction(card=card))
    return valid_moves    

class Moves:
    def get_legal_leader_moves(game_state, current_player) -> Iterable[ActionEvent]:

        hand = current_player.hand
        if not hand:
            return []
        valid_moves = getPlayCardMoves(hand)

        # trump exchanges
        if not game_state['is_closed']:
            trump_jack = filter_hand(hand,2,game_state['trump_suit'])
            if trump_jack:
                valid_moves.append(TrumpExchangePlayerAction())
            if(current_player.points >= 66):
                valid_moves.append(SixsixAction())
        # mariages
        for card in filter_hand(hand,3):
            king_card = filter_hand(hand,4,card.suit)
            if king_card:
                suitIndex = card.get_suit_idx()
                valid_moves.append(MarriagePlayerAction(suit = suitIndex))

        return valid_moves

    def get_legal_follower_moves(game_state, hand) -> Iterable[ActionEvent]:
        valid_moves = []
        if not game_state['is_closed']:
            # no need to follow, any card in the hand is a legal move
            return getPlayCardMoves(hand)    
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
        #     if you have no trumps at all you may p
        # ## implemented version, realizing that the rules for trump are overlapping with the normal case ##
        # you must play a higher card of the same suit if you can
        # failing this, you must play a lower card of the same suit;
        # --new--> failing this, if the opponen did not play a trump, you must play a trump
        # failing this, you can play anything
        leader_card = game_state['current_trick'][0]
        # you must play a higher card of the same suit if you can;
        same_suit_cards = filter_hand_by_suit(hand,leader_card.suit)
        if same_suit_cards:
            higher_same_suit, lower_same_suit = [], []
            for card in same_suit_cards:
                higher_same_suit.append(card) if card.rank > leader_card.rank else lower_same_suit.append(card)
            if higher_same_suit:
                return getPlayCardMoves(higher_same_suit)
        # failing this, you must play a lower card of the same suit;
            elif lower_same_suit:
                return getPlayCardMoves(lower_same_suit)
        # failing this, if the opponen did not play a trump, you must play a trump
        trump_cards = filter_hand_by_suit(hand,game_state['trump_suit'])
        if leader_card.suit != game_state['trump_suit'] and trump_cards:
            return getPlayCardMoves(trump_cards)
        # failing this, you can play anything
        return getPlayCardMoves(hand)


def decode_cards(env_cards: np.ndarray) -> List[Card]:
    result = []  # type: List[Card]
    for i in range(20):
        if env_cards[i] == 1:
            card = _deck[i]
            result.append(card)
    return result


def encode_cards(cards,is_closed) -> np.ndarray:
    plane = np.zeros(21, dtype=int)
    plane[20] = is_closed
    
    for card in cards:
        card_id = card.get_card_id()
        plane[card_id] = 1    
    return plane