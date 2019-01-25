from shortdeck import Card, Evaluator, Deck

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

FD = Evaluator()
print(FD.game_variant)
print(FD.evaluate(test_hand,[]))

SD = Evaluator(game_variant='SHORT_DECK')
print(SD.game_variant)
print(SD.evaluate(test_hand,[]))

TR = Evaluator(game_variant='TRITON')
print(TR.game_variant)
print(TR.evaluate(test_hand,[]))
