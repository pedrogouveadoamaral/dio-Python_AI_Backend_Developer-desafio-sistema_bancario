from datetime import datetime
from inserir_usuario import seleciona_usuario


def operacoes():
    def iniciar_usuario():
        usuario = seleciona_usuario()
        return print(f'Vamos iniciar a movimentação de sua conta corrente nº: {usuario['conta']}')

    def func_depositos(saldo, c_dep, depositos, movimentacoes):
        # Função que solicita o valor de depósito para o cliente, processa e retorna as variáveis atualizadas
        data = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        while True:
            entrada_deposito = input('Informe o valor do depósito: ').replace(',', '.')
            try:
                deposito_atual = float(entrada_deposito)
                if deposito_atual <= 0:
                    print('O valor do depósito deve ser maior que R$ 0.00.')
                    continue
                depositos.update({f'deposito_{c_dep + 1}_{data}': deposito_atual})
                print(f'Seu depósito no valor de R$ {deposito_atual:.2f} foi realizado com sucesso!')
                print(f'Seu saldo atual é de R$ {saldo + deposito_atual:.2f}')
                movimentacoes.update({f'{data}Depósito de R$': deposito_atual})
                c_dep += 1
                return saldo, c_dep, depositos, movimentacoes
            except ValueError:
                print('Valor inválido! Informe um valor correto.')

    def func_saques(*, saldo, LIMITE_QTDE_DIA_SAQUE, LIMITE_VR_SAQUE, c_saq, saques, movimentacoes):
        # Função que solicita o valor de saque para o cliente, processa e retorna as variáveis atualizadas
        data = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        while True:
            if saldo == 0.00:
                print(f'Não é possível realizar saques no momento. Seu saldo é de R$ 0.00.')
                return saldo, c_saq, saques, movimentacoes

            elif c_saq >= LIMITE_QTDE_DIA_SAQUE:
                print(f'O limite de {LIMITE_QTDE_DIA_SAQUE} saques diários foi atingido. Por favor, retorne amanhã.')
                return saldo, c_saq, saques, movimentacoes

            else:
                print(f'Seu saldo atual é de R$ {saldo:.2f}')
                entrada_saque = input('Informe o valor que deseja sacar:').replace(',', '.')

                try:  # Verifica se o valor inserido pelo usuário é um float ou int válido
                    saque_atual = float(entrada_saque)
                    if saque_atual <= 0:
                        print(f'O valor do saque deve ser maior que R$ 0.00 e menor que R$ {LIMITE_VR_SAQUE:.2f}')

                    elif LIMITE_VR_SAQUE < saque_atual <= saldo:
                        print(f'Você ultrapassou o limite de valor por saque. Por favor, informe um valor de até: '
                              f'R$ {LIMITE_VR_SAQUE:.2f}')

                    elif saque_atual > saldo:
                        print(f'Saldo insuficiente para realizar o saque pretendido.\n'
                              f'Por favor, informe um valor até R$ {saldo:.2f}.')

                    else:
                        saques.update({f'saque_{c_saq + 1}_{data}': saque_atual})
                        print(f'Seu saque no valor de R$ {saque_atual:.2f} foi realizado com sucesso!')
                        print(f'Seu saldo atual é de R$ {saldo - saque_atual:.2f}')
                        movimentacoes.update({f'{data}Saque de R$': saque_atual})
                        c_saq += 1
                        return saldo, c_saq, saques, movimentacoes

                except ValueError:
                    print('Valor inválido! Informe um valor correto.')

    def func_extrato(saldo, saques, depositos, /, *, movimentacoes):
        # Função que processa e imprime os dados do extrato completo do cliente
        print(f'Extrato:')
        for key, value in movimentacoes.items():
            print(f'{key[19:]} {value:.2f} realizado no dia {key[:10]} e hora: {key[11:19]}.') # Add: dia e hora da mov
        print(f'Total de Depósitos: R$ {sum(depositos.values()):.2f}\n' 
              f'Total de Saques: R$ {sum(saques.values()):.2f}\n'
              f'Saldo Final: R$ {round(saldo, 2):.2f}')

    # Constantes
    LIMITE_QTDE_DIA_SAQUE = 3  # Constante que armazena o valor de quantidade limite de saques por dia
    LIMITE_VR_SAQUE = 500  # Constante que armazena o valor monetário do limite de cada saque

    # Variáveis
    depositos = {}  # Dicionário para armazenar os valores de depósitos
    c_dep = 0  # Variável para contar a quantidade de depósitos realizados durante a execução atutal do programa
    saques = {}  # Dicionário para armazenar os valores de saques
    c_saq = 0  # Variável para contar a quantidade de saques realizados durante a execução atutal do programa
    movimentacoes = {}  # Dicionário para armazenar todas as movimentações. Para ser impresso no extrato
    saldo = 0  # Variável para armazenar o saldo atual da conta do cliente durante a execução atual do programa
    # Menu do usuário
    menu = '''
    [1] - Saldo
    [2] - Depósito
    [3] - Saque
    [4] - Extrato
    [5] - Encerrar
    =>
        '''
    iniciar_usuario()  # Inicia a inserção do usuário
    while True:
        operacao = input(menu)
        total_saques = sum(saques.values())
        total_depositos = sum(depositos.values())
        saldo = total_depositos - total_saques

        if operacao == '5':
            print('Encerrando. Obrigado por usar nosso sistema bancário!')
            break

        while operacao in ['1', '2', '3', '4']:
            if operacao == '1':
                print(f'Saldo atual: R$ {saldo:.2f}')
                break

            if operacao == '2':
                saldo, c_dep, depositos, movimentacoes = func_depositos(saldo, c_dep, depositos, movimentacoes)
                break

            if operacao == '3':
                saldo, c_saq, saques, movimentacoes = func_saques(saldo=saldo, LIMITE_QTDE_DIA_SAQUE=LIMITE_QTDE_DIA_SAQUE,
                               LIMITE_VR_SAQUE=LIMITE_VR_SAQUE, c_saq=c_saq, saques=saques,
                               movimentacoes=movimentacoes)
                break

            if operacao == '4':
                func_extrato(saldo, depositos, saques, movimentacoes=movimentacoes)
                break
        else:
            print('Você escolheu uma operação inválida. Por favor, selecione a opção correta no menu.')
