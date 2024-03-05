
class SchnapsenJudger:

    def __init__(self):
        self.np_random = 1

    def judge_game(self, players, hands):

        """     if game_state.leader.score.direct_points >= 66:
            follower_score = game_state.follower.score.direct_points
            if follower_score == 0:
                return game_state.leader, 3
            elif follower_score >= 33:
                return game_state.leader, 1
            else:
                # second case in explaination above, 0 < score < 33
                assert follower_score < 66
                return game_state.leader, 2
        elif game_state.follower.score.direct_points >= 66:
            raise AssertionError("Would declare the follower winner, but this should never happen in the current implementation")
        elif game_state.are_all_cards_played():
            return game_state.leader, 1
        else:
            return None """
        return None

    
    def judge_trick(self, thirstCard, secondCard):

        """         leader_card = regular_leader_move.card
        follower_card = trick.follower_move.card

        #https://github.com/intelligent-systems-course/schnapsen
        if leader_card.suit is follower_card.suit:
            if leader_card.rank > follower_card.rank:
                leader_wins = True
            else:
                leader_wins = False    

        elif leader_card.suit is trump:
            # the follower suit cannot be trumps as per the previous condition
            leader_wins = True

        elif follower_card.suit is trump:
            # the leader suit cannot be trumps because of the previous conditions
            leader_wins = False

        else:
            # the follower did not follow the suit of the leader and did not play trumps, hence the leader wins
            leader_wins = True

        winner, loser = (leader, follower) if leader_wins else (follower, leader)
        # record the win
        winner.won_cards.extend([leader_card, follower_card])
        # apply the points
        points_gained = leader_card_points + follower_card_points
        winner.score += Score(direct_points=points_gained)
        # add winner's total of direct and pending points as their new direct points
        winner.score = winner.score.redeem_pending_points()
        return winner, loser, leader_wins     """
        return True,True,True