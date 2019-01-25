from shortdeck import Card, Evaluator, Deck

FD = Evaluator()
SD = Evaluator(game_variant='SHORT_DECK')
TR = Evaluator(game_variant='TRITON')

myhand = []
myhand.append(Card.new('Ac'))
myhand.append(Card.new('Kc'))

ophand = []
ophand.append(Card.new('Jh'))
ophand.append(Card.new('Th'))

b=[]

print('******full deck******')
print(FD.equities(myhand,ophand,b))

print('******short deck******')
print(SD.equities(myhand,ophand,b))

print('******triton******')
print(TR.equities(myhand,ophand,b))

