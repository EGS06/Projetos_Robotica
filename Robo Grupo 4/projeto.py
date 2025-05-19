# motor porta D Motor da Direita não invertido
# motor porta C Motor da Esquerda invertido
from hub import light_matrix, port
import runloop
import time
import color
import color_sensor
import motor

# A = Sensor Esquerda
# B = Sensor Direita
# C = Motor Roda esquerda
# D = Motor Roda DIreita
# E = Motor Central
# F = Nada

PORTA_SENSOR_ESQ = port.A
PORTA_SENSOR_DIR = port.B
MOTOR_RODA_ESQ = port.C
MOTOR_RODA_DIR = port.D
MOTOR_CENTRAL = port.E

linha_esq = False
linha_dir = False

LIMIAR = 50
HISTERESE = 5

def atualizarSensores():
    global linha_esq
    global linha_dir 
    SENSOR_ESQ = color_sensor.reflection(PORTA_SENSOR_ESQ)
    SENSOR_DIR = color_sensor.reflection(PORTA_SENSOR_DIR)
    print('se', SENSOR_ESQ, 'sd', SENSOR_DIR)
    if linha_esq:
        if SENSOR_ESQ < (LIMIAR - HISTERESE) :
            print("Não Linha Esquerda", SENSOR_ESQ)
            linha_esq = False
    else:
        if SENSOR_ESQ > (LIMIAR + HISTERESE) :
            print("linha Esquerda", SENSOR_ESQ)
            linha_esq = True
    print("foi pra baixo")
    if linha_dir:
        if SENSOR_DIR < (LIMIAR - HISTERESE) :
            print("Não Linha Direita", SENSOR_DIR)
            linha_dir = False
    else:
       if SENSOR_DIR > (LIMIAR + HISTERESE) :
            print("linha Direita", SENSOR_DIR)
            linha_dir = True
    print(linha_esq, linha_dir)
# def atualizarSensores(valor_sensor):
#    if valor_sensor > (LIMIAR + HISTERESE):
#        print("Linha", valor_sensor)
#        sensor_linha = True
#    elif valor_sensor < (LIMIAR - HISTERESE):
#        print("Não linha", valor_sensor)
#        sensor_linha = False
#    else:
#        sensor_linha = False
#    return sensor_linha

def tras(velocidade):
    motor.run(MOTOR_RODA_DIR, -velocidade)
    motor.run(MOTOR_RODA_ESQ, velocidade)

def frente(velocidade):
    motor.run(MOTOR_RODA_DIR, velocidade)
    motor.run(MOTOR_RODA_ESQ, -velocidade)

def parar():
    velocidade = 0
    motor.run(MOTOR_RODA_DIR, -velocidade)
    motor.run(MOTOR_RODA_ESQ, velocidade)

def girarEsquerda(velocidade):
    motor.run(MOTOR_RODA_DIR, velocidade)
    motor.run(MOTOR_RODA_ESQ, 0)

def girarDireita(velocidade):
    motor.run(MOTOR_RODA_DIR, 0)
    motor.run(MOTOR_RODA_ESQ, -velocidade)


async def main():
    global linha_dir
    global linha_esq
    await light_matrix.write("!")
    velocidade = 100
    while True:
        atualizarSensores()
        # sensor mais proximo
        if (not linha_dir) and (not linha_esq):
            frente(velocidade)
        elif linha_dir and (not linha_esq):
            girarDireita(velocidade)
        elif (not linha_dir) and linha_esq:
            girarEsquerda(velocidade)
        else:
            parar()
        await runloop.sleep_ms(10)

runloop.run(main())
