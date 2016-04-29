from numeroscadastrais import cpf
import numeroscadastrais.exceptions as cpf_exceptions

def check_valid_1():
    """Diz se um CPF é válido ou não."""
    user_cpf_string = input("Digite um CPF: ")
    if cpf.is_valid(user_cpf_string):
        print("Esse CPF é válido.")
    else:
        print("Esse CPF não é válido.")

def check_valid_2():
    """Diz se um CPF está no formato correto ou possui um número inválido."""
    user_cpf_string = input("Digite um CPF: ")
    
    try:    
        cpf.require_valid(user_cpf_string)
    except cpf_exceptions.InvalidIdFormat:
        print(
            "Formato incorreto.\n"
            "Digite 11 digitos. Pontos e traços são permitidos."
        )
    except cpf_exceptions.InvalidIdValue:
        print(
            "CPF incorreto.\n"
            "Você deve ter digitado um número errado. Esse CPF não existe."
        )
    else:
        print("Esse CPF é válido.")

def check_valid_3():
    """Diz o motivo exato pelo qual o CPF é inválido."""
    user_cpf_string = input("Digite um CPF: ")
    
    try:
        cpf.require_valid(user_cpf_string)
    except cpf_exceptions.InvalidCharacters:
        print("Esse CPF contém letras ou outros caractéres inválidos.")
    except cpf_exceptions.InvalidLength:
        print("Esse CPF não está no tamanho correto de 11 caractéres.")
    except cpf_exceptions.InvalidCheckDigit:
        print("Esse CPF foi digitado incorretamente.")
    except cpf_exceptions.InvalidSpecificId:
        # Caso de 111.111.111-11, 222.222.222-22, etc.
        print("Esse CPF não existe.")
    else:
        print("Esse CPF é válido.")


def equality_1():
    """Diz se um CPF equivale a outro usando somente strings."""
    test_cpf_string = '123.456.789-10'
    user_cpf_string = input("Digite o CPF %s: " % test_cpf_string)
    if cpf.compare_strings(test_cpf_string, user_cpf_string):
        print("Você digitou o mesmo CPF.")
    else:
        print("Você não digitou o mesmo CPF.")

def equality_2():
    """Diz se um CPF equivale a outro usando uma string."""
    test_cpf_string = '12345678910'
    test_cpf = CPF(test_cpf_string)
    user_cpf_string = input("Digite o CPF %s: " % test_cpf)
    if test_cpf.equals_string(user_cpf_string):
        print("Você digitou o mesmo CPF.")
    else:
        print("Você não digitou o mesmo CPF.")

def equality_3():
    """Diz se um CPF equivale a outro usando somente a estrutura cpf.CPF."""
    try:
        cpf_1 = CPF(input("Digite um CPF: "))
    except cpf_exceptions.InvalidIdFormat:
        print("Formato inválido.")
        return
    
    try:
        cpf_2 = CPF(input("Digite outro CPF: "))
    except cpf_exceptions.InvalidIdFormat:
        print("Formato inválido.")
        return
    
    if cpf_1 == cpf_2:
        print("Você digitou o mesmo CPF.")
    else:
        print("Você não digitou o mesmo CPF.")


def components():
    """Diz as partes de um CPF."""
    try:
        user_cpf = cpf.CPF(input("Digite um CPF: "))
    except cpf_exceptions.InvalidIdFormat:
        print("CPF no formato inválido.")
    
    print("CPF digitado: %s" % user_cpf)
    print("Números aleatórios: %s" % user_cpf.digitos_aleatorios)
    print("Digito região fiscal: %s" % user_cpf.digito_regiao_fiscal)
    print("Região fiscal: %s" % user_cpf.regiao_fiscal)
    print("Digitos verificadores: %s" % user_cpf.digitos_verificadores)
    print("CPF Válido: %s" % ("Sim" if user_cpf.is_valid else "Não"))
    
    