
from hub import port, sound
import color_sensor
import motor
import runloop
import utime
import distance_sensor


# =========================================================
# PARTE 1 - CONFIGURAÇÕES DO SEGUE-LINHA
# =========================================================

VELOCIDADE = -280
KP = 7.2

PRETO = 20
VERDE = 6
VERMELHO = 9

FRENTE = 780
VIRADA = 950
GIRO_180 = 2650
RE = 400

ESPERA_VERDE = 120

VELOCIDADE_DASH_PRETO = -550
TEMPO_DASH_PRETO = 800
BLOQUEIO_VERDE_APOS_PRETO = 1000

DISTANCIA_OBSTACULO = 60
TEMPO_CONFIRMA_OBSTACULO = 50

# =========================================================
# DESVIO DE OBSTÁCULO DA PISTA
#
# 90° DIREITA
# 1 SEGUNDO
# 90° ESQUERDA
# 3 SEGUNDOS
# 90° ESQUERDA
# 1 SEGUNDO
# =========================================================

DESVIO_90 = VIRADA

TEMPO_OBSTACULO_1 = 1000
TEMPO_OBSTACULO_2 = 3000
TEMPO_OBSTACULO_3 = 1000

# =========================================================
# SOM - DOIS PRETOS
# =========================================================

SOM_DOIS_PRETOS_FREQ = 1000
SOM_DOIS_PRETOS_DURACAO = 150
SOM_DOIS_PRETOS_VOLUME = 100

JANELA_IGNORAR_VERDE_APOS_PRETO = 500


# =========================================================
# PARTE 2 - ÁREA DE RESGATE
# =========================================================

ULTRASSOM = port.C

MOTOR_ESQUERDO = port.A
MOTOR_DIREITO = port.D

SENSOR_F = port.F
SENSOR_B = port.B

TEMPO_1CM_SAIDA = 350
TEMPO_2CM_BUSCA = 700

VELOCIDADE_RE_ENTRADA_RESGATE = 280

# =========================================================
# SAÍDA DA SALA
# =========================================================

ANGULO_ENTRADA_MIN = 160
ANGULO_ENTRADA_MAX = 230

REFLEXAO_PRETO = 30

MAX_PASSOS_SAIDA = 20

TOLERANCIA_PAREDE = 40


# =========================================================
# TRANSIÇÃO PARA SALA DE RESGATE
# =========================================================

DISTANCIA_ENTRADA_RESGATE = 60
TEMPO_CONFIRMA_ENTRADA_RESGATE = 50

DISTANCIA_LIMITE_PAREDE_RESGATE = 900

DISTANCIA_RE_ENTRADA_RESGATE = 460


# =========================================================
# ORIENTAÇÃO GLOBAL
# =========================================================

angulo_atual = 0


# =========================================================
# FUNÇÕES DO SEGUE-LINHA
# =========================================================

def set_motores(vel_esq, vel_dir):
    motor.run(port.A, vel_esq)
    motor.run(port.D, -vel_dir)


async def parar():
    set_motores(0, 0)


def sensor_esquerdo_verde():
    return color_sensor.color(port.F) == VERDE


def sensor_direito_verde():
    return color_sensor.color(port.B) == VERDE


def tipo_verde():

    esq = sensor_esquerdo_verde()
    dir = sensor_direito_verde()

    if esq and dir:
        return "DOIS"

    elif esq:
        return "ESQUERDA"

    elif dir:
        return "DIREITA"

    return "NENHUM"


async def confirmar_verde():

    primeira_leitura = tipo_verde()

    if primeira_leitura == "NENHUM":
        return "NENHUM"

    if primeira_leitura == "DOIS":
        return "DOIS"

    await parar()

    await runloop.sleep_ms(ESPERA_VERDE)

    segunda_leitura = tipo_verde()

    if segunda_leitura == "DOIS":
        return "DOIS"

    return primeira_leitura


