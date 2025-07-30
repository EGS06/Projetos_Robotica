# motor porta D Motor da Direita não invertido
# motor porta C Motor da Esquerda invertido
#yaw sensor
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
# F = Sensor Parada

TEMPO_PARADA_MS = 2500
PORTA_SENSOR_ESQ = port.D
PORTA_SENSOR_DIR = port.C
PORTA_SENSOR_PARADA = port.E
MOTOR_RODA_ESQ = port.B
MOTOR_RODA_DIR = port.A
#MOTOR_CENTRAL = port.E
LINHA_CRUZ = 4

TEMPO_ENTRE_CRUZ = 2500

linha_esq = False
linha_dir = False
linha_final = False
agora = time.ticks_ms()
ult_tempo = time.ticks_ms()
contador = 0
contador_linha = 0

LIMIAR = 25

HISTERESE = 5

def atualizarSensores():
    global linha_esq
    global linha_dir
    SENSOR_ESQ = color_sensor.reflection(PORTA_SENSOR_ESQ)
    SENSOR_DIR = color_sensor.reflection(PORTA_SENSOR_DIR)
    if linha_esq:
        if SENSOR_ESQ < (LIMIAR - HISTERESE) :
            linha_esq = False
    else:
        if SENSOR_ESQ > (LIMIAR + HISTERESE) :
            linha_esq = True
    if linha_dir:
        if SENSOR_DIR < (LIMIAR - HISTERESE) :
            linha_dir = False
    else:
        if SENSOR_DIR > (LIMIAR + HISTERESE) :
            linha_dir = True

def sensorFinal():
    global linha_final
    SENSOR_FINAL = color_sensor.reflection(PORTA_SENSOR_PARADA)
    if linha_final:
        if SENSOR_FINAL < (LIMIAR - HISTERESE - 5) :
            linha_final = False
    else:
        if SENSOR_FINAL > (LIMIAR + HISTERESE + 5) :
            linha_final = True



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
    motor.run(MOTOR_RODA_DIR, int(velocidade))
    motor.run(MOTOR_RODA_ESQ, 0)

def girarDireita(velocidade):
    motor.run(MOTOR_RODA_DIR, 0)
    motor.run(MOTOR_RODA_ESQ, int(-velocidade))

posicao = 0
erro_anterior = 0
VELOCIDADE = 400
VELOCIDADE = 400 + contador * 50
async def seguirLinhaProporcional2():
    global posicao
    global erro_anterior
    maxVel = 600
    sensor_esq = color_sensor.reflection(PORTA_SENSOR_ESQ)
    sensor_dir = color_sensor.reflection(PORTA_SENSOR_DIR)

    sensor_esq = sensor_esq - 20
    if (sensor_esq < 0):
        sensor_esq = 0

    sensor_dir = sensor_dir - 20
    if (sensor_dir < 0):
        sensor_dir = 0

    erro = sensor_esq - sensor_dir
    derivada = erro - erro_anterior
    erro_anterior = erro
    if(erro == 0):
        erro = posicao
    else:
        posicao = erro


    proporcional = 8
    kd = 2


    ajuste = int(erro * proporcional + kd * derivada)
    vel_esq = -int(VELOCIDADE - ajuste)
    vel_dir = int(VELOCIDADE + ajuste)

    if(vel_esq < -maxVel):
        vel_esq = -maxVel
    elif (vel_esq > maxVel):
        vel_esq = maxVel

    if(vel_dir < -maxVel):
        vel_dir = -maxVel
    elif (vel_dir > maxVel):
        vel_dir = maxVel

    print("erro: ", erro, "esq: ", sensor_esq, "dir ", sensor_dir, "roda dir: ", vel_dir, "roda esq ", vel_esq)

    motor.run(MOTOR_RODA_ESQ, vel_esq)
    motor.run(MOTOR_RODA_DIR, vel_dir)

    await runloop.sleep_ms(10)



async def main():
    global linha_dir
    global linha_esq
    global contador_linha
    global agora
    global ult_tempo
    global contador
    light_matrix.write("!")
    while (contador < LINHA_CRUZ):
        # Sensor de parada
        agora = time.ticks_ms()
        sensorFinal()
        if linha_final:
            contador_linha = contador_linha + 1
            if contador_linha > 5:
                if((ult_tempo + TEMPO_ENTRE_CRUZ) < agora):
                    contador = contador + 1
                    light_matrix.write(str(contador))
                    ult_tempo = agora

        else:
            contador_linha = 0

        atualizarSensores()
        await seguirLinhaProporcional2()


    light_matrix.write("fim")
    ult_tempo = time.ticks_ms()
    while True:
        agora = time.ticks_ms()
        if (agora - ult_tempo > TEMPO_PARADA_MS):
            parar()
        else:
            atualizarSensores()
            await seguirLinhaProporcional2()




runloop.run(main())
