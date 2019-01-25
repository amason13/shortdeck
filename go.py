from treys import Card, Evaluator, Deck

evaluator = Evaluator()
myhand = []
myhand.append(Card.new('Ac'))
myhand.append(Card.new('Kc'))

ophand = []
ophand.append(Card.new('Jh'))
ophand.append(Card.new('Th'))

evaluator.evaluate(myhand,ophand)

evaluator.evaluate(myhand,ophand,game_variant = SHORT_DECK)

evaluator.evaluate(myhand,ophand,game_variant = TRITON)