def detectou_vermelho():

    return (
        color_sensor.color(port.F) == VERMELHO
        and
        color_sensor.color(port.B) == VERMELHO
    )


def detectou_dois_pretos():

    return (
        color_sensor.reflection(port.F) < PRETO
        and
        color_sensor.reflection(port.B) < PRETO
    )


def detectou_algum_preto():

    return (
        color_sensor.reflection(port.F) < PRETO
        or
        color_sensor.reflection(port.B) < PRETO
    )


def detectou_obstaculo():

    distancia = distance_sensor.distance(port.C)

    if distancia == -1:
        return False

    return distancia <= DISTANCIA_OBSTACULO


# =========================================================
# CURVAS DO SEGUE-LINHA
# =========================================================

async def virar_esquerda():

    set_motores(VELOCIDADE, VELOCIDADE)

    await runloop.sleep_ms(FRENTE)

    motor.run(port.A, -VELOCIDADE)
    motor.run(port.D, -VELOCIDADE)

    await runloop.sleep_ms(VIRADA)


async def virar_direita():

    set_motores(VELOCIDADE, VELOCIDADE)

    await runloop.sleep_ms(FRENTE)

    motor.run(port.A, VELOCIDADE)
    motor.run(port.D, VELOCIDADE)

    await runloop.sleep_ms(VIRADA)


async def fazer_180():

    set_motores(-VELOCIDADE, -VELOCIDADE)

    await runloop.sleep_ms(RE)

    motor.run(port.A, VELOCIDADE)
    motor.run(port.D, VELOCIDADE)

    await runloop.sleep_ms(GIRO_180)


# =========================================================
# DOIS PRETOS
# =========================================================

async def dois_pretos():

    await sound.beep(
        SOM_DOIS_PRETOS_FREQ,
        SOM_DOIS_PRETOS_DURACAO,
        SOM_DOIS_PRETOS_VOLUME
    )

    inicio = utime.ticks_ms()

    while utime.ticks_diff(
        utime.ticks_ms(),
        inicio
    ) < TEMPO_DASH_PRETO:

        set_motores(
            VELOCIDADE_DASH_PRETO,
            VELOCIDADE_DASH_PRETO
        )

        await runloop.sleep_ms(10)


# =========================================================
# DESVIO DE OBSTÁCULO DA PISTA
#
# 90° DIREITA
# 1 SEGUNDO
# 90° ESQUERDA
# 3 SEGUNDOS
# 90° ESQUERDA
# 1 SEGUNDO
# =========================================================

async def desviar_obstaculo():

    await parar()

    await runloop.sleep_ms(100)

    print("")
    print("================================")
    print("    DESVIO DE OBSTACULO")
    print("================================")

    # -----------------------------------------------------
    # 1 - 90° DIREITA
    # -----------------------------------------------------

    print("1 - 90 GRAUS DIREITA")

    motor.run(port.A, VELOCIDADE)
    motor.run(port.D, VELOCIDADE)

    await runloop.sleep_ms(DESVIO_90)

    motor.stop(port.A)
    motor.stop(port.D)

    await runloop.sleep_ms(100)

    # -----------------------------------------------------
    # 2 - ANDAR 1 SEGUNDO
    # -----------------------------------------------------

    print("2 - ANDANDO 1 SEGUNDO")

    set_motores(
        VELOCIDADE,
        VELOCIDADE
    )

    await runloop.sleep_ms(
        TEMPO_OBSTACULO_1
    )

    await parar()

    await runloop.sleep_ms(100)

    # -----------------------------------------------------
    # 3 - 90° ESQUERDA
    # -----------------------------------------------------

    print("3 - 90 GRAUS ESQUERDA")

    motor.run(port.A, -VELOCIDADE)
    motor.run(port.D, -VELOCIDADE)

    await runloop.sleep_ms(DESVIO_90)

    motor.stop(port.A)
    motor.stop(port.D)

    await runloop.sleep_ms(100)

    # -----------------------------------------------------
    # 4 - ANDAR 3 SEGUNDOS
    # -----------------------------------------------------

    print("4 - ANDANDO 3 SEGUNDOS")

    set_motores(
        VELOCIDADE,
        VELOCIDADE
    )

    await runloop.sleep_ms(
        TEMPO_OBSTACULO_2
    )

    await parar()

    await runloop.sleep_ms(100)

    # -----------------------------------------------------
    # 5 - 90° ESQUERDA
    # -----------------------------------------------------

    print("5 - 90 GRAUS ESQUERDA")

    motor.run(port.A, -VELOCIDADE)
    motor.run(port.D, -VELOCIDADE)

    await runloop.sleep_ms(DESVIO_90)

    motor.stop(port.A)
    motor.stop(port.D)

    await runloop.sleep_ms(100)

    # -----------------------------------------------------
    # 6 - ANDAR 1 SEGUNDO
    # -----------------------------------------------------

    print("6 - ANDANDO 1 SEGUNDO")

    set_motores(
        VELOCIDADE,
        VELOCIDADE
    )

    await runloop.sleep_ms(
        TEMPO_OBSTACULO_3
    )

    await parar()

    await runloop.sleep_ms(100)

    print("")
    print("================================")
    print("    DESVIO FINALIZADO")
    print("================================")


