# -*- coding: utf-8 -*-
from deck import deck
import sys

class Poker:
    def __init__(self, number_of_players, debug = False):
        self.deck = deck()
        if number_of_players < 2 or number_of_players > 10:
            sys.exit("*** ERROR ***: Invalid number of players. It must be between 2 and 10.")
        self.number_of_players = number_of_players
        self.debug = debug  # Imprimirá los parámetros de análisis

    def shuffle(self):
        self.deck.shuffle()

    def cut(self, amount):
        return self.deck.cut(amount)

    def getFlop(self):
        # Obtiene tres cartas
        if not self.deck.deal(3):
            return False
        return self.deck.deal(3)

    def getOne(self):
        # Obtiene una carta
        if not self.deck.deal(1):
            return False
        return self.deck.deal(1)

    def distribute(self):
        number_of_cards = 2 # Al empezar cada jugador obtiene 2 cartas
        if(number_of_cards*self.number_of_players > self.deck.cards_left() ):
            return False

        inplay = []
        for i in range(0, self.number_of_players):
            inplay.append( [] )

        for i in range(0, number_of_cards):
            for j in range(0, self.number_of_players):
                inplay[j].append(self.deck.deal(1).pop())

        # Retornar una lista de las cartas
        return inplay

    def name_of_hand(self, type_of_hand):
        if type_of_hand == 0:
            return "2 pares"
        elif type_of_hand == 1:
            return "1 par"
        elif type_of_hand == 2:
            return "Corrida"
        elif type_of_hand == 3:
            return "3 iguales"
        elif type_of_hand == 4:
            return "Full"
        elif type_of_hand == 5:
            return "Carta alta"
        elif type_of_hand == 6:
            return "Color"
        elif type_of_hand == 7:
            return "4 iguales"
        elif type_of_hand == 8:
            return "Corrida de color"
        else:
            return "Corrida real"

    def score(self, hand):
        score = 0
        kicker = []

        pairs = {}
        prev = 0

        #Keeps track of all the pairs in a dictionary where the key is the pair's card value
        #and the value is the number occurrences. Eg. If there are 3 Kings -> {"13":3}
        for card in hand:
            if prev == card.value:
                key = card.value
                if key in pairs:
                    pairs[key] += 1
                else:
                    pairs[key] = 2
            prev = card.value

        #Keeps track of the number of pairs and sets. The value of the previous dictionary
        #is the key. Therefore if there is a pair of 4s and 3 kings -> {"2":1,"3":1}
        nop = {}
        for k, v in pairs.iteritems():
            if v in nop:
                nop[v] += 1
            else:
                nop[v] = 1

        #Here we determine the best possible combination the hand can be knowing if the
        #hand has a four of a kind, three of a kind, and multiple pairs.
        if 4 in nop:        #Has 4 of a kind, assigns the score and the value of the
            score = 7
            kicker = pairs.keys()
            #ensures the first kicker is the value of the 4 of a kind
            kicker = [key for key in kicker if pairs[key] == 4]
            key = kicker[0]

            #Gets a list of all the cards remaining once the the 4 of a kind is removed
            temp = [card.value for card in hand if card.value != key]
            #Gets the last card in the list which is the highest remaining card to be used in
            #the event of a tie
            card_value = temp.pop()
            kicker.append(card_value)

            return [score, kicker] # Returns immediately because this is the best possible hand
            #doesn't check get the best 5 card hand if all users have a 4 of a kind

        elif 3 in nop:      # Tiene 3 cartas iguales?
            # Tiene 3 iguales y un par (Full)
            if nop[3] == 2 or 2 in nop: # Two 3 of a kind, or a pair and 3 of a kind (fullhouse)
                score = 6

                #gets a list of all the pairs and reverses it
                kicker = pairs.keys()
                kicker.reverse()
                temp = kicker

                #ensures the first kicker is the value of the highest 3 of a king
                kicker = [key for key in kicker if pairs[key] == 3]
                if( len(kicker) > 1):   # if there are two 3 of a kinds, take the higher as the first kicker
                    kicker.pop() #removes the lower one from the kicker

                #removes the value of the kicker already in the list
                temp.remove(kicker[0])
                #Gets the highest pair or 3 of kind and adds that to the kickers list
                card_value = temp[0]
                kicker.append(card_value)

            # 3 iguales solamente
            else:
                score = 3

                kicker = pairs.keys()       #Gets the value of the 3 of a king
                key = kicker[0]

                #Gets a list of all the cards remaining once the three of a kind is removed
                temp = [card.value for card in hand if card.value != key]
                #Get the 2 last cards in the list which are the 2 highest to be used in the
                #event of a tie
                card_value = temp.pop()
                kicker.append(card_value)

                card_value = temp.pop()
                kicker.append(card_value)

        # Al menos un par
        elif 2 in nop:
            # Al menos 2 o 3 pares
            if nop[2] >= 2:
                score = 2

                kicker = pairs.keys()   #Gets the card value of all the pairs
                kicker.reverse()        #reverses the key so highest pairs are used

                """
                # Si tiene 3 pares solo tomar los 2 más altos
                if (len(kicker) == 3):
                    kicker.pop()
                """

                key1 = kicker[0]
                key2 = kicker[1]

                #Gets a list of all the cards remaining once the the 2 pairs are removed
                temp = [card.value for card in hand if card.value != key1 and card.value != key2]

                #Gets the last card in the list which is the highest remaining card to be used in
                #the event of a tie
                card_value = temp.pop()
                kicker.append(card_value)

            # Tiene solo un par
            else:
                score = 1

                kicker = pairs.keys()   #Gets the value of the pair
                key = kicker[0]

                #Gets a list of all the cards remaining once pair are removed
                temp = [card.value for card in hand if card.value != key]
                #Gets the last 3 cards in the list which are the highest remaining cards
                #which will be used in the event of a tie
                card_value = temp.pop()
                kicker.append(card_value)

                card_value = temp.pop()
                kicker.append(card_value)

                card_value = temp.pop()
                kicker.append(card_value)

        #------------Checking for Straight---------------
        #Doesn't check for the ace low straight
        counter = 0
        high = 0
        straight = False

        #Checks to see if the hand contains an ace, and if so starts checking for the straight
        #using an ace low
        """
        if (hand[6].value == 14):
            prev = 1
        else:
            prev = None
        """

        #Loops through the hand checking for the straight by comparing the current card to the
        #the previous one and tabulates the number of cards found in a row
        #***It ignores pairs by skipping over cards that are similar to the previous one
        for card in hand:
            if prev and card.value == (prev + 1):
                counter += 1
                if counter == 4: #A straight has been recognized
                    straight = True
                    high = card.value
            elif prev and prev == card.value: #ignores pairs when checking for the straight
                pass
            else:
                counter = 0
            prev = card.value

        #If a straight has been realized and the hand has a lower score than a straight
        if (straight or counter >= 4) and score < 4:
            straight = True
            score = 4
            kicker = [high] #Records the highest card value in the straight in the event of a tie


        #-------------Checking for Flush-----------------
        flush = False
        total = {}

        #Loops through the hand calculating the number of cards of each symbol.
        #The symbol value is the key and for every occurrence the counter is incremented
        for card in hand:
            key = card.symbol
            if key in total:
                total[key] += 1
            else:
                total[key] = 1

        #key represents the suit of a flush if it is within the hand
        key = -1
        for k, v in total.iteritems():
            if v >= 5:
                key = int(k)

        #If a flush has been realized and the hand has a lower score than a flush
        if key != -1 and score < 5:
            flush = True
            score = 5
            kicker = [card.value for card in hand if card.symbol == key]


        #-----Checking for Straight & Royal Flush--------
        if flush and straight:
            #Doesn't check for the ace low straight
            counter = 0
            high = 0
            straight_flush = False

            #Checks to see if the hand contains an ace, and if so starts checking for the straight
            #using an ace low
            if (kicker[len(kicker)-1] == 14):
                prev = 1
            else:
                prev = None

            #Loops through the hand checking for the straight by comparing the current card to the
            #the previous one and tabulates the number of cards found in a row
            #***It ignores pairs by skipping over cards that are similar to the previous one
            for card in kicker:
                if prev and card == (prev + 1):
                    counter += 1
                    if counter >= 4: #A straight has been recognized
                        straight_flush = True
                        high = card
                elif prev and prev == card: #ignores pairs when checking for the straight
                    pass
                else:
                    counter = 0
                prev = card

            #If a straight has been realized and the hand has a lower score than a straight
            if straight_flush:
                if high == 14:
                    score = 9
                else:
                    score = 8
                kicker = [high]
                return [score, kicker]

        if flush:     #if there is only a flush then determines the kickers
            kicker.reverse()

            #This ensures only the top 5 kickers are selected and not more.
            length = len(kicker) - 5
            for i in range (0,length):
                kicker.pop() #Pops the last card of the list which is the lowest

        #-------------------High Card--------------------
        if score == 0:      #If the score is 0 then high card is the best possible hand

            #It will keep track of only the card's value
            kicker = [int(card.value) for card in hand]
            #Reverses the list for easy comparison in the event of a tie
            kicker.reverse()
            #Since the hand is sorted it will pop the two lowest cards position 0, 1 of the list
            kicker.pop()
            kicker.pop()
            #The reason we reverse then pop is because lists are inefficient at popping from
            #the beginning of the list, but fast at popping from the end therefore we reverse
            #the list and then pop the last two elements which will be the two lowest cards
            #in the hand

        conversion = {8: 8, 7: 7, 6: 4, 5: 6, 4: 2, 3: 3, 2: 0, 1: 1, 0: 5}

        #Return the score, and the kicker to be used in the event of a tie
        return [conversion[score], kicker]

    #---------------Determine Score-----------------
    def determine_score(self, community_cards, players_hands):
        for hand in players_hands:
            hand.extend(community_cards)
            hand.sort()

        results = []
        if self.debug:
            print "---- Puntuaciones ----"
        for hand in players_hands:
            overall = self.score(hand)
            results.append([overall[0], overall[1]])    # Stores the results

            if self.debug:      #Outputs the debug statements
                text = "Mano - "
                for c in hand:
                    text += str(c) + " "

                kicker = ""
                for c in overall.pop(1):
                    try:
                        kicker += str(c) + " "
                    except:
                        kicker += str(c) + " "
                print text + "Puntuacion: " + str(overall.pop(0)) + ", Desempate: " + kicker

        return results

    def determine_winner(self, results):
        if self.debug:
            print "---- Determinando ganador ----"

        #the highest score if found
        high = 0
        for r in results:
            if r[0] > high:
                high = r[0]

            if self.debug:
                print r

        kicker = {}
        counter = 0

        #Only the kickers of the player's hands that are tied for the win are analysed
        for r in results:
            if r[0] == high:
                kicker[counter] = r[1]

            counter += 1

        #if the kickers of multiple players are in the list then we have a tie and need
        #to begin comparing kickers
        if (len(kicker) > 1):
            if self.debug: #Outputs the debug statements
                print "---- Rompe empates ----"
                print "---- Desempate ----"
                for k, v in kicker.items():
                    print str(k) + " : " + str(v)

            #Iterate through all the kickers
            #It is important to the number of kickers differ based on the type of hand
            number_of_kickers = len(kicker[kicker.keys().pop()])
            for i in range (0, number_of_kickers):
                high = 0
                for k, v in kicker.items():
                    if v[i] > high:
                        high = v[i]

                #only hands matching the highest kicker remain in the list to be compared
                kicker = {k:v for k, v in kicker.items() if v[i] == high}

                if self.debug: #Outputs the debug statements of which
                    print "---- Ronda " + str(i) + " ----"
                    for k in kicker:
                        print k

                #if only one the kickers of one player remains that they are the winner
                if( len(kicker) <= 1):
                    return kicker.keys().pop()

        else:   # A clear winner was found
            return kicker.keys().pop()

        # A tie occurred, a list of the winners is returned
        return kicker.keys()