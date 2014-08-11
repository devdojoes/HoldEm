# -*- coding: utf-8 -*-
"""
Cosas por hacer:
- Limitar rapuestas cuando un jugador tiene menos puntos
- ¿Qué pasa cuand olos dos jugadores se
- Probar si corre bien con Python 3
"""
import motor_de_poker as poker
import random

def mostrar_cartas(cartas):
    """Leer una una lista de cartas y mostrar el texto"""
    texto = ''

    for carta in cartas:
        texto += carta + ' '

    print(texto)

def preguntar_jugada():
    """Preguntar por el teclado la siguiente jugada"""
    respuesta = raw_input('A - Apostar, R - Rendirse: ')
    respuesta = respuesta.strip().upper()
    if respuesta == 'A' or respuesta == 'R':
        print('') # Imprimir un espacio
        return respuesta

    preguntar_jugada()

def leer_jugada_del_bot(cartas_jugador, cartas_comunes, puntuacion):
    if random.randrange(10) > 8:
        return 'R'
    else:
        return 'A'

def mostrar_apuesta(apuesta_actual):
    print('\nPor apostar: ' + str(apuesta_actual))

def agregar_cartas(mazo, num_cartas, cartas_actuales):
    for _ in xrange(num_cartas):
        cartas_actuales.extend(mazo.pop())

def mostrar_apuestas():
    global apuesta_actual
    global nuestro_jugador
    global jugador_oponente
    global juego

    jugadores[nuestro_jugador]['dinero'] -= apuesta_actual
    jugadores[jugador_oponente]['dinero'] -= apuesta_actual
    juego['pozo'] += apuesta_actual * 2
    print('')
    print('        Apuestas: ' + str(apuesta_actual))
    print('Oponente apuesta: ' + str(apuesta_actual))
    print('            Pozo: ' + str(juego['pozo']))

def mostrar_mejor_mano(cartas):
    mejor_mano = sorted(poker.best_hand(cartas))
    print('\nMejor mano ' + \
        str(mejor_mano) + \
        ' (' + str(poker.hand_names[poker.hand_rank(mejor_mano)[0]]) + ')')
    print('Desempate: ' + str(poker.hand_rank(mejor_mano)))

# Inicializar condiciones del juego
juego = { 'pozo': 0 }
jugadores = [{ 'dinero': 100, 'victorias': 0 }, { 'dinero': 100, 'victorias': 0 }]

juego_activo = True
nuestro_jugador = 0
jugador_oponente = 1
apuesta_actual = 1
mano_actual = 1
cartas_jugador = {}
cartas_comunes = []

def repartir_cartas():
    global juego
    global nuestro_jugador
    global jugador_oponente
    global apuesta_actual
    global jugadores
    global cartas_comunes
    global cartas_jugador

    mazo = poker.deal(32, 1)

    cartas_jugador[nuestro_jugador] = []
    cartas_jugador[jugador_oponente] = []
    cartas_comunes = []

    apuesta_actual = 1
    mostrar_apuestas()

    # Repartir dos cartas a cada jugador
    agregar_cartas(mazo, 2, cartas_jugador[nuestro_jugador])
    agregar_cartas(mazo, 2, cartas_jugador[jugador_oponente])

    print('\nTus cartas iniciales')
    mostrar_cartas(cartas_jugador[nuestro_jugador])

    apuesta_actual = 1
    mostrar_apuesta(apuesta_actual)

    jugada_jugador = preguntar_jugada()
    jugada_bot = leer_jugada_del_bot(cartas_jugador[jugador_oponente], cartas_comunes, juego)
    if jugada_jugador == 'R' and jugada_bot == 'R':
        return 'Ambos'
    elif jugada_jugador == 'R':
        return 'Jug1'
    elif jugada_bot == 'R':
        return 'Jug2'

    mostrar_apuestas()

    # Obtener el "Flop" (Primeras tres cartas)
    print('Cartas comunes')
    agregar_cartas(mazo, 3, cartas_comunes)

    mostrar_cartas(cartas_jugador[nuestro_jugador])
    mostrar_cartas(cartas_comunes)
    mostrar_mejor_mano(cartas_jugador[nuestro_jugador] + cartas_comunes)

    apuesta_actual = 2
    mostrar_apuesta(apuesta_actual)

    jugada_jugador = preguntar_jugada()
    jugada_bot = leer_jugada_del_bot(cartas_jugador[jugador_oponente], cartas_comunes, juego)
    if jugada_jugador == 'R' and jugada_bot == 'R':
        return 'Ambos'
    elif jugada_jugador == 'R':
        return 'Jug1'
    elif jugada_bot == 'R':
        return 'Jug2'

    mostrar_apuestas()

    # Obtener la siguiente carta "Turn"
    agregar_cartas(mazo, 1, cartas_comunes)

    mostrar_cartas(cartas_jugador[nuestro_jugador])
    mostrar_cartas(cartas_comunes)
    mostrar_mejor_mano(cartas_jugador[nuestro_jugador] + cartas_comunes)

    apuesta_actual = 4
    mostrar_apuesta(apuesta_actual)

    jugada_jugador = preguntar_jugada()
    jugada_bot = leer_jugada_del_bot(cartas_jugador[jugador_oponente], cartas_comunes, juego)
    if jugada_jugador == 'R' and jugada_bot == 'R':
        return 'Ambos'
    elif jugada_jugador == 'R':
        return 'Jug1'
    elif jugada_bot == 'R':
        return 'Jug2'

    mostrar_apuestas()

    # Obtener la quinta carta "River"
    agregar_cartas(mazo, 1, cartas_comunes)

    mostrar_cartas(cartas_jugador[nuestro_jugador])
    mostrar_cartas(cartas_comunes)
    mostrar_mejor_mano(cartas_jugador[nuestro_jugador] + cartas_comunes)

    apuesta_actual = 8
    mostrar_apuesta(apuesta_actual)

    jugada_jugador = preguntar_jugada()
    jugada_bot = leer_jugada_del_bot(cartas_jugador[jugador_oponente], cartas_comunes, juego)
    if jugada_jugador == 'R' and jugada_bot == 'R':
        return 'Ambos'
    elif jugada_jugador == 'R':
        return 'Jug1'
    elif jugada_bot == 'R':
        return 'Jug2'

    mostrar_apuestas()

    return 'Nadie' # Nadie se rindió

