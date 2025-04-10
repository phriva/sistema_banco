from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\nSaldo insuficiente!!")
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!!")
            return True
        else:
            print("\nValor invalido!!")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDeposito realizado com sucesso!!")
        else:
            print("\nValor invalido!!")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nValor do saque maior que o permitido!!")
        elif excedeu_saques:
            print("\nLimite de saques atingido!!")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agência: {self.agencia}
            C/C: {self.numero}
            Titular: {self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adiciona_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adiciona_transacao(self)
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adiciona_transacao(self)
    
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

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

def depositar(clientes): 
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!!")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes): 
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Ainda Não foi efetuado nenhuma operação!!"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n R${transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo R$ {conta.saldo:.2f}")

def criar_cliente(clientes):
    cpf = input("Digite o numero do CPF do usurario(somente digitos): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe usuario com esse CPF")
        return

    nome = input("\nDigite o nome do usuario: ")
    data = input("\nDigite a data de nasciento do usuario(dd-mm-aaaa): ")
    endereco = input("\nDigite o endereco do usuario(logradouro, nro - bairro - cidade/sigla): ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta!!")
        return
    
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def criar_conta(numero_da_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, fluxo de criação de conta encerrado!!")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_da_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nconta criada com sucesso!")
    
def listar_conta(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'c':
            criar_cliente(clientes)

        elif opcao == 'cc':
            numero_da_conta = len(contas) + 1
            criar_conta(numero_da_conta, clientes, contas)

        elif opcao == 'lc':
            listar_conta(contas)

        elif opcao == 'q':
            break

        else:
            print("Opção invalida, por favor selecione novamente a operação desejada.")

main()