# =========================================================
# SEGUE-LINHA
# =========================================================

def seguir_linha():

    esq = color_sensor.reflection(port.F)
    dir = color_sensor.reflection(port.B)

    erro = dir - esq

    correcao = int(KP * erro)

    vel_esq = max(
        -1000,
        min(1000, VELOCIDADE + correcao)
    )

    vel_dir = max(
        -1000,
        min(1000, VELOCIDADE - correcao)
    )

    set_motores(
        vel_esq,
        vel_dir
    )


# =========================================================
# FUNÇÕES DA ÁREA DE RESGATE
# =========================================================

def medir():

    distancia = distance_sensor.distance(
        ULTRASSOM
    )

    if distancia < 0:
        return 9999

    return distancia


def sensor_preto(porta):

    reflexao = color_sensor.reflection(porta)
    cor = color_sensor.color(porta)

    return (
        reflexao <= REFLEXAO_PRETO
        and
        cor == 0
    )


def saiu_da_area():

    preto_f = sensor_preto(SENSOR_F)
    preto_b = sensor_preto(SENSOR_B)

    return preto_f or preto_b


def normalizar(angulo):

    while angulo >= 360:
        angulo -= 360

    while angulo < 0:
        angulo += 360

    return angulo


def eh_entrada(angulo):

    angulo = normalizar(angulo)

    return (
        ANGULO_ENTRADA_MIN
        <= angulo
        <= ANGULO_ENTRADA_MAX
    )


# =========================================================
# GIROS DA ÁREA
# =========================================================

async def girar_15_horario():

    global angulo_atual

    motor.run(
        MOTOR_ESQUERDO,
        -280
    )

    motor.run(
        MOTOR_DIREITO,
        -280
    )

    await runloop.sleep_ms(243)

    motor.stop(MOTOR_ESQUERDO)
    motor.stop(MOTOR_DIREITO)

    await runloop.sleep_ms(100)

    angulo_atual += 15
    angulo_atual = normalizar(
        angulo_atual
    )


async def girar_15_anti_horario():

    global angulo_atual

    motor.run(
        MOTOR_ESQUERDO,
        280
    )

    motor.run(
        MOTOR_DIREITO,
        280
    )

    await runloop.sleep_ms(243)

    motor.stop(MOTOR_ESQUERDO)
    motor.stop(MOTOR_DIREITO)

    await runloop.sleep_ms(100)

    angulo_atual -= 15
    angulo_atual = normalizar(
        angulo_atual
    )


