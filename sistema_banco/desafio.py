menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == 'd':
        deposito = float(input("Digite o valor do deposito R$ "))
        saldo += deposito
        extrato += f"Deposito de R$ {deposito:.2f}\n"
        print("Deposito realizado com sucesso!!")

    elif opcao == 's':
        if numero_saques < LIMITE_SAQUES:

            saque = float(input("Digite o valor do saque R$ "))

            if saque <= limite:
                if saque <= saldo:
                    saldo -= saque
                    limite -= saque
                    numero_saques += 1
                    extrato += f"Saque de R$ {saque:.2f}\n"
                    print("Saque realizado com sucesso!!")
                else:
                    print("Saldo insuficiente!!")
            else:
                print("Limite atingido!!")
        else:
            print("Limite de saques atingido!!")

    elif opcao == 'e':
        print(f"{extrato}\n\nSaldo R$ {saldo:.2f}")

    elif opcao == 'q':
        break

    else:
        print("Opção invalida, por favor selecione novamente a operação desejada.")