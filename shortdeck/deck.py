from random import shuffle as rshuffle
from .card import Card


class Deck:
    """
    Class representing a deck. The first time we create, we seed the static 
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it. 
    """
    _FULL_DECK = []
    _SHORT_DECK = []
    
    def __init__(self, variant = 'FULL_DECK'):
        self.variant = variant
        self.shuffle()
        self.dead_cards = []
        
    def shuffle(self):
        # and then shuffle
        if self.variant == 'FULL_DECK':
            self.cards = Deck.GetFullDeck()
        else: 
            self.cards = Deck.GetShortDeck()
        rshuffle(self.cards)
        
    def reshuffle(self):
        rshuffle(self.cards)

    def draw(self, n=1):            
        cards = []
        for i in range(n):
            cards.append(self.cards.pop(0))
        return cards
  
                
    def remove(self, my_cards):
        for c in my_cards:
            self.cards.remove(c)

    def __str__(self):
        return Card.print_pretty_cards(self.cards)

    @staticmethod
    def GetFullDeck():
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
                Deck._FULL_DECK.append(Card.new(rank + suit))

        return list(Deck._FULL_DECK)
    
    @staticmethod
    def GetShortDeck():
        if Deck._SHORT_DECK:
            return list(Deck._SHORT_DECK)

        # create the standard 36 card short deck
        for rank in Card.STR_RANKS[4:]:
            for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
                Deck._SHORT_DECK.append(Card.new(rank + suit))

        return list(Deck._SHORT_DECK)

