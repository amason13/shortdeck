from random import shuffle as rshuffle
from .card import Card


class Deck:
    """
    Class representing a deck. The first time we create, we seed the static 
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it. 
    """
    _FULL_DECK = []
    
    def __init__(self):
        self.shuffle()
        self.dead_cards = []
        
    def shuffle(self):
        # and then shuffle
        self.cards = Deck.GetFullDeck()
        rshuffle(self.cards)
        self.dead_cards=[]
        
    def reshuffle(self):
        rshuffle(self.cards)

    def draw(self, n=1):
        if n == 1:
            card = self.cards.pop(0)
            self.dead_cards.append(card)
            return card

        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards
        for card in cards:
            self.dead_cards.append(card)
                
    def remove(self, my_cards):
        print(Card.print_pretty_cards(my_cards))
        for c in my_cards:
            self.cards.remove(c)
            self.dead_cards.append(c)

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

