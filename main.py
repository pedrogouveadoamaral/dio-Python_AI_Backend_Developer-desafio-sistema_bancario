# Importações
from datetime import datetime

def operacoes():
    # Constantes
    LIMITE_QTDE_DIA_SAQUE = 3
    LIMITE_VR_SAQUE = 500

    # Variáveis
    depositos = {}  # Dicionário para armazenar os valores de depósitos
    c_dep = 0  # Variável para contar a quantidade de depósitos realizados durante a execução atutal do programa
    saques = {}  # Dicionário para armazenar os valores de saques
    c_saq = 0  # Variável para contar a quantidade de saques realizados durante a execução atutal do programa
    movimentacoes = {}  # Dicionário para armazenar todas as movimentações. Para ser utilizado no extrato
    data = datetime.now().strftime(
        "%d%m%Y")  # Variável para armazenar a data do dia em que o programa está sendo executado

    # Menu do usuário
    menu = '''
        [1] - Saldo
        [2] - Depósito
        [3] - Saque
        [4] - Extrato
        [5] - Encerrar
        =>
    '''

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
                while True: # Validação para verificar se o valor informado de depósito é, ou pode ser um float
                    entrada_deposito = input('Informe o valor do depósito: ').replace(',', '.')
                    try:
                        deposito_atual = float(entrada_deposito)
                        if deposito_atual <= 0:
                            print('O valor do depósito deve ser maior que zero.')
                            continue
                        depositos.update({f'deposito_{c_dep + 1}_{data}': deposito_atual})
                        print(f'Seu depósito no valor de R$ {deposito_atual:.2f} '
                              f'foi realizado com sucesso!')
                        print(f'Seu saldo atual é de R$ {saldo + deposito_atual}')
                        movimentacoes.update({f'{c_dep}Depósito de R$': deposito_atual})
                        c_dep += 1
                        break
                    except ValueError:
                        print('Valor inválido! Informe um valor correto.')
                break
            if operacao == '3':
                while True:
                    if saldo == 0.00:
                        print(f'Não é possível realizar saques no momento. Seu saldo é de R$ 0.00.')
                        break

                    elif c_saq >= LIMITE_QTDE_DIA_SAQUE:
                        print('O limite de quantidades de saques diários foi atingido. Por favor, retorne amanhã.')
                        break

                    else:
                        print(f'Seu saldo atual é de R$ {saldo:.2f}')
                        entrada_saque = input('Informe o valor que deseja sacar:')

                        try: # Verifica se o valor inserido pelo usuário é um float ou int válido
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
                                print(f'Seu sa'
                                      f'que no valor de R$ {saque_atual:.2f} foi realizado com sucesso!')
                                print(f'Seu saldo atual é de R$ {saldo - saque_atual}')
                                movimentacoes.update({f'{c_saq}Saque de R$': saque_atual})
                                c_saq += 1
                                break

                        except ValueError:
                            print('Valor inválido! Informe um valor correto.')
                break

            if operacao == '4':
                print(f'Extrato:')
                for key, value in movimentacoes.items():
                    print(f'{key[1:]} {value}')
                print(f'Total de Depósitos: {total_depositos}\n'
                      f'Total de Saques: {total_saques}\n'
                      f'Saldo Final: {saldo}')
                break

        else:
            print('Você escolheu uma operação inválida. Por favor selecione a opção correta no menu.')

if __name__ == "__main__":
    print("Iniciando o sistema bancário.")
    operacoes()
