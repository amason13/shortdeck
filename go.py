from shortdeck import Card, Evaluator, Deck

FD = Evaluator()
SD = Evaluator(game_variant='SHORT_DECK')
TR = Evaluator(game_variant='TRITON')

myhand = []
myhand.append(Card.new('Ac'))
myhand.append(Card.new('6c'))

ophand = []
ophand.append(Card.new('Kh'))
ophand.append(Card.new('Kd'))

b=[]
'''
print('******full deck******')
print(FD.equities(myhand,ophand,b))

print('******short deck******')
print(SD.equities(myhand,ophand,b))

print('******triton******')
print(TR.equities(myhand,ophand,b))
'''
test_hand = []

test_hand.append(Card.new('Ac'))
test_hand.append(Card.new('6c'))
test_hand.append(Card.new('7c'))
test_hand.append(Card.new('8c'))
test_hand.append(Card.new('9c'))

print(SD.evaluate(test_hand,[]))
