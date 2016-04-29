class InvalidIdError(ValueError):
    """Exceção base para números cadastrais inválidos."""
    pass

class InvalidIdFormat(InvalidIdError):
    """Exceção base para formato inválido de uma string."""
    pass

class InvalidIdValue(InvalidIdError):
    """Exceção base para numéros inválidos no formato de string válido."""
    pass


class InvalidCharacters(InvalidIdFormat):
    """Exceção para caractéres não permitidos contidos em uma string.
    
    Exemplo:
        Formato esperado: 123-456-789-10
        Formato usado: 123-ABC-?!¿-漢字
    """
    pass

class InvalidLength(InvalidIdFormat):
    """Exceção para comprimento de string incorreto.
    
    Exemplo:
        Tamanho esperado: 123-456-789-10
        Tamanho usado: 123
    """
    pass

class InvalidCheckDigit(InvalidIdValue):
    """Exceção para digitos verificadores incorretos.
    
    Exemplo:
        Digito correto: 111.111.111-11 (CPF)
        Digito incorreto: 111.111.111-55 (CPF)
    """
    pass

class InvalidSpecificId(InvalidIdValue):
    """Exceção certos números que são especificamente inválidos.
    
    Exemplo:
        Número válido: 100.000.987-44 (CPF)
        Número inválido: 111.111.111-11 (CPF)
    """
    pass