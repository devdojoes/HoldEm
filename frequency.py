# -*- coding: utf-8 -*-
from holdem import Poker
import sys

debug = False
numero_de_jugadores = 2


juego = { 'pozo': 0 }

jugadores = [{ 'dinero': 250, 'victorias': 0 },{ 'dinero': 250, 'victorias': 0 }]

juego_activo = True
nuestro_jugador = 0
jugador_oponente = 1
jugador_que_empieza = 0
apuesta_actual = 1
mano_actual = 1

frecuencia_de_manos = {}

while juego_activo:
    poker = Poker(numero_de_jugadores, debug)
    if not poker:
        sys.exit('Numero de jugadores inválido')

    print('- Mano #' + str(mano_actual) + ' -')
    poker.shuffle() # Revolver cartas

    players_hands = poker.distribute()
    if not players_hands:
        sys.exit('Cartas insuficientes')

    # Obtener el "Flop" (Primeras tres cartas)
    carta = poker.getFlop()
    if not carta:
        sys.exit('Cartas insuficientes')
    cartas_comunes = carta

    """
    # Obtener la siguiente carta "Turn"
    carta = poker.getOne()
    if not carta:
        sys.exit('Cartas insuficientes')
    cartas_comunes.extend(carta)

    # Obtener la quinta carta "River"
    carta = poker.getOne()
    if not carta:
        sys.exit('Cartas insuficientes')
    cartas_comunes.extend(carta)
    """

    results = poker.determine_score(cartas_comunes, players_hands)

    try:
        results = poker.determine_score(cartas_comunes, players_hands)
    except:
        sys.exit("No se puede determinar la puntuacion")

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
            name_of_hand = poker.name_of_hand(results[counter][0])

            if name_of_hand in frecuencia_de_manos:
                frecuencia_de_manos[name_of_hand] += 1
            else:
                frecuencia_de_manos[name_of_hand] = 1

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
            name_of_hand = poker.name_of_hand(results[counter][0])

            if name_of_hand in frecuencia_de_manos:
                frecuencia_de_manos[name_of_hand] += 1
            else:
                frecuencia_de_manos[name_of_hand] = 1

            counter += 1
            print text

    mano_actual += 1

    if mano_actual > 2:
        juego_activo = False


#print(frecuencia_de_manos)
total = sum(frecuencia_de_manos.values())
print(total)
for key in frecuencia_de_manos:
    print(key + ' ' + str(frecuencia_de_manos[key] / float(total)))