async def girar_10_horario():

    global angulo_atual

    motor.run(
        MOTOR_ESQUERDO,
        -280
    )

    motor.run(
        MOTOR_DIREITO,
        -280
    )

    await runloop.sleep_ms(162)

    motor.stop(MOTOR_ESQUERDO)
    motor.stop(MOTOR_DIREITO)

    await runloop.sleep_ms(100)

    angulo_atual += 10
    angulo_atual = normalizar(
        angulo_atual
    )


async def girar_10_anti_horario():

    global angulo_atual

    motor.run(
        MOTOR_ESQUERDO,
        280
    )

    motor.run(
        MOTOR_DIREITO,
        280
    )

    await runloop.sleep_ms(162)

    motor.stop(MOTOR_ESQUERDO)
    motor.stop(MOTOR_DIREITO)

    await runloop.sleep_ms(100)

    angulo_atual -= 10
    angulo_atual = normalizar(
        angulo_atual
    )


async def girar_2_horario():

    global angulo_atual

    motor.run(
        MOTOR_ESQUERDO,
        -280
    )

    motor.run(
        MOTOR_DIREITO,
        -280
    )

    await runloop.sleep_ms(32)

    motor.stop(MOTOR_ESQUERDO)
    motor.stop(MOTOR_DIREITO)

    await runloop.sleep_ms(100)

    angulo_atual += 2
    angulo_atual = normalizar(
        angulo_atual
    )


async def girar_2_anti_horario():

    global angulo_atual

    motor.run(
        MOTOR_ESQUERDO,
        280
    )

    motor.run(
        MOTOR_DIREITO,
        280
    )

    await runloop.sleep_ms(32)

    motor.stop(MOTOR_ESQUERDO)
    motor.stop(MOTOR_DIREITO)

    await runloop.sleep_ms(100)

    angulo_atual -= 2
    angulo_atual = normalizar(
        angulo_atual
    )


# =========================================================
# GIRO PARA ÂNGULO GLOBAL
# =========================================================

async def girar_para_angulo_global(alvo):

    global angulo_atual

    alvo = normalizar(alvo)

    diferenca = (
        alvo - angulo_atual
    ) % 360

    if diferenca <= 180:

        while diferenca >= 15:

            await girar_15_horario()

            diferenca -= 15

        if diferenca >= 10:

            await girar_10_horario()

            diferenca -= 10

        while diferenca >= 2:

            await girar_2_horario()

            diferenca -= 2

    else:

        diferenca = 360 - diferenca

        while diferenca >= 15:

            await girar_15_anti_horario()

            diferenca -= 15

        if diferenca >= 10:

            await girar_10_anti_horario()

            diferenca -= 10

        while diferenca >= 2:

            await girar_2_anti_horario()

            diferenca -= 2

    angulo_atual = alvo


# =========================================================
# PROCURAR PRIMEIRA ABERTURA
# =========================================================

async def procurar_primeira_abertura():

    global angulo_atual

    print("")
    print("################################")
    print("#    PROCURANDO SAIDA        #")
    print("################################")

    angulo_atual = 0

    for passo in range(24):

        distancia = medir()

        print("")
        print(
            "ANGULO:",
            angulo_atual,
            "| DISTANCIA:",
            distancia,
            "MM"
        )

        if distancia == 9999:

            if eh_entrada(angulo_atual):

                print(
                    "ABERTURA DA ENTRADA - IGNORANDO"
                )

            else:

                print(
                    "SAIDA DETECTADA"
                )

                confirmacoes = 0

                for i in range(3):

                    teste = medir()

                    print(
                        "CONFIRMACAO",
                        i + 1,
                        ":",
                        teste
                    )

                    if teste == 9999:
                        confirmacoes += 1

                    await runloop.sleep_ms(50)

                if confirmacoes >= 2:

                    await parar()

                    await runloop.sleep_ms(300)

                    print("")
                    print("################################")
                    print("#    SAIDA ESCOLHIDA    #")
                    print("################################")

                    print(
                        "ANGULO:",
                        angulo_atual
                    )

                    return angulo_atual

        await girar_15_horario()

    print("")
    print("==============================")
    print("NENHUMA SAIDA ENCONTRADA")
    print("==============================")

    return None