while juego_activo:
    print('         - Mano # ' + str(mano_actual) + ' -')

    print('------------------------------')
    print('        Tu tienes: ' + str(jugadores[nuestro_jugador]['dinero']))
    print('Tu oponente tiene: ' + str(jugadores[jugador_oponente]['dinero']))
    print('             Pozo: ' + str(juego['pozo']))

    resultado = repartir_cartas()

    # ¿Quién se rindió?
    if resultado == 'Jug1':
        jugadores[jugador_oponente]['dinero'] += juego['pozo']
        jugadores[jugador_oponente]['victorias'] += 1
    if resultado == 'Jug2':
        print('El oponente se rinde')
        jugadores[nuestro_jugador]['dinero'] += juego['pozo']
        jugadores[nuestro_jugador]['victorias'] += 1
    if resultado == 'Ambos':
        # Se acaba la ronda y se reparten los puntos
        print('Ambos se rinden')
        jugadores[nuestro_jugador]['dinero'] += int(juego['pozo'] / 2)
        jugadores[jugador_oponente]['dinero'] += int(juego['pozo'] / 2)
    elif resultado == 'Nadie':
        # Calcular y mostrar las mejores manos
        mejor_mano_1 = sorted(poker.best_hand(cartas_jugador[nuestro_jugador] + cartas_comunes))
        mejor_mano_2 = sorted(poker.best_hand(cartas_jugador[jugador_oponente] + cartas_comunes))

        print('')
        print('Tus cartas')
        mostrar_cartas(cartas_jugador[nuestro_jugador])
        print('\nCartas comunes')
        mostrar_cartas(cartas_comunes)
        print('\nCartas del oponente')
        mostrar_cartas(cartas_jugador[jugador_oponente])

        print('Mejor mano de nuestro jugador')
        print(mejor_mano_1)
        print(poker.hand_names[poker.hand_rank(mejor_mano_1)[0]])
        print('Ranking: ' + str(poker.hand_rank(mejor_mano_1)))

        print('')
        print('Mejor mano del oponente')
        print(mejor_mano_2)
        print(poker.hand_names[poker.hand_rank(mejor_mano_2)[0]])
        print('Ranking: ' + str(poker.hand_rank(mejor_mano_2)))
        print('')

        if (poker.hand_rank(mejor_mano_1) > poker.hand_rank(mejor_mano_2)):
            print('Gana nuestro jugador')
            jugadores[nuestro_jugador]['dinero'] += juego['pozo']
            jugadores[nuestro_jugador]['victorias'] += 1
        elif (poker.hand_rank(mejor_mano_1) < poker.hand_rank(mejor_mano_2)):
            print('Gana el oponente')
            jugadores[jugador_oponente]['dinero'] += juego['pozo']
            jugadores[jugador_oponente]['victorias'] += 1
        else:
            print('Empate')
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

if jugadores[nuestro_jugador]['dinero'] > jugadores[jugador_oponente]['dinero']:
    print('Gana nuestro jugador')
else:
    print('Gana el oponente')