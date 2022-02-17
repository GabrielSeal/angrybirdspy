from console import *
from time import sleep
from random import randrange
from jogoConst import *

def jogar(dificuldade):
    #Nome do jogador e Instruções sobre o jogo.
    print("\033[33mDigite o nome do jogador: \033[m")
    nomeJogador = str(input())
    pause()
    sleep(0.8)
    
    print("""\033[33m \nCOMANDOS:

    APERTE "W" PARA O CANHÃO SUBIR.

    APERTE "S" PARA O CANHÃO DESCER.

    APERTE A BARRA DE ESPAÇO PARA ATIRAR.\033[31m
    
    REGRAS:

    SE OS 4 ALVOS CONSECUTIVOS DA RODADA CHEGAREM AO CANHÃO, VOCÊ PERDE VIDA

    ACERTE UM PARA INTERROMPER A SEQUÊNCIA E GANHAR PONTOS

    AO CHEGAR EM 1000 PONTOS, VOCÊ GANHA

    A DIFICULDADE DIMINUI SUAS VIDAS E AUMENTA A VELOCIDADE DOS ALVOS

    
    BOA SORTE!!!\n\033[m""")

    pause()
    #Print da tela do jogo
    init(LIMITE_VERT)
    gotoxy(0, 1)
    print('\033[33m-\033[m' * LIMITE, end='', flush=True)
    reset(0, 1, LIMITE_VERT, LIMITE)
    print('\033[34m*\033[m' * LIMITE, end='', flush=True)
    gotoxy(0, LIMITE_VERT - 4)
    print('\033[33m-\033[m' * LIMITE, end='', flush=True)
    gotoxy((LIMITE / 2) - 2, 0)
    print("\033[33mPontos: 0", end='')
    gotoxy((LIMITE / 2) - 5, LIMITE_VERT - 3)
    print("\033[32mVidas:\033[m", end='')
    input()
    gotoxy(0,0)
    #Lista das balas
    balas = [ {"x":0, "y":0, "ativa": False, "traj": {"A":0, "B": 0,"C":0}},
              {"x":0, "y":0, "ativa": False, "traj": {"A":0, "B": 0,"C":0}},
              {"x":0, "y":0, "ativa": False, "traj": {"A":0, "B": 0,"C":0}} ]
    #Lista dos alvos
    discos = [ { "img":'\033[31m[]\033[m', "x":0, "y":0, "ativo": False, "traj": {"A":0, "B": 0, "C": 0} },
               { "img":'\033[31m[]\033[m', "x":0, "y":0, "ativo": False, "traj": {"A":0, "B": 0, "C": 0} },
               { "img":'\033[31m[]\033[m', "x":0, "y":0, "ativo": False, "traj": {"A":0, "B": 0, "C": 0} },
               { "img":'\033[31m[]\033[m', "x":0, "y":0, "ativo": False, "traj": {"A":0, "B": 0, "C": 0} } ]
    #Variáveis
    yCanhao = 15
    pontuacaoJogador = 0.0
    numeroVidasJogador = 6 / dificuldade
    intervalo = 5   # Intervalo de (ciclos de espera para) lançamento de disco

    while True:
        # Invoca alvo em intervalos.
        if (randrange(15) % len(discos) == 0 and intervalo < 0):
            intervalo = len(discos) + randrange(10)
            j = 0
            for disco in discos:
                if (not disco["ativo"]):
                    disco["ativo"] = True
                    disco["x"] = LIMITE
                    disco["y"] = LIMITE_VERT - 5
                    disco["traj"]["C"] = disco["y"]
                    disco["traj"]["A"] = (max(-15, 4 - disco["traj"]["C"])) / ((LIMITE/2) * (LIMITE/2 - LIMITE)) # 2 = y min
                    disco["traj"]["B"] = - disco["traj"]["A"] * LIMITE
                    break
                j += 1

        # apaga, move e desenha discos
        j = 0
        for disco in discos:
            # Apaga o disco
            gotoxy(disco["x"], disco["y"])
            print("  ", end='')
        
            if disco["ativo"]:
                
                # Muda a posição do alvo
                
                disco["x"] -= 0.5 * dificuldade   # Alvo se move para direita (aumenta x)

                #Cancela o alvo caso colida com a parede da esquerda
                if disco["x"] <= 2:
                    disco["ativo"] = False
                else:
                    gotoxy(disco["x"], disco["y"])
                    print(disco["img"], end='')
            else:
                # Limpa exibição da trajetória
                print(' ' * 30, end='')

            j += 1

        # COMANDOS DO USUÁRIO
        if (kbhit()):
            c = hitKey()
            gotoxy((LIMITE / 2) - 25, LIMITE_VERT - 3)
            print(ord(c), (ord(c) == ord(' ')), end='', flush=True)
            
            # Atirar bala
            if (ord(c) == ord(' ')): # tecla de espaço em branco usada para disparar
                for bala in balas:
                    if (not bala["ativa"]):
                        bala["ativa"] = True
                        bala["x"] = 3
                        bala["y"] = yCanhao
                        bala["traj"]["C"] = bala["y"]
                        bala["traj"]["A"] = 0
                        bala["traj"]["B"] = 1
                        break
             #Movimenta canhão
            elif (ord(c) == ord("w") or ord(c) == ord("W")):
                if (yCanhao <=5):
                    gotoxy(1, yCanhao)
                    print("\033[36m=[\033[m")
                else:
                    gotoxy(1, yCanhao)
                    print('  ')
                    yCanhao -= 1

            elif (ord(c) == ord("s") or ord(c) == ord("S")):
                if (yCanhao >=24):
                    gotoxy(1, yCanhao)
                    print("\033[36m=[\033[m")
                else:
                    gotoxy(1, yCanhao)
                    print('  ')
                    yCanhao +=1

        # apaga, move e desenha balas
        for bala in balas:
            if (bala["ativa"]):
                gotoxy(bala["x"], bala["y"])
                print(' ', end='')


                #Simula parábola
                bala["x"] += 2
                if (bala["x"] <= 20):
                    bala["y"] -= bala["traj"]["B"]/2  # FAZER bala["y"] = solve1(bala["traj"], bala["x"])
                else:
                    bala["y"] += bala["traj"]["B"]

                if (bala["y"] >= 26 or bala["y"] <= 0):
                    bala["ativa"] = False
                else:
                    gotoxy(bala["x"], bala["y"])
                    print('\033[37mo\033[m',end='')
            #Limpa trajetória:
            else:
                print(' ' * 30, end='')


        #Desenha canhao
            gotoxy(1, yCanhao)
            print("\033[36m=[\033[m")     
    
        #Colisão de acerto
        acertou = 0
        for bala in balas:
            for disco in discos:
                if (bala["ativa"] and disco["ativo"]
                        and (bala["x"] == disco["x"]  or bala["x"] == disco["x"] + 1 or bala["x"] == disco["x"] - 1
                        or bala["x"] == disco["x"] + 0.5 or bala["x"] == disco["x"] - 0.5)
                        and bala["y"] == disco["y"]):
                    acertou = True
                    gotoxy(bala["x"], bala["y"])
                    print(' ')
                    gotoxy(disco["x"], disco["y"])
                    print(' ')
                    disco["ativo"] = False
                    bala["ativa"] = False
                    break
        #Aumento da pontuação
        if (acertou):
            pontuacaoJogador += PONTOS_ACERTO
            gotoxy(LIMITE/2 + 6,0)
            print("%0.2f" % pontuacaoJogador, end='')
        #Redução da vida
        if (disco["ativo"] and disco["x"] <= 3):
            numeroVidasJogador -= 1
        gotoxy((LIMITE / 2) + 2, LIMITE_VERT - 3)
        print("%.0f" % numeroVidasJogador, end='')
        #YOU WIN
        fimDoJogo = lambda : pontuacaoJogador >= 1000
        if (fimDoJogo()):
            gotoxy(35, LIMITE_VERT / 2)
            print(f"\033[32mYOU WIN, {nomeJogador}!\033[m")
            break
        #YOU LOSE 
        gameOver = lambda : numeroVidasJogador == 0
        if (gameOver()):
            gotoxy(35, LIMITE_VERT / 2)
            print(f"\033[31mGAME OVER, {nomeJogador}!\033[m")
            break
        #Redução de intervalo após cada ciclo para lançamento dos alvos.
        print(end='',flush=True)
        sleep(0.1)
        intervalo -= 1

    pause()
