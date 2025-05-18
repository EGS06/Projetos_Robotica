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
SENSOR_DIR = 0
SENSOR_ESQ = 0
PORTA_SENSOR_DIR = port.B
MOTOR_RODA_ESQ = port.C
MOTOR_RODA_DIR = port.D
MOTOR_CENTRAL = port.E

LIMIAR = 60
#tentar adicionar HISTERESE

def estouNaLinha(valor_sensor):
    if valor_sensor >= LIMIAR:
        print("Linha")
        sensor_linha = True
    else:
        print("Não linha")
        sensor_linha = False
    return sensor_linha

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
    await light_matrix.write("!")
    velocidade = 100
    while True:
        SENSOR_DIR = color_sensor.reflection(PORTA_SENSOR_DIR)
        SENSOR_ESQ = color_sensor.reflection(PORTA_SENSOR_ESQ)
        linhaEsq = estouNaLinha(SENSOR_ESQ)
        linhaDir = estouNaLinha(SENSOR_DIR)
        # sensor mais proximo 
        if (not linhaDir) and (not linhaEsq):
            frente(velocidade)
        elif linhaDir and (not linhaEsq):
            girarDireita(velocidade)
        elif (not linhaDir) and linhaEsq:
            girarEsquerda(velocidade)
        else:
            parar()
        await runloop.sleep_ms(10)

        # ORIGINAL
        # if (not linhaDir) and (not linhaEsq):
        #     frente(velocidade)
        # if linhaDir and (not linhaEsq):
        #     girarDireita(velocidade)
        # if (not linhaDir) and linhaEsq:
        #     girarEsquerda(velocidade)
        # if linhaDir and linhaEsq:
        #     parar()

        # VERSÃO MAIS ANTIGA
        # if color_sensor.reflection(PORTA_SENSOR_ESQ) > 60 & color_sensor.reflection(PORTA_SENSOR_DIR) > 65:
        #     parar()
        # if color_sensor.reflection(PORTA_SENSOR_ESQ) < 40 & color_sensor.reflection(PORTA_SENSOR_DIR) < 35:
        #     frente(100)
        # if color_sensor.reflection(PORTA_SENSOR_ESQ) > 60:
        #     girarEsquerda(100)
        # if color_sensor.reflection(PORTA_SENSOR_ESQ) > 65:
        #     girarDireita(100)

        # ADAPTAÇÃO DA VERSÃO ANTIGA USANDO AS COMPARAÇÕES MAIS DIRETAS
        # if (SENSOR_ESQ > 60) and (SENSOR_DIR > 65):
        #     parar()
        # elif (SENSOR_ESQ < 60) and (SENSOR_DIR < 65):
        #     frente(velocidade)
        # elif linhaEsq:
        #     girarEsquerda(velocidade)
        # else:
        #     girarDireita(velocidade)
runloop.run(main())
