def menu():
    menu = """

    [c] Cadastrar
    [cc] Criar Conta
    [lc] Listar Contas
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    return input(menu)

def depositar(saldo, valor, extrato, /): 
    if valor > 0:
        saldo += valor
        extrato += f"Deposito de R$ {valor:.2f}\n"
        print("Deposito realizado com sucesso!!")
    else:
        print("Valor invalido insira um valor positivo!!")

    return saldo, extrato

def sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print("Saldo insuficiente!!")
    elif excedeu_limite:
        print("Limite atingido!!")
    elif excedeu_saques:
        print("Limite de saques atingido!!")
    elif valor > 0:
        saldo -= valor
        limite -= valor
        numero_saques += 1
        extrato += f"Saque de R$ {valor:.2f}\n"
        print("Saque realizado com sucesso!!")
    else:
        print("Valor invalido!!")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("Ainda Não foi efetuado nenhuma operação!!") if not extrato else extrato
    print(f"\nSaldo R$ {saldo:.2f}")

def criar_usuario(usuarios):
    cpf = input("Digite o numero do CPF do usurario(somente digitos): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(f"\nJá existe usuario com o CPF: {usuario['cpf']}")
        return

    nome = input("\nDigite o nome do usuario: ")
    data = input("\nDigite a data de nasciento do usuario(dd-mm-aaaa): ")
    endereco = input("\nDigite o endereco do usuario(logradouro, nro - bairro - cidade/sigla): ")
    
    usuarios.append({"nome": nome, "data": data, "cpf": cpf, "endereco": endereco})

    print(f"\nSeja bem-vindo {nome}")

def filtrar_usuario(cpf, usuarios):
    user_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return user_filtrado[0] if user_filtrado else None

def criar_conta(agencia, numero_da_conta, usuarios):
    cpf = input("Digite o numero do CPF do usurario(somente digitos): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_da_conta": numero_da_conta, "usuario":usuario}

    print("\nUsuario não encontrado!")
    
def listar_conta(contas):
    for conta in contas:
        dados_da_conta = f"""
            Agência: {conta['agencia']}
            C/C: {conta['numero_da_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print(dados_da_conta)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            deposito = float(input("Digite o valor do deposito R$ "))

            saldo, extrato = depositar(saldo, deposito , extrato)

        elif opcao == 's':
            saque = float(input("Digite o valor do saque R$ "))

            saldo, extrato = sacar(
                saldo=saldo, 
                valor=saque,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == 'e':
            exibir_extrato(saldo, extrato = extrato)

        elif opcao == 'c':
            criar_usuario(usuarios)

        elif opcao == 'cc':
            numero_da_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_da_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == 'lc':
            listar_conta(contas)

        elif opcao == 'q':
            break

        else:
            print("Opção invalida, por favor selecione novamente a operação desejada.")

main()
