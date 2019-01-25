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

boat = []
boat.append(Card.new('Ac'))
boat.append(Card.new('As'))
boat.append(Card.new('Ad'))
boat.append(Card.new('Kc'))
boat.append(Card.new('Kd'))

print(FD.evaluate(boat,[]))
print(SD.evaluate(boat,[]))
print(TR.evaluate(boat,[]))
