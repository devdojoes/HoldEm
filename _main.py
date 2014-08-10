# -*- coding: utf-8 -*-
from holdem import Poker
import sys

debug = True
numero_de_jugadores = 2

def mostrar_cartas_jugador(num_jugador):
    texto = '\n  Tus cartas: '
    for carta in players_hands[num_jugador]:
        texto += str(carta) + ' '
    print(texto)

def mostrar_cartas_oponente(num_jugador):
    texto = '    Oponente: '
    for carta in players_hands[num_jugador]:
        texto += str(carta) + ' '
    print(texto)

def mostrar_cartas_comunes(community_cards):
    texto = '     Comunes: '
    for carta in community_cards:
        texto += str(carta) + ' '
    print(texto)

def preguntar_jugada():
    print('')
    respuesta = raw_input('A - Apostar, R - Rendirse: ')
    respuesta = respuesta.strip().upper()
    if respuesta == 'A' or respuesta == 'R':
        print('') # Imprimir un espacio
        return respuesta

    preguntar_jugada()

def accion_bot():
    print('')

def mostrar_apuesta(apuesta_actual):
    print('Apuesta actual: ' + str(apuesta_actual))

juego = { 'pozo': 0 }
jugadores = [{ 'dinero': 100, 'victorias': 0 }, { 'dinero': 100, 'victorias': 0 }]

juego_activo = True
nuestro_jugador = 0
jugador_oponente = 1
jugador_que_empieza = 0
apuesta_actual = 1
mano_actual = 1

cartas_comunes = []

poker = Poker(numero_de_jugadores, debug)
players_hands = poker.distribute()

def repartir_cartas():
    global nuestro_jugador
    global apuesta_actual
    global jugadores
    global juego
    global cartas_comunes

    mostrar_cartas_jugador(nuestro_jugador)
    mostrar_apuesta(apuesta_actual)
    apuesta_actual = 1

    print('')
    print('Apuestas: ' + str(apuesta_actual))
    print('Oponente apuesta: ' + str(apuesta_actual))
    jugadores[nuestro_jugador]['dinero'] -= apuesta_actual
    jugadores[jugador_oponente]['dinero'] -= apuesta_actual
    juego['pozo'] += apuesta_actual * 2
    print('Pozo: ' + str(juego['pozo']))

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
        apuesta_actual = 1
    else:
        return False

    print('')
    print('Apuestas: ' + str(apuesta_actual))
    print('Oponente apuesta: ' + str(apuesta_actual))
    jugadores[nuestro_jugador]['dinero'] -= apuesta_actual
    jugadores[jugador_oponente]['dinero'] -= apuesta_actual
    juego['pozo'] += apuesta_actual * 2
    print('Pozo: ' + str(juego['pozo']))

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
        apuesta_actual = 2
    else:
        return False

    print('')
    print('Apuestas: ' + str(apuesta_actual))
    print('Oponente apuesta: ' + str(apuesta_actual))
    jugadores[nuestro_jugador]['dinero'] -= apuesta_actual
    jugadores[jugador_oponente]['dinero'] -= apuesta_actual
    juego['pozo'] += apuesta_actual * 2
    print('Pozo: ' + str(juego['pozo']))

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
        apuesta_actual = 4
    else:
        return False

    print('')
    print('Apuestas: ' + str(apuesta_actual))
    print('Oponente apuesta: ' + str(apuesta_actual))
    jugadores[nuestro_jugador]['dinero'] -= apuesta_actual
    jugadores[jugador_oponente]['dinero'] -= apuesta_actual
    juego['pozo'] += apuesta_actual * 2
    print('Pozo: ' + str(juego['pozo']))

    return True

while juego_activo:
    poker = Poker(numero_de_jugadores, debug)
    if not poker:
        sys.exit('Numero de jugadores inválido')

    print('- Mano #' + str(mano_actual) + ' -')
    poker.shuffle() # Revolver cartas

    players_hands = poker.distribute()
    if not players_hands:
        sys.exit('Cartas insuficientes')

    print('-----------------------')
    # Solo imprimir las cartas de nuestro jugador
    print('        Tu tienes: ' + str(jugadores[nuestro_jugador]['dinero']))
    print('Tu oponente tiene: ' + str(jugadores[jugador_oponente]['dinero']) + ' Pozo: ' + str(juego['pozo']))

    resultado = repartir_cartas()

    if resultado == False:
        jugadores[jugador_oponente]['dinero'] += juego['pozo']
        jugadores[jugador_oponente]['victorias'] += 1
    elif resultado == True:
        mostrar_cartas_jugador(nuestro_jugador)
        mostrar_cartas_oponente(jugador_oponente)
        mostrar_cartas_comunes(cartas_comunes)

        try:
            results = poker.determine_score(cartas_comunes, players_hands)
        except:
            sys.exit("No se puede determinar la puntuación")

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

        # TO DO: Repartir en caso de empate
        if empate == False:
            if ganador == nuestro_jugador:
                jugadores[nuestro_jugador]['dinero'] += juego['pozo']
                jugadores[nuestro_jugador]['victorias'] += 1
            else:
                jugadores[jugador_oponente]['dinero'] += juego['pozo']
                jugadores[jugador_oponente]['victorias'] += 1
        else:
            jugadores[nuestro_jugador]['dinero'] += int(juego['pozo'] / 2)
            jugadores[jugador_oponente]['dinero'] += int(juego['pozo'] / 2)

    # Inicializar
    apuesta_actual = 1
    juego['pozo'] = 0
    mano_actual += 1

    print('')

    if jugadores[nuestro_jugador]['dinero'] < 0 or jugadores[jugador_oponente]['dinero'] < 0:
        juego_activo = False

    raw_input('Aprieta enter para continuar')

# Mostrar las victorias de cada jugador
print('Victorias Jugador 1: ' + str(jugadores[0]['victorias']))
print('Victorias Jugador 2: ' + str(jugadores[1]['victorias']))
