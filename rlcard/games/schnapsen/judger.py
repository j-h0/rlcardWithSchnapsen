
class SchnapsenJudger:

    def __init__(self):
        self.np_random = 1

    def judge_game(self, leader, follower, emptydeck):

        if emptydeck:
            return 1,-1
    
        if leader.score >= 66:
            follower_score = follower.score
            if follower_score == 0:
                return 3,-3
            elif follower_score >= 33:
                return 1,-1
            else:
                # second case in explaination above, 0 < score < 33
                assert follower_score < 66
                return 2,-2
        else:
            return None 

    
    def judge_trick(leader,follower,current_trick,trumpSuit):

        leader_card = current_trick[0]
        follower_card = current_trick[1]

        #https://github.com/intelligent-systems-course/schnapsen
        if leader_card.suit is follower_card.suit:
            if leader_card.rank > follower_card.rank:
                leader_wins = True
            else:
                leader_wins = False    

        elif leader_card.suit is trumpSuit:
            # the follower suit cannot be trumps as per the previous condition
            leader_wins = True

        elif follower_card.suit is trumpSuit:
            # the leader suit cannot be trumps because of the previous conditions
            leader_wins = False

        else:
            # the follower did not follow the suit of the leader and did not play trumps, hence the leader wins
            leader_wins = True

        winner, loser = (leader, follower) if leader_wins else (follower, leader)
        # record the win
        # add winner's total of direct and pending points as their new direct points
        return winner, loser, leader_wins