# =========================================================
# CENTRALIZAR NA SAÍDA
# =========================================================

async def centralizar_na_saida():

    global angulo_atual

    angulo_abertura = angulo_atual

    print("")
    print("================================")
    print("CENTRALIZANDO NA ABERTURA")
    print("================================")

    # -----------------------------------------------------
    # PROCURA PAREDE DIREITA
    # -----------------------------------------------------

    angulo_parede_direita = None

    for i in range(24):

        distancia = medir()

        print(
            "DIREITA | ANGULO:",
            angulo_atual,
            "| DISTANCIA:",
            distancia
        )

        if distancia != 9999 and distancia > 0:

            angulo_parede_direita = angulo_atual

            break

        await girar_15_horario()

    if angulo_parede_direita is None:

        await girar_para_angulo_global(
            angulo_abertura
        )

        return False

    await girar_para_angulo_global(
        angulo_abertura
    )

    # -----------------------------------------------------
    # PROCURA PAREDE ESQUERDA
    # -----------------------------------------------------

    angulo_parede_esquerda = None

    for i in range(24):

        distancia = medir()

        print(
            "ESQUERDA | ANGULO:",
            angulo_atual,
            "| DISTANCIA:",
            distancia
        )

        if distancia != 9999 and distancia > 0:

            angulo_parede_esquerda = angulo_atual

            break

        await girar_15_anti_horario()

    if angulo_parede_esquerda is None:

        await girar_para_angulo_global(
            angulo_abertura
        )

        return False

    # -----------------------------------------------------
    # CALCULA CENTRO DA ABERTURA
    # -----------------------------------------------------

    deslocamento_direita = (
        angulo_parede_direita
        - angulo_abertura
    ) % 360

    deslocamento_esquerda = (
        angulo_parede_esquerda
        - angulo_abertura
    ) % 360

    if deslocamento_direita > 180:

        deslocamento_direita -= 360

    if deslocamento_esquerda > 180:

        deslocamento_esquerda -= 360

    angulo_meio = (
        angulo_abertura
        +
        (
            deslocamento_direita
            +
            deslocamento_esquerda
        ) / 2
    )

    angulo_meio = normalizar(
        angulo_meio
    )

    print("")
    print("================================")
    print("CENTRO DA ABERTURA")
    print("================================")

    print(
        "PAREDE ESQUERDA:",
        angulo_parede_esquerda
    )

    print(
        "ABERTURA:",
        angulo_abertura
    )

    print(
        "PAREDE DIREITA:",
        angulo_parede_direita
    )

    print(
        "ANGULO DO MEIO:",
        angulo_meio
    )

    await girar_para_angulo_global(
        angulo_meio
    )

    await runloop.sleep_ms(300)

    return True


# =========================================================
# ANDAR 1 CM
# =========================================================

async def andar_1cm_saida():

    motor.run(
        MOTOR_ESQUERDO,
        -280
    )

    motor.run(
        MOTOR_DIREITO,
        280
    )

    await runloop.sleep_ms(
        TEMPO_1CM_SAIDA
    )

    motor.stop(MOTOR_ESQUERDO)
    motor.stop(MOTOR_DIREITO)


# =========================================================
# ANDAR 2 CM
# =========================================================

async def andar_2cm_busca():

    motor.run(
        MOTOR_ESQUERDO,
        -280
    )

    motor.run(
        MOTOR_DIREITO,
        280
    )

    await runloop.sleep_ms(
        TEMPO_2CM_BUSCA
    )

    motor.stop(MOTOR_ESQUERDO)
    motor.stop(MOTOR_DIREITO)

    await runloop.sleep_ms(250)


# =========================================================
# IR PARA SAÍDA
#
# IMPORTANTE:
# NÃO EXISTE MAIS CHECAGEM DE OBSTÁCULO AQUI.
#
# ELE APENAS:
#-> ANDA 1 CM
#-> VERIFICA PRETO
#-> ANDA 1 CM
#-> VERIFICA PRETO
#-> ...
# =========================================================

