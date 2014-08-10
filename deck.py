# -*- coding: utf-8 -*-
# Código basado de GitHub
from random import shuffle

class Card:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        elif self.value == other.value:
            return 0
        return 1

    def __str__(self):
        text = str(self.value)

        if self.symbol == 0:    # D - Diamantes
            text += "D"
        elif self.symbol == 1:  # C - Corazones
            text += "C"
        elif self.symbol == 2:  # E - Espadas
            text += "E"
        else:   # T - Treboles
            text += "T"

        return text

class deck:
    # Inicializamos las cartas
    def __init__(self, addJokers = False):
        self.cards = []
        self.inplay = []
        self.addJokers = addJokers
        for symbol in range(0, 4):
            for value in range (1, 10):
                self.cards.append(Card(symbol, value))

        self.total_cards = len(self.cards)

    #Shuffles the deck
    def shuffle(self):
        self.cards.extend(self.inplay)
        self.inplay = []
        shuffle(self.cards)

    #Cuts the deck by the amount specified
    #Returns true if the deck was cut successfully and false otherwise
    def cut(self, amount):
        if not amount or amount < 0 or amount >= len(self.cards):
            return False #returns false if cutting by a negative number or more cards than in the deck

        temp = []
        for i in range(0,amount):
            temp.append( self.cards.pop(0) )
        self.cards.extend(temp)
        return True

    #Returns a data dictionary
    def deal(self, number_of_cards):
        if number_of_cards > len(self.cards):
            return False #Returns false if there are insufficient cards

        inplay = []
        for i in range(0, number_of_cards):
            inplay.append(self.cards.pop(0))

        self.inplay.extend(inplay)
        return inplay

    def cards_left(self):
        return len(self.cards)