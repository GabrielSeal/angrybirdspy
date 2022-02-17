import console
from jogo import *
from menu import *

dificuldade = 2

while True:
    opcao = 0
    while (opcao != 1 and opcao != 2 and opcao != 3):
        console.clear()
        exibirMenu()
        try:
            opcao = int(input())
        except:
            opcao = 0

    if (opcao == 1):
        console.clear()
        jogar(dificuldade)
    elif (opcao == 2):
        #Configuração
        console.clear()
        print("Configuracoes do JOGO:")
        dificuldade = int(input("- Dificuldade:\n[1] - Fácil\n[2] - Médio\n[3] - Difícil\n"))
        console.pause()
        console.clear()
        print("Carregando", end ='')
        for c in range (3):   
            sleep(0.8)
            print(".", end='', flush = True)
        sleep(0.8)
        print("\nJogo configurado!\n")
        sleep(0.8)
        console.pause()
    elif (opcao == 3):
        console.clear()
        sleep(0.8)
        print("\nAté a próxima!")
        exit(0)
    else:
        exibirMenu()