async def ir_para_saida():

    print("")
    print("==============================")
    print("        INDO PARA SAIDA")
    print("==============================")

    for passo in range(MAX_PASSOS_SAIDA):

        reflexao_f = color_sensor.reflection(
            SENSOR_F
        )

        reflexao_b = color_sensor.reflection(
            SENSOR_B
        )

        preto_f = sensor_preto(
            SENSOR_F
        )

        preto_b = sensor_preto(
            SENSOR_B
        )

        print("")
        print(
            "PASSO:",
            passo + 1
        )

        print(
            "F:",
            reflexao_f,
            "| B:",
            reflexao_b
        )

        # -------------------------------------------------
        # SAIU DA SALA
        # -------------------------------------------------

        if preto_f or preto_b:

            await parar()

            print("")
            print("################################")
            print("#        SAIU DA SALA!        #")
            print("################################")

            sound.beep(
                1000,
                500,
                100
            )

            return True

        # -------------------------------------------------
        # SEM ULTRASSOM
        # SEM DESVIO
        # APENAS ANDA
        # -------------------------------------------------

        await andar_1cm_saida()

        # -------------------------------------------------
        # VERIFICA PRETO NOVAMENTE
        # -------------------------------------------------

        if saiu_da_area():

            await parar()

            print("")
            print("################################")
            print("#        SAIU DA SALA!        #")
            print("################################")

            sound.beep(
                1000,
                500,
                100
            )

            return True

    # -----------------------------------------------------
    # LIMITE DE SEGURANÇA
    # -----------------------------------------------------

    await parar()

    print("")
    print("==============================")
    print("LIMITE DE PASSOS ATINGIDO")
    print("==============================")

    return False


# =========================================================
# SAIR DA SALA
# =========================================================

async def sair_da_sala():

    global angulo_atual

    tentativa = 0

    print("")
    print("################################")
    print("#    INICIANDO SAIDA        #")
    print("################################")

    while True:

        tentativa += 1

        print("")
        print("================================")
        print(
            "BUSCA DE SAIDA:",
            tentativa
        )
        print("================================")

        # -------------------------------------------------
        # VOLTA PARA 0°
        # -------------------------------------------------

        await girar_para_angulo_global(0)

        # -------------------------------------------------
        # PROCURA ABERTURA
        # -------------------------------------------------

        abertura = (
            await procurar_primeira_abertura()
        )

        # -------------------------------------------------
        # ACHOU SAÍDA
        # -------------------------------------------------

        if abertura is not None:

            print("")
            print("================================")
            print("SAIDA ENCONTRADA")
            print("================================")

            print(
                "ANGULO:",
                abertura
            )

            await girar_para_angulo_global(
                abertura
            )

            # -------------------------------------------------
            # CENTRALIZA
            # -------------------------------------------------

            centralizado = (
                await centralizar_na_saida()
            )

            if not centralizado:

                print(
                    "NAO FOI POSSIVEL CENTRALIZAR"
                )

                continue

            # -------------------------------------------------
            # AGORA SIM:
            # SÓ VAI PARA A SAÍDA
            # -------------------------------------------------

            saiu = await ir_para_saida()

            if saiu:
                return True

            print("")
            print("==============================")
            print("NAO SAIU")
            print("NOVA BUSCA")
            print("==============================")

            continue

        # -------------------------------------------------
        # NÃO ACHOU SAÍDA
        # -------------------------------------------------

        print("")
        print("================================")
        print("SAIDA NAO ENCONTRADA")
        print("MOVENDO PARA NOVA POSICAO")
        print("================================")

        # 90° anti-horário

        for _ in range(6):

            await girar_15_anti_horario()

        # Anda 2 cm

        await andar_2cm_busca()

        # 90° horário

        for _ in range(6):

            await girar_15_horario()

        angulo_atual = 0

        await runloop.sleep_ms(300)


