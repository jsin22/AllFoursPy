#!/usr/bin/python3
import random  # for shuffling
import re # regex
import itertools # iterate multiper lists - zip_longest
import sys # for exit
import time # for sleep
from random import randint # for selecting random card in Ai mode
from random import choice # for selecting random beg in Ai mode
from os import path # for reading board file
from os import system # for clear screen 

class CardUtil:
    suits = {
        0: "Clubs",
        1: "Diamonds",
        2: "Spades",
        3: "Hearts"
    }

    charSuit = {
        0: "♣",
        1: "♦",
        2: "♠",
        3: "♥"
    }

    charRank = {
        0: "2",
        1: "3",
        2: "4",
        3: "5",
        4: "6",
        5: "7",
        6: "8",
        7: "9",
        8: "T",
        9: "J",
        10: "Q",
        11: "K",
        12: "A"
    }

    ranks = {
        0: "Two",
        1: "Three",
        2: "Four",
        3: "Five",
        4: "Six",
        5: "Seven",
        6: "Eight",
        7: "Nine",
        8: "Ten",
        9: "Jack",
        10: "Queen",
        11: "King",
        12: "Ace"
    }

    def suit(card):
        return CardUtil.suits[int(card / 13)]

    def rank(card):
        return CardUtil.ranks[int(card % 13)]

    def out(card):
        print(CardUtil.rank(card) + ":" + CardUtil.suit(card))
    
    def txt(card):
        if card == None: 
            return "--"
        return CardUtil.charRank[int(card % 13)] + CardUtil.charSuit[int(card / 13)]


class Deck:
    def __init__(self):
        self.new()

    def new(self):
        self.cards = []
        for x in range(52):
            self.cards.append(x) 

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        string = ""
        for c in self.cards:
            string += CardUtil.rank(c) + " of " + CardUtil.suit(c) + ", "
        return string

class Player:
    def __init__(self, name, ai):
        self.resetHand()
        self.name = name
        self.currentCard = None
        self.isAi = ai
    
    def resetHand(self):
        self.hand = []
    
    def addCard(self, c):
        self.hand.append(c)
    
    def out(self):
        return self.name + " - " + CardUtil.txt(self.currentCard)
    
    def getBeg(self, trump):

        def getUserBeg():
            print("Beg? (y): ")
            yn = str(input())
            return (False, True)[yn == "Y" or yn == "y"]

        def getAiBeg():
            begs = [True, False]
            return choice(begs)

        return getAiBeg() if self.isAi else getUserBeg()

    
    # leadCard - first card played during this play
    # trumpCard - trumpCard for this round
    # teamCard - card played by teammate in this play
    # oppCards - cards played by opponents in this play
    # teammateHand - cards your teammates have
    def playCard(self, leadCard, trumpCard, teammateCard, oppCards, teammateHand):

        if len(self.hand) == 0:
            return None 

        def checkCard(card):
            if card == None:
                return False

            if leadCard == None: # first play
                return True

            s = CardUtil.suit(card)
            ls = CardUtil.suit(leadCard)
            if s == ls or s == CardUtil.suit(trumpCard):
                return True
            
            for c in self.hand:
                if CardUtil.suit(c) == ls:
                    return False
        
        def getPlay():
            print("Play: ")
            try:
                play = int(input()) 
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                return None

            if play <= 0 or play > len(self.hand):
                return None

            return play - 1

        def getUserPlay():
            play = getPlay()
            while play == None or checkCard(self.hand[play]) == False:
                print("Bad Play! Try Again.")
                play = getPlay()

            return play

        def getAiPlay():
            play = randint(0, len(self.hand)-1)
            while checkCard(self.hand[play]) == False:
                play = randint(0, len(self.hand)-1)

            return play
            
        play = getAiPlay() if self.isAi else getUserPlay()
        
        self.currentCard = self.hand.pop(play)
        return self.currentCard
    
    def __str__(self):
        string = self.name + " - "
        for i, c in enumerate(self.hand, 0):
            string += str(i) + "." + CardUtil.rank(c) + " of " + CardUtil.suit(c) + ", "
        return string
    
class Team:
    def __init__(self, name):
        self.score = 0
        self.p1 = Player(name+".1", True)
        self.p2 = Player(name+".2", True)
        self.tricks = []

    def reset(self):
        self.score = 0
        self.p1.resetHand()
        self.p2.resetHand()
        self.tricks = []


