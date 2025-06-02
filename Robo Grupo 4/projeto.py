# motor porta D Motor da Direita não invertido
# motor porta C Motor da Esquerda invertido
from hub import light_matrix, port
import runloop
import time
import color
import color_sensor
import motor
# testar controlar velocidade de motores
# testar logica pois se uma das rodas ja estiver parada quandos os dois verem branco, a roda que ja estava parada cobntinua parada
# verificar sensores de parada

# A = Sensor Esquerda
# B = Sensor Direita
# C = Motor Roda esquerda
# D = Motor Roda DIreita
# E = Motor Central
# F = Sensor Parada

TEMPO_PARADA_MS = 2500
PORTA_SENSOR_ESQ = port.A
PORTA_SENSOR_DIR = port.B
PORTA_SENSOR_PARADA = port.F
MOTOR_RODA_ESQ = port.C
MOTOR_RODA_DIR = port.D
MOTOR_CENTRAL = port.E
LINHA_CRUZ = 4
VELOCIDADE = 600
TEMPO_ENTRE_CRUZ = 5000

linha_esq = False
linha_dir = False
linha_final = False
agora = time.ticks_ms()
ult_tempo = time.ticks_ms()
contador = 0
contador_linha = 0

LIMIAR = 30
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

def sensorFinal():
    global linha_final
    SENSOR_FINAL = color_sensor.reflection(PORTA_SENSOR_PARADA)
    print('sf', SENSOR_FINAL)
    if linha_final:
        if SENSOR_FINAL < (LIMIAR - HISTERESE - 5) :
            print("Não linha parada", SENSOR_FINAL)
            linha_final = False
    else:
        if SENSOR_FINAL > (LIMIAR + HISTERESE + 5) :
            print("linha Parada", SENSOR_FINAL)
            linha_final = True
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
    motor.run(MOTOR_RODA_DIR, 0)
    motor.run(MOTOR_RODA_ESQ, 0)

def girarEsquerda(velocidade):
    motor.run(MOTOR_RODA_DIR, velocidade)
    motor.run(MOTOR_RODA_ESQ, 0)

def girarDireita(velocidade):
    motor.run(MOTOR_RODA_DIR, 0)
    motor.run(MOTOR_RODA_ESQ, -velocidade)

def seguirLinha(linha_dir, linha_esq):
    if (not linha_dir) and (not linha_esq):
        frente(VELOCIDADE)
    elif linha_dir and (not linha_esq):
        girarDireita(VELOCIDADE)
    elif (not linha_dir) and linha_esq:
        girarEsquerda(VELOCIDADE)
    else:
        frente(VELOCIDADE)

async def main():
    global linha_dir
    global linha_esq
    global contador_linha
    global agora
    global ult_tempo
    global contador
    light_matrix.write("att")
    while (contador < LINHA_CRUZ):
        # Sensor de parada
        agora = time.ticks_ms()
        sensorFinal()
        if linha_final:
            contador_linha = contador_linha + 1
            print("viu linha")
            if contador_linha > 5:
                if((ult_tempo + TEMPO_ENTRE_CRUZ) < agora):
                    contador = contador + 1
                    light_matrix.write(str(contador))
                    ult_tempo = agora
                    print("confirmou linha")
                    print("numero de cruzamentos" , contador)
        else:
            contador_linha = 0
            print("n era linha")

        # Sensores de movimento
        atualizarSensores()
        seguirLinha(linha_dir, linha_esq)
        

    light_matrix.write("fim")
    ult_tempo = time.ticks_ms()
    while True:
        agora = time.ticks_ms()
        if (agora - ult_tempo > TEMPO_PARADA_MS):
            parar()
    

runloop.run(main())