# =========================================================
# ESCANEAR 330°
# =========================================================

async def escanear_360_e_procurar_parede():

    global angulo_atual

    angulo_atual = 0

    print("")
    print("################################")
    print("#GIRO DE 330 GRAUS        #")
    print("#VERIFICANDO SALA            #")
    print("################################")

    encontrou_parede = False

    menor_distancia = 9999

    angulo_parede = 0

    for passo in range(22):

        distancia = medir()

        print(
            "ANGULO:",
            angulo_atual,
            "| DISTANCIA:",
            distancia,
            "MM"
        )

        if (
            distancia
            <= DISTANCIA_LIMITE_PAREDE_RESGATE
        ):

            encontrou_parede = True

            if distancia < menor_distancia:

                menor_distancia = distancia

                angulo_parede = angulo_atual

        await girar_15_horario()

    if encontrou_parede:

        print("")
        print("==============================")
        print("SALA DE RESGATE CONFIRMADA")
        print("==============================")

        return True, angulo_parede

    print("")
    print("==============================")
    print("NAO E SALA DE RESGATE")
    print("==============================")

    return False, None


# =========================================================
# RECUAR ATÉ DISTÂNCIA DA PAREDE
# =========================================================

async def recuar_ate_distancia_parede(
    alvo_mm
):

    print("")
    print("==============================")
    print(
        "RECUANDO ATE",
        alvo_mm,
        "MM"
    )
    print("==============================")

    while True:

        distancia = medir()

        print(
            "DISTANCIA:",
            distancia,
            "MM"
        )

        if distancia >= alvo_mm:

            await parar()

            await runloop.sleep_ms(200)

            break

        motor.run(
            MOTOR_ESQUERDO,
            VELOCIDADE_RE_ENTRADA_RESGATE
        )

        motor.run(
            MOTOR_DIREITO,
            -VELOCIDADE_RE_ENTRADA_RESGATE
        )

        await runloop.sleep_ms(100)

        motor.stop(
            MOTOR_ESQUERDO
        )

        motor.stop(
            MOTOR_DIREITO
        )

        await runloop.sleep_ms(50)


# =========================================================
# ENTRAR NA ÁREA DE RESGATE
#
# NÃO PEGA BOLAS.
# CONFIRMA A SALA E PROCURA A SAÍDA.
# =========================================================

async def entrar_na_area_de_resgate():

    global angulo_atual

    await parar()

    await runloop.sleep_ms(100)

    # -----------------------------------------------------
    # CORREÇÃO DE 5°
    # -----------------------------------------------------

    print("")
    print("CORRIGINDO 5 GRAUS PARA ESQUERDA")

    motor.run(
        MOTOR_ESQUERDO,
        280
    )

    motor.run(
        MOTOR_DIREITO,
        280
    )

    await runloop.sleep_ms(81)

    motor.stop(
        MOTOR_ESQUERDO
    )

    motor.stop(
        MOTOR_DIREITO
    )

    angulo_atual -= 5

    angulo_atual = normalizar(
        angulo_atual
    )

    # -----------------------------------------------------
    # CONFIRMA SALA
    # -----------------------------------------------------

    eh_sala, angulo_parede = (
        await escanear_360_e_procurar_parede()
    )

    # -----------------------------------------------------
    # NÃO É SALA
    # -----------------------------------------------------

    if not eh_sala:

        await girar_para_angulo_global(0)

        angulo_atual = 0

        await desviar_obstaculo()

        return

    # -----------------------------------------------------
    # É SALA
    # -----------------------------------------------------

    await girar_para_angulo_global(
        angulo_parede
    )

    await recuar_ate_distancia_parede(
        DISTANCIA_RE_ENTRADA_RESGATE
    )

    angulo_atual = 0

    await runloop.sleep_ms(300)

    print("")
    print("================================")
    print("ENTROU NA SALA DE RESGATE")
    print("SEM COLETA DE BOLAS")
    print("INICIANDO SAIDA")
    print("================================")

    # -----------------------------------------------------
    # DIRETO PARA A SAÍDA
    # -----------------------------------------------------

    await sair_da_sala()

    await parar()

    await runloop.sleep_ms(200)


