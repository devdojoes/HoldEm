# -*- coding: utf-8 -*-
from holdem import Poker
import sys

debug = True
numero_de_jugadores = 2

def mostrar_cartas_comunes(community_cards):
    texto = '         '
    for carta in community_cards:
        texto += str(carta) + ' '
    print(texto)

def mostrar_cartas_jugador(num_jugador):
    texto = ''
    for carta in players_hands[0]:
        texto += str(carta) + ' '
    print(texto)

def preguntar_jugada():
    respuesta = raw_input('A - Apostar, R - Rendirse: ')
    respuesta = respuesta.strip().upper()
    if respuesta == 'A' or respuesta == 'R':
        print('') # Imprimir un espacio
        return respuesta

    preguntar_jugada()

def mostrar_apuesta(apuesta_actual):
    print('La apuesta actual es: ' + str(apuesta_actual))

juego = { 'pozo': 0 }

jugadores = []
jugador_1 = { 'dinero': 100 }
jugador_2 = { 'dinero': 100 }
jugadores.append(jugador_1)
jugadores.append(jugador_2)

juego_activo = True
nuestro_jugador = 0
jugador_que_empieza = 0
apuesta_actual = 2

while juego_activo:
    poker = Poker(numero_de_jugadores, debug)
    if not poker:
        sys.exit('Numero de jugadores inválido')

    print('- Tus cartas -')
    poker.shuffle() # Revolver cartas
       
    players_hands = poker.distribute()
    if not players_hands:
        sys.exit('Cartas insuficientes')

    print('-----------------------')
    # Solo imprimir las cartas de nuestro jugador
    print('Tienes: ' + str(jugadores[nuestro_jugador]['dinero']) + ' Pozo: ' + str(juego['pozo']))
    mostrar_cartas_jugador(nuestro_jugador)
    mostrar_apuesta(apuesta_actual)
    jugada = preguntar_jugada()
    if jugada == 'A':
        apuesta_actual += 2
    else:
        apuesta_actual = 2

    # Obtener el "Flop" (Primeras tres cartas)
    carta = poker.getFlop()
    if not carta:
        sys.exit('Cartas insuficientes')
    cartas_comunes = carta
    mostrar_cartas_jugador(nuestro_jugador)
    mostrar_cartas_comunes(cartas_comunes)
    mostrar_apuesta(apuesta_actual)
    jugada = preguntar_jugada()
    if jugada == 'A':
        apuesta_actual += 2
    else:
        apuesta_actual = 2

    # Obtener la siguiente carta "Turn"
    carta = poker.getOne()
    if not carta:
        sys.exit('Cartas insuficientes')
    cartas_comunes.extend(carta)
    mostrar_cartas_jugador(nuestro_jugador)
    mostrar_cartas_comunes(cartas_comunes)
    mostrar_apuesta(apuesta_actual)
    jugada = preguntar_jugada()
    if jugada == 'A':
        apuesta_actual += 2
    else:
        apuesta_actual = 2

    # Obtener la quinta carta "River"
    carta = poker.getOne()
    if not carta:
        sys.exit('Cartas insuficientes')
    cartas_comunes.extend(carta)
    mostrar_cartas_jugador(nuestro_jugador)
    mostrar_cartas_comunes(cartas_comunes)
    mostrar_apuesta(apuesta_actual)
    jugada = preguntar_jugada()
    if jugada == 'A':
        apuesta_actual += 2
    else:
        apuesta_actual = 2

    try:
        results = poker.determine_score(cartas_comunes, players_hands)
    except:
        sys.exit("No se puede determinar la puntuación")

    try:
        ganador = poker.determine_winner(results)
    except:
        sys.exit('No se puede determinar el ganador')

    #Checks to see if the hand has ended in tie and displays the appropriate message         
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

    # TO DO: Repartir en caso de empate
    if empate == False:
        if ganador == nuestro_jugador:
            jugadores[nuestro_jugador]['dinero'] += apuesta_actual
        else:
            jugadores[nuestro_jugador]['dinero'] -= apuesta_actual

    # Inicializar
    apuesta_actual = 2

    print('')
    print('Siguiente jugada:')