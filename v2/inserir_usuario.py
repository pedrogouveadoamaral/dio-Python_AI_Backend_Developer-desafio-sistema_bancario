def seleciona_usuario():
    """Função principal para selecionar um usuário e sua conta."""

    def validar_input(mensagem):
        """Valida a entrada do usuário para garantir que não seja vazia.

        Args:
            mensagem (str): A mensagem a ser exibida ao usuário.

        Returns:
            str: O valor fornecido pelo usuário.
        """
        while True:
            valor = input(mensagem).strip()  # Remove espaços em branco do início e do fim
            if valor:  # Verifica se o valor não está vazio
                return valor
            else:
                print('Por favor, forneça um valor válido.')

    def procurar_usuario(usuarios, cpf):
        """Procura um usuário na lista de usuários com base no CPF.

        Args:
            usuarios (list): Lista de usuários.
            cpf (str): CPF do usuário a ser procurado.

        Returns:
            tuple: Índice do usuário na lista (se encontrado) e o nome completo do usuário.
        """
        nome_usuario = ''
        procura = next((i for i, sublist in enumerate(usuarios) if cpf in sublist), None)
        if procura is not None:
            nome_usuario = f'{usuarios[procura][0]} {usuarios[procura][1]}'
        return procura, nome_usuario

    def cadastrar_usuario(cpf):
        """Cadastra um novo usuário.

        Args:
            cpf (str): CPF do usuário.

        Returns:
            list: Informações do usuário.
        """
        nome_completo = validar_input('Nome Completo: ')
        dtnascimento = validar_input('Data de nascimento: ')
        endereco = validar_input('Endereço: ')
        usuario = [nome_completo, dtnascimento, cpf, endereco]
        return usuario

    def tab_usuarios(novo_usuario, usuarios):
        """Adiciona um novo usuário à lista de usuários.

        Args:
            novo_usuario (list): Informações do novo usuário.
            usuarios (list): Lista de usuários.

        Returns:
            list: Lista atualizada de usuários.
        """
        usuarios.append(novo_usuario)
        print(f'Usuário cadastrado com sucesso.')
        return usuarios

    def cadastrar_conta(cpf, nrconta):
        """Cadastra uma nova conta para o usuário.

        Args:
            cpf (str): CPF do usuário.
            nrconta (int): Número da conta.

        Returns:
            str: Número da nova conta.
        """
        AGENCIA = '0001'
        nrconta_str = f'0{nrconta}' if nrconta < 10 else str(nrconta)
        nova_conta = f'{AGENCIA}{nrconta_str}{cpf}'
        return nova_conta

    def tab_contas(contas, cpf, nova_conta):
        """Adiciona uma nova conta à lista de contas.

        Args:
            contas (list): Lista de contas.
            cpf (str): CPF do usuário.
            nova_conta (str): Número da nova conta.

        Returns:
            list: Lista atualizada de contas.
        """
        contas.append(nova_conta)
        print(f'Conta {nova_conta} cadastrada e vinculada ao CPF {cpf} com sucesso.')
        return contas

    def validar_cpf():
        """Valida o CPF inserido pelo usuário."""
        while True:
            cpf = input('Informe seu CPF: (Somente os números): ').translate(str.maketrans('', '', '.- '))
            validacao = cpf.isalnum() and len(cpf) == 11
            if validacao:
                return cpf, True
            else:
                print('CPF inválido. Informe novamente.')

    def cadastrar_outra_conta():
        """Verifica se o usuário deseja cadastrar outra conta."""
        resposta = input('Deseja cadastrar mais uma conta? (S/N): ').strip().upper()
        return resposta in ['S', 's', 'Sim', 'sim']

    def filtrar_contas(cpf, contas):
        """Filtra as contas para encontrar apenas aquelas vinculadas ao CPF informado."""
        return [conta for conta in contas if cpf in conta]

    def selecionar_conta(contas, cpf):
        """Permite ao usuário selecionar uma conta entre as disponíveis.

        Args:
            contas (list): Lista de contas disponíveis.
            cpf (str): CPF do usuário.

        Returns:
            str: Conta selecionada pelo usuário.
        """
        contas_filtradas = filtrar_contas(cpf, contas)
        print('Selecione a conta desejada:')
        for i, conta in enumerate(contas_filtradas, start=1):
            print(f'{i}. {conta}')
        while True:
            escolha = input('Digite o número da conta: ')
            if escolha.isdigit() and 1 <= int(escolha) <= len(contas_filtradas):
                return contas_filtradas[int(escolha) - 1]
            else:
                print('Escolha inválida. Digite o número correspondente à conta.')

    def fluxo_usuario():
        """Executa o fluxo principal para o usuário."""
        usuarios = []  # Lista de usuários
        contas = []  # Lista de contas

        cpf, validacao_cpf = validar_cpf()  # Validação do CPF
        while True:
            if validacao_cpf:
                procura_usuario = procurar_usuario(usuarios, cpf)
                if procura_usuario[0] is not None:  # Se o usuário já estiver cadastrado
                    print(f'Olá, {procura_usuario[1]}. Seja bem-vindo(a).')
                    contas_filtradas = filtrar_contas(cpf, contas)
                    if len(contas_filtradas) >= 1:
                        print(f'Você possui a(s) seguinte(s) conta(s):')
                        for conta in contas_filtradas:
                            print(conta)
                    else:
                        print('Não foram encontradas contas vinculadas ao seu CPF.\n'
                              'Mas não se preocupe, iremos cadastrar sua primeira conta a seguir.')
                        nova_conta = cadastrar_conta(cpf, len(contas) + 1)
                        tab_contas(contas, cpf, nova_conta)
                    if cadastrar_outra_conta():
                        nova_conta = cadastrar_conta(cpf, len(contas) + 1)
                        tab_contas(contas, cpf, nova_conta)
                    else:  # Chama a função filtrar_contas novamente para retornar a conta encontrada para o usuário
                        contas_filtradas = filtrar_contas(cpf, contas)
                        if len(contas_filtradas) == 1:  # Se for encontrada só uma conta, a retorna e encerra o loop
                            return {'cpf_usuario': cpf, 'conta': contas_filtradas[0]}
                            break
                        else:
                            pass
                    if len(contas) >= 1:
                        conta_escolhida = selecionar_conta(contas, cpf)
                        print(f'Você selecionou a conta {conta_escolhida}')
                        return {'cpf_usuario': cpf, 'conta': conta_escolhida}
                        break
                else:  # Se o usuário não estiver cadastrado
                    print('Usuário não cadastrado. Informe seus dados para criar um novo usuário e conta.')
                    novo_usuario = cadastrar_usuario(cpf)
                    tab_usuarios(novo_usuario, usuarios)
                    nova_conta = cadastrar_conta(cpf, len(contas) + 1)
                    tab_contas(contas, cpf, nova_conta)

    return fluxo_usuario()
