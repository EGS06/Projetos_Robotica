from hub import light_matrix, port
import runloop
import time
import color_sensor
import motor

# Configurações
TEMPO_PARADA_MS = 2500
PORTA_SENSOR_ESQ = port.D
PORTA_SENSOR_DIR = port.C
PORTA_SENSOR_PARADA = port.E                                       
MOTOR_RODA_ESQ = port.B
MOTOR_RODA_DIR = port.A
LINHA_CRUZ = 4
VELOCIDADE = 400
TEMPO_ENTRE_CRUZ = 5000
LIMIAR = 25
HISTERESE = 5

# Variáveis globais
linha_final = False
agora = time.ticks_ms()
ult_tempo = time.ticks_ms()
contador = 0
contador_linha = 0

# Variáveis PID
erro_anterior = 0
integral = 0
Kp = 2.0
Ki = 0.01
Kd = 1.2

# Funções PID
def calcular_PID(erro, erro_anterior, integral):
    integral += erro
    derivativo = erro - erro_anterior
    saida = Kp * erro + Ki * integral + Kd * derivativo
    return saida, integral, erro

# Movimento
def parar():
    motor.run(MOTOR_RODA_DIR, 0)
    motor.run(MOTOR_RODA_ESQ, 0)

def sensorFinal():
    global linha_final
    SENSOR_FINAL = color_sensor.reflection(PORTA_SENSOR_PARADA)
    print('sf', SENSOR_FINAL)
    if linha_final:
        if SENSOR_FINAL < (LIMIAR - HISTERESE - 5):
            print("Não linha parada", SENSOR_FINAL)
            linha_final = False
    else:
        if SENSOR_FINAL > (LIMIAR + HISTERESE + 5):
            print("linha Parada", SENSOR_FINAL)
            linha_final = True

# Loop principal
async def main():
    global contador, contador_linha, agora, ult_tempo
    global erro_anterior, integral

    light_matrix.write("2/1")

    while contador < LINHA_CRUZ:
        agora = time.ticks_ms()
        
        # Sensor de parada (cruzamento)
        sensorFinal()
        if linha_final:
            contador_linha += 1
            if contador_linha > 5:
                if time.ticks_diff(agora, ult_tempo) > TEMPO_ENTRE_CRUZ:
                    contador += 1
                    light_matrix.write(str(contador))
                    ult_tempo = agora
                    print("Cruzamento detectado:", contador)
        else:
            contador_linha = 0

        # Leitura dos sensores laterais
        ref_esq = color_sensor.reflection(PORTA_SENSOR_ESQ)
        ref_dir = color_sensor.reflection(PORTA_SENSOR_DIR)
        erro = ref_esq - ref_dir

        # PID
        ajuste, integral, erro_anterior = calcular_PID(erro, erro_anterior, integral)
        vel_esq = VELOCIDADE - ajuste
        vel_dir = VELOCIDADE + ajuste

        # Limitador de velocidade
        vel_esq = max(min(vel_esq, 1000), -1000)
        vel_dir = max(min(vel_dir, 1000), -1000)

        motor.run(MOTOR_RODA_ESQ, -int(vel_esq))  # Motor invertido
        motor.run(MOTOR_RODA_DIR, int(vel_dir))

    # Fim da linha
    light_matrix.write("fim")
    ult_tempo = time.ticks_ms()

    while True:
        agora = time.ticks_ms()
        if time.ticks_diff(agora, ult_tempo) > TEMPO_PARADA_MS:
            parar()
        else:
            # Continua corrigindo a linha até parar
            ref_esq = color_sensor.reflection(PORTA_SENSOR_ESQ)
            ref_dir = color_sensor.reflection(PORTA_SENSOR_DIR)
            erro = ref_esq - ref_dir
            ajuste, integral, erro_anterior = calcular_PID(erro, erro_anterior, integral)
            vel_esq = VELOCIDADE - ajuste
            vel_dir = VELOCIDADE + ajuste

            vel_esq = max(min(vel_esq, 1000), -1000)
            vel_dir = max(min(vel_dir, 1000), -1000)

            motor.run(MOTOR_RODA_ESQ, -int(vel_esq))
            motor.run(MOTOR_RODA_DIR, int(vel_dir))

runloop.run(main())
