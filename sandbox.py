# -*- coding: utf-8 -*-
from holdem import Poker
from deck import Card
import sys

debug = True
numero_de_jugadores = 2

poker = Poker(numero_de_jugadores, debug)
if not poker:
    sys.exit('Numero de jugadores inválido')

players_hands = poker.distribute()

# Sandbox

players_hands[0] = []
carta = Card(3, 6)
players_hands[0].append(carta)
carta = Card(1, 4)
players_hands[0].append(carta)
for carta in players_hands[0]:
    print('Carta: ' + str(carta))

players_hands[1] = []
carta = Card(1, 7)
players_hands[1].append(carta)
carta = Card(2, 1)
players_hands[1].append(carta)
for carta in players_hands[1]:
    print('Opone: ' + str(carta))

cartas_comunes = []
carta = Card(0, 5)
cartas_comunes.append(carta)
carta = Card(1, 5)
cartas_comunes.append(carta)
carta = Card(0, 3)
cartas_comunes.append(carta)
carta = Card(1, 9)
cartas_comunes.append(carta)
carta = Card(1, 3)
cartas_comunes.append(carta)
for carta in cartas_comunes:
    print('Comun: ' + str(carta))

try:
    results = poker.determine_score(cartas_comunes, players_hands)
except:
    sys.exit("No se puede determinar la puntuacion")

print('Results:' + str(results))

try:
    ganador = poker.determine_winner(results)
except:
    sys.exit('No se puede determinar el ganador')

# Verifica si hay un empate al revisar que hay un solo ganador (si es arreglo hay varios)
empate = True
try:
    len(ganador)
except:
    empate = False

if not empate:
    counter = 0
    print "-------- Hay un ganador --------"
    for hand in players_hands:
        if counter == ganador:
            text = "Ganador  * "
        else:
            text = "Perdedor   "
        for c in hand:
            text += str(c) + " "

        text += " (" + poker.name_of_hand(results[counter][0]) + ')'
        counter += 1
        print text

else:
    counter = 0
    print "--------- Hay un empate --------"
    for hand in players_hands:
        if counter in ganador:
            text = "Ganador  * "
        else:
            text = "Perdedor   "
        for c in hand:
            text += str(c) + " "

        text += " (" + poker.name_of_hand(results[counter][0]) + ')'


        counter += 1
        print text
