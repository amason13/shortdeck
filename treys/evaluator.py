import itertools
from .card import Card
from .deck import Deck
from .lookup import LookupTable

class Evaluator(object):
    """
    Evaluates hand strengths using a variant of Cactus Kev's algorithm:
    http://suffe.cool/poker/evaluator.html

    I make considerable optimizations in terms of speed and memory usage, 
    in fact the lookup table generation can be done in under a second and 
    consequent evaluations are very fast. Won't beat C, but very fast as 
    all calculations are done with bit arithmetic and table lookups. 
    """

    def __init__(self):
        
        self.table = LookupTable()
        
    def SHORTmap(self,hr):
        if hr == 747: #A6789 of a suit becomes a straight flush of rank 56789 suited
            hr = 6
        # swap full houses and flushes around
        elif (167 <= hr) & (hr <= 322): 
            hr -= 156
        elif (323 <= hr) & (hr <= 1599):
            hr += 1277
        # swap straights and trips around.
        elif (1600 <= hr) & (hr <= 1609):
            hr -= 10
        elif (1610 <= hr) & (hr <= 2467):
            hr += 867            
        else:
            pass
        return hr
    
    def TRITONmap(self,hr):
        if hr == 747: #A6789 of a suit becomes a straight flush of rank 56789 suited
            hr = 6
        # swap full houses and flushes around
        elif (167 <= hr) & (hr <= 322): 
            hr -= 156
        elif (323 <= hr) & (hr <= 1599):
            hr += 1277
        else:
            pass
        return hr

    def evaluate(self, cards, board, game_variant='FULL_DECK'):
        """
        This is the function that the user calls to get a hand rank. 

        Supports empty board, etc very flexible. No input validation 
        because that's cycles!
        """
        all_cards = list(cards) + board
        hand_rank = self._five(all_cards)
        
        if game_variant == 'FULL_DECK':
            pass
        elif game_variant == 'SHORT_DECK':
            # perform SD rank mapping and replace hand_rank
            self.SHORTmap(hand_rank)
        elif game_variant == 'TRITON':
            # PERFORM TRITON rank mapping and replace hand_rank
            self.TRITONmap(hand_rank)            
        else: 
            print('Game variant error')
            
        return hand_rank
        
        
    def _five(self, cards):
        """
        Performs an evalution given cards in integer form, mapping them to
        a rank in the range [1, 7462], with lower ranks being more powerful.

        Variant of Cactus Kev's 5 card evaluator, though I saved a lot of memory
        space using a hash table and condensing some of the calculations. 
        """
        # if flush
        if cards[0] & cards[1] & cards[2] & cards[3] & cards[4] & 0xF000:
            handOR = (cards[0] | cards[1] | cards[2] | cards[3] | cards[4]) >> 16
            prime = Card.prime_product_from_rankbits(handOR)
            return self.table.flush_lookup[prime]

        # otherwise
        else:
            prime = Card.prime_product_from_hand(cards)
            return self.table.unsuited_lookup[prime]

    
    def get_rank_class(self, hr):
        """
        Returns the class of hand given the hand hand_rank
        returned from evaluate. 
        """
        if hr >= 0 and hr <= LookupTable.MAX_STRAIGHT_FLUSH:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_STRAIGHT_FLUSH]
        elif hr <= LookupTable.MAX_FOUR_OF_A_KIND:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FOUR_OF_A_KIND]
        elif hr <= LookupTable.MAX_FULL_HOUSE:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FULL_HOUSE]
        elif hr <= LookupTable.MAX_FLUSH:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FLUSH]
        elif hr <= LookupTable.MAX_STRAIGHT:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_STRAIGHT]
        elif hr <= LookupTable.MAX_THREE_OF_A_KIND:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_THREE_OF_A_KIND]
        elif hr <= LookupTable.MAX_TWO_PAIR:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_TWO_PAIR]
        elif hr <= LookupTable.MAX_PAIR:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_PAIR]
        elif hr <= LookupTable.MAX_HIGH_CARD:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_HIGH_CARD]
        else:
            raise Exception("Inavlid hand rank, cannot return rank class")

    def class_to_string(self, class_int):
        """
        Converts the integer class hand score into a human-readable string.
        """
        return LookupTable.RANK_CLASS_TO_STRING[class_int]

    def get_five_card_rank_percentage(self, hand_rank):
        """
        Scales the hand rank score to the [0.0, 1.0] range.
        """
        return float(hand_rank) / float(LookupTable.MAX_HIGH_CARD)

    def hand_summary(self, board, hands):
        """
        Gives a sumamry of the hand with ranks as time proceeds. 

        Requires that the board is in chronological order for the 
        analysis to make sense.
        """

        assert len(board) == 5, "Invalid board length"
        for hand in hands:
            assert len(hand) == 2, "Inavlid hand length"

        line_length = 10
        stages = ["FLOP", "TURN", "RIVER"]

        for i in range(len(stages)):
            line = "=" * line_length
            print(f"{line} {stages[i]} {line}")
            
            best_rank = 7463  # rank one worse than worst hand
            winners = []
            for player, hand in enumerate(hands):

                # evaluate current board position
                rank = self.evaluate(hand, board[:(i + 3)])
                rank_class = self.get_rank_class(rank)
                class_string = self.class_to_string(rank_class)
                percentage = 1.0 - self.get_five_card_rank_percentage(rank)  # higher better here
                print(f"Player {player + 1} hand = {class_string}, percentage rank among all hands = {percentage}")

                # detect winner
                if rank == best_rank:
                    winners.append(player)
                    best_rank = rank
                elif rank < best_rank:
                    winners = [player]
                    best_rank = rank

            # if we're not on the river
            if i != stages.index("RIVER"):
                if len(winners) == 1:
                    print(f"Player {winners[0] + 1} hand is currently winning.\n")
                else:
                    print(f"Players {[x + 1 for x in winners]} are tied for the lead.\n")

            # otherwise on all other streets
            else:
                hand_result = self.class_to_string(self.get_rank_class(self.evaluate(hands[winners[0]], board)))
                print()
                print(f"{line} HAND OVER {line}")
                if len(winners) == 1:
                    print(f"Player {winners[0] + 1} is the winner with a {hand_result}\n")
                else:
                    print(f"Players {winners} tied for the win with a {hand_result}\n")