class Game:
    def __init__(self):
        self.deck = Deck()
        self.dealerIndex = 0
        self.winScore = 14 
        self.board = []

        self.teams = [Team("A"), Team("B")]

        self.players = [self.teams[0].p1, 
                        self.teams[1].p1, 
                        self.teams[0].p2, 
                        self.teams[1].p2]
        
        self.numPlayers = len(self.players)

        self.init_board()

    def new(self):
        self.teams[0].score = 0
        self.teams[1].score = 0
        self.deck.new()

    def init_board(self):
        game_folder = path.dirname(__file__)
        filename = path.join(game_folder, 'board.txt')
        with open(filename, 'rt') as f:
            for line in f:
                self.board.append(line)
    
    def printPlayer(self, pIndex):
        line = ""
        for i, c in enumerate(self.players[pIndex].hand, 1):
            line += str(i) + "-" + CardUtil.txt(c)
            if i % 3:
                line += " | " 
            else:
                line += "\n"
        
        if len(self.players[pIndex].hand) % 3:
            line += "\n"

        return line
    
    def printBoard(self, currentPlayer):
        system('clear')

        def printPlayerCard(line, marker, i):
            dlr = "   "
            cur = " "
            if self.dealerIndex % self.numPlayers == i:
                dlr = "(D)"
            
            if currentPlayer == i:
                cur = "*"

            replaceStr = cur + dlr + self.players[i].out()

            return re.sub(marker, replaceStr, line)

        for line in self.board:
            dlr = ""
            cur = ""
            if line[0] == 'S':
                line = re.sub(r'^S', ' ', line)
                line = re.sub(r'A:s', 'A: '+str(self.teams[0].score), line)
                line = re.sub(r'B:s', 'B: '+str(self.teams[1].score), line)
            elif line[0] == 'T':
                line = re.sub(r'^T', ' ', line)
                line = re.sub(r'-', CardUtil.txt(self.trumpCard), line)
            elif line[0] == 'A' and line[1] == '1':
                line = re.sub(r'^A1', "", line)
                line = printPlayerCard(line, "C", 0)
            elif line[0] == 'A' and line[1] == '2':
                line = re.sub(r'^A2', "", line)
                line = printPlayerCard(line, "C", 2)
            elif line[0] == 'B': 
                line = re.sub(r'^B', "", line)
                line = printPlayerCard(line, "C1", 1)
                line = printPlayerCard(line, "C2", 3)
            elif line[0] == 'H':
                replaceStr =  self.players[currentPlayer].name + "'s Hand:\n" 
                replaceStr += self.printPlayer(currentPlayer)  
                line = re.sub(r'^H', replaceStr, line)

            print(line)

        #time.sleep(1)
        return None

    def dealCards(self, numCards):
        i = self.dealerIndex 
        for x in range(self.numPlayers * numCards):
            self.players[i % self.numPlayers].addCard(self.deck.cards.pop(0))
            i += 1
    
    def resetHands(self):
        for p in self.players:
            p.resetHand()

    def calcHungJack(self, trick):
        jackTeam = None
        hangTeam = None

        for i, v in enumerate(trick):
            if CardUtil.suit(v[0]) == CardUtil.suit(self.trumpCard) and CardUtil.rank(v[0]) == "Jack":
                jackTeam = v[1]
            elif (CardUtil.suit(v[0]) == CardUtil.suit(self.trumpCard)) and \
                 (CardUtil.rank(v[0]) == "Queen" or CardUtil.rank(v[0]) == "King" or CardUtil.rank(v[0]) == "Ace"):
                hangTeam = v[1]
        
        if jackTeam != None and hangTeam != jackTeam:
            return hangTeam
        
        return None

    def handWinner(self, trick):
        trumpSuitHigh = None
        leadSuitHigh = trick[0][0]
        winner = 0
        teamWinner = None
        jackTeam = None

        for i, v in enumerate(trick):
            # if trump, find the highest card value
            if CardUtil.suit(v[0]) == CardUtil.suit(self.trumpCard) and (trumpSuitHigh == None or v[0] > trumpSuitHigh):
                trumpSuitHigh = v[0]
                winner = i
            # winner is the lead card suit if no trump is played
            elif CardUtil.suit(v[0]) == CardUtil.suit(leadSuitHigh) and v[0] > leadSuitHigh and trumpSuitHigh == None:
                leadSuitHigh = v[0]
                winner = i  
        
        return winner

    def calcGame(self, tricks):
        teamCount = [0, 0]

        for i in tricks:
            for x in i:
                if CardUtil.rank(x[0]) == "Ten":
                    teamCount[x[1]] += 10
                elif CardUtil.rank(x[0]) == "Jack":
                    teamCount[x[1]] += 1
                elif CardUtil.rank(x[0]) == "Queen":
                    teamCount[x[1]] += 2
                elif CardUtil.rank(x[0]) == "King":
                    teamCount[x[1]] += 3
                elif CardUtil.rank(x[0]) == "Ace":
                    teamCount[x[1]] += 4
        
        return (1, 0)[teamCount[0] > teamCount[1]]

    def calcHi(self, tricks):
        teamIndex = None
        trumpSuit = CardUtil.suit(self.trumpCard)
        highTrump = None

        for i in tricks:
            for x in i:
                if CardUtil.suit(x[0]) == trumpSuit and (highTrump == None or x[0] > highTrump):
                    highTrump = x[0]
                    teamIndex = x[1]

        return highTrump, teamIndex

    def calcLo(self, tricks):
        teamIndex = None
        trumpSuit = CardUtil.suit(self.trumpCard)
        lowTrump = None

        for i in tricks:
            for x in i:
                if CardUtil.suit(x[0]) == trumpSuit and (lowTrump == None or x[0] < lowTrump):
                    lowTrump  = x[0]
                    teamIndex = x[1]

        return lowTrump, teamIndex

    def calcJack(self, tricks):
        trumpSuit = CardUtil.suit(self.trumpCard)

        for i in tricks:
            for x in i:
                if CardUtil.suit(x[0]) == trumpSuit and CardUtil.rank(x[0]) == "Jack":
                    return x[1]
        
        return None
    
    def calcKick(self, card):
        if CardUtil.rank(card) == "Jack":
            self.teams[self.dealerIndex % 2].score += 3
        elif CardUtil.rank(card) == "Six":
            self.teams[self.dealerIndex % 2].score += 2
        elif CardUtil.rank(card) == "Ace":
            self.teams[self.dealerIndex % 2].score += 1

    def playRound(self):
        numOfPlays = len(self.players[0].hand) # number of cards in this round
        i = self.dealerIndex + 1 # start with player to the right of dealer
        tricks = [] # get all hands in this round, will use to count for game
        hungJack = False

        for y in range(numOfPlays):
            t1 = []
            t2 = []
            trick = []
            pIndex = [] # create player index array

            t1.append([ self.players[i % self.numPlayers].playCard(None,  self.trumpCard, None,  [], self.players[(i+2) % self.numPlayers].hand),
                        i % 2 ]); pIndex.append(i); i+=1; self.printBoard(i % self.numPlayers)  
            t2.append([ self.players[i % self.numPlayers].playCard(t1[0][0], self.trumpCard, None,  t1, self.players[(i+2) % self.numPlayers].hand),
                        i % 2 ]); pIndex.append(i); i+=1; self.printBoard(i % self.numPlayers)
            t1.append([ self.players[i % self.numPlayers].playCard(t1[0][0], self.trumpCard, t1[0], t2, self.players[(i+2) % self.numPlayers].hand),
                        i % 2 ]); pIndex.append(i); i+=1; self.printBoard(i % self.numPlayers)
            t2.append([ self.players[i % self.numPlayers].playCard(t1[0][0], self.trumpCard, t2[0], t1, self.players[(i+2) % self.numPlayers].hand),
                        i % 2 ]); pIndex.append(i); i+=1; self.printBoard(i % self.numPlayers) 

            trick.append(t1[0]); trick.append(t2[0]); trick.append(t1[1]); trick.append(t2[1])

            i = pIndex[self.handWinner(trick)] # which player won the hand 

            tIndex = self.calcHungJack(trick)
            if tIndex != None:
                self.teams[tIndex].score += 3
                hungJack = True

            tricks.append(trick)
            
            # reset current cards for next hand
            for p in self.players:
                p.currentCard = None
            self.printBoard(i % self.numPlayers)

        hiCard, tIndex = self.calcHi(tricks)
        if tIndex != None:
            self.teams[tIndex].score += 1

        loCard, tIndex = self.calcLo(tricks)
        if tIndex != None:
            self.teams[tIndex].score += 1
        
        tIndex = (self.calcJack(tricks), None)[hungJack]
        if tIndex != None:
            self.teams[tIndex].score += 1

        tIndex = self.calcGame(tricks)
        self.teams[tIndex].score += 1

    def checkBeg(self):
        return self.players[(self.dealerIndex + 1) % self.numPlayers].getBeg(self.trumpCard)

    def dealBeg(self):
        #condition when there aren't enough cards to deal to everyone, so try remaining cards
        if len(self.deck.cards) < ((self.numPlayers * 3) + 1):
            for i in range(len(self.deck.cards)):
                nextTrump = self.deck.cards.pop(0)
                self.calcKick(nextTrump)

                if(CardUtil.suit(nextTrump) != CardUtil.suit(self.trumpCard)):
                    self.trumpCard = nextTrump
                    return True
                else:
                    self.trumpCard = nextTrump

            return False # no new suit was found

        self.dealCards(3)
        nextTrump = self.deck.cards.pop(0)
        self.calcKick(nextTrump)

        if(CardUtil.suit(nextTrump) == CardUtil.suit(self.trumpCard)):
            self.trumpCard = nextTrump
            self.dealBeg()
        else:
            self.trumpCard = nextTrump
        
        return True

    def nextRound(self):

        self.resetHands()
        self.deck.new()
        self.deck.shuffle()

        self.dealCards(6)
        self.trumpCard = self.deck.cards.pop(0)
        self.calcKick(self.trumpCard)

        self.printBoard((self.dealerIndex + 1) % self.numPlayers)

        if self.checkBeg():
            if(self.dealBeg() == False): # pack ran out with no new trump
                self.nextRound()
        
        self.printBoard((self.dealerIndex + 1) % self.numPlayers)
        self.playRound()
        self.dealerIndex += 1 # dealer moves to the right

    def run(self):

        self.playing = True
        while self.playing:
            self.nextRound()
            self.playing = self.teams[0].score < self.winScore and self.teams[1].score < self.winScore
        
        print(("Team A","Team B")[self.teams[1].score >= self.winScore], "Wins!\n")

        print("Play Again?: ")
        yn = input()
        if yn == 'y' or yn == 'Y':
            self.new()
            self.playing = True
            self.run()

# main
if __name__ == "__main__":
    g = Game()
    g.run()