# =========================================================
# DETECÇÃO DA ENTRADA DA SALA
# =========================================================

def detectou_entrada_resgate():

    distancia = distance_sensor.distance(
        ULTRASSOM
    )

    if distancia == -1:
        return False

    return (
        distancia
        <= DISTANCIA_ENTRADA_RESGATE
    )


# =========================================================
# MAIN
# =========================================================

async def main():

    bloqueio_verde_ate = 0

    ultimo_preto_visto = 0

    while True:

        # -------------------------------------------------
        # MEMORIZA PRETO
        # -------------------------------------------------

        if detectou_algum_preto():

            ultimo_preto_visto = (
                utime.ticks_ms()
            )

        # -------------------------------------------------
        # VERMELHO
        # -------------------------------------------------

        if detectou_vermelho():

            await parar()

            await runloop.sleep_ms(10)

            continue

        # -------------------------------------------------
        # ENTRADA DA SALA
        # -------------------------------------------------

        if detectou_entrada_resgate():

            await runloop.sleep_ms(
                TEMPO_CONFIRMA_ENTRADA_RESGATE
            )

            if detectou_entrada_resgate():

                await entrar_na_area_de_resgate()

                bloqueio_verde_ate = (
                    utime.ticks_ms()
                    +
                    BLOQUEIO_VERDE_APOS_PRETO
                )

                ultimo_preto_visto = (
                    utime.ticks_ms()
                )

            await runloop.sleep_ms(10)

            continue

        # -------------------------------------------------
        # OBSTÁCULO NORMAL DA PISTA
        # -------------------------------------------------

        if detectou_obstaculo():

            await runloop.sleep_ms(
                TEMPO_CONFIRMA_OBSTACULO
            )

            if detectou_obstaculo():

                await desviar_obstaculo()

            await runloop.sleep_ms(10)

            continue

        # -------------------------------------------------
        # DOIS PRETOS
        # -------------------------------------------------

        if detectou_dois_pretos():

            await runloop.sleep_ms(50)

            if detectou_dois_pretos():

                await dois_pretos()

                bloqueio_verde_ate = (
                    utime.ticks_ms()
                    +
                    BLOQUEIO_VERDE_APOS_PRETO
                )

            await runloop.sleep_ms(10)

            continue

        # -------------------------------------------------
        # VERDE
        # -------------------------------------------------

        agora = utime.ticks_ms()

        verde_bloqueado = (
            utime.ticks_diff(
                bloqueio_verde_ate,
                agora
            ) > 0
        )

        preto_recente = (
            utime.ticks_diff(
                agora,
                ultimo_preto_visto
            )
            <
            JANELA_IGNORAR_VERDE_APOS_PRETO
        )

        if (
            not verde_bloqueado
            and
            not preto_recente
        ):

            verde = tipo_verde()

            if verde != "NENHUM":

                verde_confirmado = (
                    await confirmar_verde()
                )

                if verde_confirmado == "DIREITA":

                    await parar()

                    await runloop.sleep_ms(100)

                    await virar_direita()

                    await runloop.sleep_ms(150)

                    continue

                elif verde_confirmado == "ESQUERDA":

                    await parar()

                    await runloop.sleep_ms(100)

                    await virar_esquerda()

                    await runloop.sleep_ms(150)

                    continue

                elif verde_confirmado == "DOIS":

                    await parar()

                    await runloop.sleep_ms(150)

                    await fazer_180()

                    await runloop.sleep_ms(150)

                    continue

        # -------------------------------------------------
        # SEGUE LINHA
        # -------------------------------------------------

        seguir_linha()

        await runloop.sleep_ms(10)


# =========================================================
# INÍCIO
# =========================================================

runloop.run(main())


