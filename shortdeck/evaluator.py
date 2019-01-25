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

    def __init__(self, game_variant = 'FULL_DECK'):
        
        self.table = LookupTable()
        self.game_variant = game_variant
        
        self.hand_size_map = {
            5: self._five,
            6: self._six,
            7: self._seven
        }

        
    def SHORTmap(self, hr):
        if hr == 747: #A6789 of a suit becomes a straight flush of rank 56789 suited
            hr = 6
        elif hr == 6610: # A6789 unsuited becomes a straight of rank 56789
            hr = 1605
        # swap full houses and flushes around
        elif (167 <= hr) and (hr <= 322): 
            hr += 1277
        elif (323 <= hr) and (hr <= 1599):
            hr -= 156
        # swap straights and trips around.
        elif (1600 <= hr) and (hr <= 1609):
            hr += 858
        elif (1610 <= hr) and (hr <= 2467):
            hr -= 10            
        else:
            pass
        return hr

    def TRITONmap(self, hr):
        if hr == 747: #A6789 of a suit becomes a straight flush of rank 56789 suited
            hr = 6
        elif hr == 6610: # A6789 unsuited becomes a straight of rank 56789
            hr = 1605
        # swap full houses and flushes around
        elif (167 <= hr) and (hr <= 322): 
            hr += 1277
        elif (323 <= hr) and (hr <= 1599):
            hr -= 156
        else:
            pass
        return hr

    def evaluate(self, cards, board):
        """
        This is the function that the user calls to get a hand rank. 

        Supports empty board, etc very flexible. No input validation 
        because that's cycles!
        """
        all_cards = list(cards) + board
        hand_rank = self.hand_size_map[len(all_cards)](all_cards)
        print(self.game_variant, hand_rank)
        if self.game_variant == 'FULL_DECK':
            pass
        elif self.game_variant == 'SHORT_DECK':
            # perform SD rank mapping and replace hand_rank
            hand_rank = self.SHORTmap(hand_rank)
        elif self.game_variant == 'TRITON':
            # PERFORM TRITON rank mapping and replace hand_rank
            hand_rank = self.TRITONmap(hand_rank)            
        else: 
            print('Game variant error')
        print(hand_rank)    
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

    def _six(self, cards):
        """
        Performs five_card_eval() on all (6 choose 5) = 6 subsets
        of 5 cards in the set of 6 to determine the best ranking, 
        and returns this ranking.
        """
        minimum = LookupTable.MAX_HIGH_CARD

        all5cardcombobs = itertools.combinations(cards, 5)
        for combo in all5cardcombobs:

            score = self._five(combo)
            if score < minimum:
                minimum = score

        return minimum

    def _seven(self, cards):
        """
        Performs five_card_eval() on all (7 choose 5) = 21 subsets
        of 5 cards in the set of 7 to determine the best ranking, 
        and returns this ranking.
        """
        minimum = LookupTable.MAX_HIGH_CARD

        all5cardcombobs = itertools.combinations(cards, 5)
        for combo in all5cardcombobs:
            
            score = self._five(combo)
            if score < minimum:
                minimum = score

        return minimum
    
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
            
    def equities(self, hero_cards, villain_cards, board, num_iters = 1000):
        all_cards = hero_cards + villain_cards + board
        hero = 0
        ties = 0
        for i in range(num_iters):
            deck = Deck(variant = self.game_variant)
            deck.remove(all_cards)
            deck.reshuffle()
            
            full_board = board + deck.draw(5-len(board))
            
            hero_rank = self.evaluate(hero_cards,full_board)
            villain_rank = self.evaluate(villain_cards,full_board)

            if hero_rank == villain_rank:
                ties+=1
                print(Card.print_pretty_cards(full_board))

            if hero_rank<villain_rank:
                hero+=1
                
        return (hero/num_iters, ties/num_iters, (num_iters-hero-ties)/num_iters)          
        
    


    
