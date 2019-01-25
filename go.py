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

FD.equities(myhand,ophand,b)

SD.equities(myhand,ophand,b)

TR.equities(myhand,ophand,b)

