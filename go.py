from shortdeck import Card, Evaluator, Deck

FD = Evaluator()
SD = Evaluator(game_variant='SHORT_DECK')
TR = Evaluator(game_variant='TRITON')
'''
h1 = []
h1.append(Card.new('Ac'))
h1.append(Card.new('6c'))

h2 = []
h2.append(Card.new('Kh'))
h2.append(Card.new('Kd'))

h3 = []
h3.append(Card.new('8h'))
h3.append(Card.new('9h'))

h4 = []
h4.append(Card.new('2h'))
h4.append(Card.new('2d'))

print(FD.equities(h1,h2,[]))
print(FD.equities(h1,h3,[]))
print(FD.equities(h1,h4,[]))
print(FD.equities(h2,h3,[]))
print(FD.equities(h2,h4,[]))
print(FD.equities(h3,h4,[]))
'''
'''
print('******full deck******')
print(FD.equities(myhand,ophand,[]))

print('******short deck******')
print(SD.equities(myhand,ophand,[]))

print('******triton******')
print(TR.equities(myhand,ophand,[]))

boat = []
boat.append(Card.new('Ac'))
boat.append(Card.new('As'))
boat.append(Card.new('Ad'))
boat.append(Card.new('Kc'))
boat.append(Card.new('Kd'))

flush = []
flush.append(Card.new('Ac'))
flush.append(Card.new('2c'))
flush.append(Card.new('3c'))
flush.append(Card.new('Kc'))
flush.append(Card.new('7c'))

print(FD.evaluate(boat,[]))
print(FD.evaluate(flush,[]))

print(SD.evaluate(boat,[]))
print(SD.evaluate(flush,[]))

print(TR.evaluate(boat,[]))
print(TR.evaluate(flush,[]))
'''
p1 = []
p2 = []
b = []

p1.append(Card.new('8c'))
p1.append(Card.new('8h'))

p2.append(Card.new('9c'))
p2.append(Card.new('Jh'))

b.append(Card.new('8d'))
b.append(Card.new('7d'))
b.append(Card.new('Tc'))
b.append(Card.new('Qs'))


print(SD.equities(p1,p2,b))
print(TR.equities(p1,p2,b))
