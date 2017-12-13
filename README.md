Treys
========

A pure Python poker hand evaluation library

    [ 3 ❤ ] , [ 3 ♠ ]
    
## Installation

```
$ pip install treys
```

## Implementation notes

Treys is a Python 3 port of [Deuces](https://github.com/worldveil/deuces). Most of work is taken from [msaindon's](https://github.com/msaindon/deuces) fork.

Treys (originally Deuces) was written by [Will Drevo](http://willdrevo.com/) for the MIT Pokerbots Competition. It is lightweight and fast. All lookups are done with bit arithmetic and dictionary lookups. That said, Treys won't beat a C implemenation (~250k eval/s) but it is useful for situations where Python is required or where bots are allocated reasonable thinking time (human time scale).

Treys handles 5, 6, and 7 card hand lookups. The 6 and 7 card lookups are done by combinatorially evaluating the 5 card choices.

## Usage

Treys is easy to set up and use. 

```python
>>> from treys import Card
>>> card = Card.new('Qh')
```

Card objects are represented as integers to keep Treys performant and lightweight. 

Now let's create the board and an example Texas Hold'em hand:

```python
>>> board = [
>>>     Card.new('Ah'),
>>>     Card.new('Kd'),
>>>     Card.new('Jc')
>>> ]
>>> hand = [
>>>    Card.new('Qs'),
>>>    Card.new('Th')
>>> ]
```

Pretty print card integers to the terminal: 

    >>> Card.print_pretty_cards(board + hand)
      [ A ❤ ] , [ K ♦ ] , [ J ♣ ] , [ Q ♠ ] , [ T ❤ ] 

If you have [`termacolor`](http://pypi.python.org/pypi/termcolor) installed, they will be colored as well. 

Otherwise move straight to evaluating your hand strength:
```python
>>> from treys import Evaluator
>>> evaluator = Evaluator()
>>> print evaluator.evaluate(board, hand)
1600
```

Hand strength is valued on a scale of 1 to 7462, where 1 is a Royal Flush and 7462 is unsuited 7-5-4-3-2, as there are only 7642 distinctly ranked hands in poker. Once again, refer to my blog post for a more mathematically complete explanation of why this is so. 

If you want to deal out cards randomly from a deck, you can also do that with Treys:
```python
>>> from treys import Deck
>>> deck = Deck()
>>> board = deck.draw(5)
>>> player1_hand = deck.draw(2)
>>> player2_hand = deck.draw(2)
```
and print them:

    >>> Card.print_pretty_cards(board)
      [ 4 ♣ ] , [ A ♠ ] , [ 5 ♦ ] , [ K ♣ ] , [ 2 ♠ ]
    >>> Card.print_pretty_cards(player1_hand)
      [ 6 ♣ ] , [ 7 ❤ ] 
    >>> Card.print_pretty_cards(player2_hand)
      [ A ♣ ] , [ 3 ❤ ] 

Let's evaluate both hands strength, and then bin them into classes, one for each hand type (High Card, Pair, etc)
```python
>>> p1_score = evaluator.evaluate(board, player1_hand)
>>> p2_score = evaluator.evaluate(board, player2_hand)
>>> p1_class = evaluator.get_rank_class(p1_score)
>>> p2_class = evaluator.get_rank_class(p2_score)
```
or get a human-friendly string to describe the score,

    >>> print "Player 1 hand rank = %d (%s)\n" % (p1_score, evaluator.class_to_string(p1_class))
    Player 1 hand rank = 6330 (High Card)

    >>> print "Player 2 hand rank = %d (%s)\n" % (p2_score, evaluator.class_to_string(p2_class))
    Player 2 hand rank = 1609 (Straight)

or, coolest of all, get a blow-by-blow analysis of the stages of the game with relation to hand strength:

    >>> hands = [player1_hand, player2_hand]
    >>> evaluator.hand_summary(board, hands)

    ========== FLOP ==========
    Player 1 hand = High Card, percentage rank among all hands = 0.893192
    Player 2 hand = Pair, percentage rank among all hands = 0.474672
    Player 2 hand is currently winning.

    ========== TURN ==========
    Player 1 hand = High Card, percentage rank among all hands = 0.848298
    Player 2 hand = Pair, percentage rank among all hands = 0.452292
    Player 2 hand is currently winning.

    ========== RIVER ==========
    Player 1 hand = High Card, percentage rank among all hands = 0.848298
    Player 2 hand = Straight, percentage rank among all hands = 0.215626

    ========== HAND OVER ==========
    Player 2 is the winner with a Straight

## License

Copyright (c) 2013 Will Drevo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
