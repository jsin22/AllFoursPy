#!/usr/bin/python3
# 0 - TwoClubs, 1 - ThreeClubs, 2 - FourClubs, 3 - FiveClubs, 4 - SixClubs,
# 5 - SevenClubs, 6 - EightClubs, 7 - NineClubs, 8 - TenClubs, 9 - JackClubs,
# 10 - QueenClubs, 11 - KingClubs, 12 - AceClubs, 13 - TwoDiamonds, 14 - ThreeDiamonds,
# 15 - FourDiamonds, 16 - FiveDiamonds, 17 - SixDiamonds, 18 - SevenDiamonds, 19 - EightDiamonds,
# 20 - NineDiamonds, 21 - TenDiamonds, 22 - JackDiamonds, 23 - QueenDiamonds, 24 - KingDiamonds,
# 25 - AceDiamonds, 26 - TwoSpades, 27 - ThreeSpades, 28 - FourSpades, 29 - FiveSpades,
# 30 - SixSpades, 31 - SevenSpades, 32 - EightSpades, 33 - NineSpades, 34 - TenSpades,
# 35 - JackSpades, 36 - QueenSpades, 37 - KingSpades, 38 - AceSpades, 39 - TwoHearts,
# 40 - ThreeHearts, 41 - FourHearts, 42 - FiveHearts, 43 - SixHearts, 44 - SevenHearts,
# 45 - EightHearts, 46 - NineHearts, 47 - TenHearts, 48 - JackHearts, 49 - QueenHearts,
# 50 - KingHearts, 51 - AceHearts

from game import *

g = Game()

g.trumpCard = 41
assert g.handWinner([[4, 0], [10, 1], [44, 0], [50, 1]]) == 3

g.trumpCard = 51
assert g.handWinner([[12, 0], [13, 1], [14, 0], [15, 1]]) == 0

g.trumpCard = 31
assert g.calcHungJack([[12, 0], [35, 1], [38, 0], [15, 1]]) == 0
assert g.calcHungJack([[12, 0], [35, 1], [37, 0], [38, 1]]) == None
assert g.calcHungJack([[12, 0], [3, 1], [38, 0], [15, 1]]) == None

g.trumpCard = 51
tricks = [
[[12, 0], [13, 1], [14, 0], [15, 1]], # 12 - AceClubs, 13 - TwoDiamonds, 14 - ThreeDiamonds, # 15 - FourDiamonds -> 0 = 4 | 1 = 0
[[16, 0], [17, 1], [18, 0], [40, 1]], # 16 - FiveDiamonds, 17 - SixDiamonds, 18 - SevenDiamonds, 40 - ThreeHearts -> 0 = 0 | 1 = 0
[[50, 0], [49, 1], [48, 0], [46, 1]], # 48 - JackHearts, 49 - QueenHearts, # 50 - KingHearts, 46 - NineHearts -> 0 = 4 | 1 = 2
[[32, 0], [33, 1], [47, 0], [25, 1]], # 32 - EightSpades, 33 - NineSpades, 47 - TenHearts, 25 - AceDiamonds -> 0 = 10 | 1 = 4
]
assert g.calcHi(tricks) == (50, 0)
assert g.calcLo(tricks) == (40, 1)
assert g.calcJack(tricks) == 0
assert g.calcGame(tricks) == 0

g.deck.cards = []
for i in range(24):
    g.deck.cards.append(i)
g.deck.cards.append(35)
for i in range(24,36,1):
    g.deck.cards.append(i)
g.deck.cards.append(48)
g.teams[0].score = 0
g.teams[1].score = 0
g.dealerIndex = 0
g.dealCards(6)
nextTrump = g.deck.cards.pop(0)
g.calcKick(nextTrump)
g.dealBeg()
assert g.teams[0].score == 6

print("All tests passed!")