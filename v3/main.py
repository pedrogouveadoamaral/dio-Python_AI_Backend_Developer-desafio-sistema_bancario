from datetime import datetime
from abc import ABC, abstractmethod


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if not self._pode_sacar(conta):
            return False
        conta.saldo -= self.valor
        conta.saques_diarios += 1
        conta.historico.adicionar_transacao(self)
        return True

    def _pode_sacar(self, conta):
        if conta.saldo < self.valor:
            return False
        if self.valor > conta.limite:
            return False
        if conta.saques_diarios >= conta.limite_saques:
            return False
        return True


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, cliente, numero, agencia='0001'):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def nova_conta(cliente, numero):
        return Conta(cliente, numero)

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_diarios = 0


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = datetime.strptime(data_nascimento, "%d-%m-%Y").date()
        self.cpf = cpf


def fluxo_usuario():
    usuarios = []

    def validar_input(mensagem):
        while True:
            valor = input(mensagem).strip()
            if valor:
                return valor
            else:
                print('Por favor, forneça um valor válido.')

    def procurar_usuario(cpf):
        for usuario in usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def validar_cpf():
        while True:
            _cpf = input('Informe seu CPF: (Somente os números): ').translate(str.maketrans('', '', '.- '))
            if _cpf.isdigit() and len(_cpf) == 11:
                return _cpf
            else:
                print('CPF inválido. Informe novamente.')

    def cadastrar_usuario(cpf):
        nome = validar_input('Informe seu nome: ')
        data_nascimento = validar_input('Informe sua data de nascimento (dd-mm-aaaa): ')
        endereco = validar_input('Informe seu endereço: ')
        novo_usuario = PessoaFisica(nome, data_nascimento, cpf, endereco)
        usuarios.append(novo_usuario)
        print(f'Usuário {nome} cadastrado com sucesso.')
        return novo_usuario

    cpf = validar_cpf()
    usuario = procurar_usuario(cpf)

    if usuario:
        print(f'Olá, {usuario.nome}. Seja bem-vindo(a).')
    else:
        print('Usuário não encontrado. Vamos cadastrar um novo usuário.')
        usuario = cadastrar_usuario(cpf)

    return usuario


def operacoes():
    usuario = fluxo_usuario()
    cpf = usuario.cpf
    def criar_nova_conta(usuario, cpf):
        numero_conta = f'{len(usuario.contas) + 1}{cpf}'
        conta = ContaCorrente(usuario, numero_conta)
        usuario.adicionar_conta(conta)
        print(f'Conta corrente nº: {conta.numero} criada com sucesso.')
        return conta

    criar_nova_conta(usuario, cpf) # Cria a primeira conta para o usuário automaticamente.
    while True:
        nova_conta = input('Deseja criar uma nova conta? (s/n): ')
        if nova_conta in ['s', 'sim', 'S', 'Sim']:
            criar_nova_conta(usuario, cpf)
        else:
            break

    print('Suas contas:')
    for idx, conta in enumerate(usuario.contas):
        print(f'Conta {idx + 1}: Agência {conta.agencia} - Número {conta.numero}')

    while True:
        if len(usuario.contas) == 1:
            break
        escolha_conta = input('Escolha o número da conta que deseja usar: ')
        if escolha_conta.isdigit() and 1 <= int(escolha_conta) <= len(usuario.contas):
            conta = usuario.contas[int(escolha_conta) - 1]
            break
        else:
            print('Escolha inválida. Por favor, selecione um número válido.')

    menu = '''
    [1] - Saldo
    [2] - Depósito
    [3] - Saque
    [4] - Extrato
    [5] - Encerrar
    =>
    '''
    print(f'Bem-vindo, {usuario.nome}! A movimentação da sua conta: Agência {conta.agencia} - Número {conta.numero} '
          f'está iniciada.\n'
          f'Por favor, escolha as opções no menu.')
    while True:
        operacao = input(menu)

        if operacao == '1':
            print(f'Saldo atual: R$ {conta.saldo:.2f}')

        elif operacao == '2':
            valor = float(input('Informe o valor do depósito: ').replace(',', '.'))
            conta.depositar(valor)
            print(f'Depósito de R$ {valor:.2f} realizado com sucesso. Saldo atual: R$ {conta.saldo:.2f}')

        elif operacao == '3':
            print(f'Saldo atual: R$ {conta.saldo:.2f}')
            if conta.saldo <= 0:
                print('Você não tem saldo para realizar saques.')
            elif conta.saques_diarios >= conta.limite_saques:
                print('Não é possível realizar mais saques! O número máximo de saques diários foi excedido.')
            else:
                valor = float(input('Informe o valor do saque: ').replace(',', '.'))
                resultado = conta.sacar(valor)
                if resultado is True:
                    print(f'Saque de R$ {valor:.2f} realizado com sucesso. Saldo atual: R$ {conta.saldo:.2f}')
                else:
                    if valor > conta.limite and valor < conta.saldo:
                        print(f'Saque não realizado. Motivo: Valor do saque excede o limite permitido.')
                    elif valor > conta.limite and valor > conta.saldo:
                        print(f'Saque não realizado. Motivo: Valor do saque excede o limite permitido e é maior '
                              f'que seu saldo atual.')
                    elif valor < conta.limite > conta.saldo:
                        print(f'Saque não realizado. Motivo: Você não tem saldo suficiente para realizar o saque.')

        elif operacao == '4':
            print('Extrato:')
            for transacao in conta.historico.transacoes:
                print(f'{transacao.__class__.__name__} de R$ {transacao.valor:.2f}')
            print(f'Saldo atual: R$ {conta.saldo:.2f}')

        elif operacao == '5':
            print('Encerrando. Obrigado por usar nosso sistema bancário!')
            break

        else:
            print('Você escolheu uma operação inválida. Por favor, selecione uma opção correta no menu.')


def main():
    operacoes()


if __name__ == "__main__":
    print("Iniciando o sistema bancário.")
    main()
