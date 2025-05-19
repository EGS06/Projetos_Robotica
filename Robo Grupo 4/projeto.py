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
SENSOR_ESQ = 0
SENSOR_DIR = 0
PORTA_SENSOR_DIR = port.B
MOTOR_RODA_ESQ = port.C
MOTOR_RODA_DIR = port.D
MOTOR_CENTRAL = port.E

linha_esq = False
linha_dir = False

LIMIAR = 50
HISTERESE = 5

SENSOR_ESQ = color_sensor.reflection(PORTA_SENSOR_ESQ)
if linha_esq:
    if SENSOR_ESQ > (LIMIAR + HISTERESE) :
        print("Linha", SENSOR_ESQ)
        linha_esq = True
else:
    if  SENSOR_ESQ < (LIMIAR - HISTERESE) :
        print("Não linha", SENSOR_ESQ)
        linha_esq = False

SENSOR_DIR = color_sensor.reflection(PORTA_SENSOR_DIR)
if linha_dir:
    if SENSOR_DIR > (LIMIAR + HISTERESE) :
        print("Linha", SENSOR_DIR)
        linha_dir = True
    else:
        if SENSOR_DIR < (LIMIAR - HISTERESE) :
            print("Não linha", SENSOR_DIR)
            linha_dir = False

# def estouNaLinha(valor_sensor):
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
        await light_matrix.write("!")
        velocidade = 100
        while True:
            # SENSOR_DIR = color_sensor.reflection(PORTA_SENSOR_DIR)
            # SENSOR_ESQ = color_sensor.reflection(PORTA_SENSOR_ESQ)
            # linhaEsq = estouNaLinha(SENSOR_ESQ)
            # linhaDir = estouNaLinha(SENSOR_DIR)
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

            # ORIGINAL
            # if (not linhaDir) and (not linhaEsq):
            #    frente(velocidade)
            # if linhaDir and (not linhaEsq):
            #    girarDireita(velocidade)
            # if (not linhaDir) and linhaEsq:
            #    girarEsquerda(velocidade)
            # if linhaDir and linhaEsq:
            #    parar()

            # VERSÃO MAIS ANTIGA
            # if color_sensor.reflection(PORTA_SENSOR_ESQ) > 60 & color_sensor.reflection(PORTA_SENSOR_DIR) > 65:
            #    parar()
            # if color_sensor.reflection(PORTA_SENSOR_ESQ) < 40 & color_sensor.reflection(PORTA_SENSOR_DIR) < 35:
            #    frente(100)
            # if color_sensor.reflection(PORTA_SENSOR_ESQ) > 60:
            #    girarEsquerda(100)
            # if color_sensor.reflection(PORTA_SENSOR_ESQ) > 65:
            #    girarDireita(100)

            # ADAPTAÇÃO DA VERSÃO ANTIGA USANDO AS COMPARAÇÕES MAIS DIRETAS
            # if (SENSOR_ESQ > 60) and (SENSOR_DIR > 65):
            #    parar()
            # elif (SENSOR_ESQ < 60) and (SENSOR_DIR < 65):
            #    frente(velocidade)
            # elif linhaEsq:
            #    girarEsquerda(velocidade)
            # else:
            #    girarDireita(velocidade)
    runloop.run(main())
