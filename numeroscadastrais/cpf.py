import re

from .exceptions import *

class CPF:
    """Cadastro de Pessoa Física.
    
    Uma simples estrutura que mapeia e normaliza strings de CPF.
    
    Use cpf.is_valid() e cpf.require_valid() se precisar apenas de validar
    números de CPF.
    
    Formato: AAA.AAA.AAB-ZZ
    A - Digitos aleátorios.
    B - Digito da região fiscal responsável pelo CPF.
    Z - Digitos verificadores.
    
    Como usar:
        >>> my_cpf = CPF('123.456.789-10')
        >>> my_cpf.regiao_fiscal
        9
        >>> my_cpf.digitos_verificadores
        10
        >>> my_cpf.digits_only
        '12345678910'
        >>> "Meu CPF é %s" % CPF('12345678910')
        'Meu CPF é 123.456.789-10'
        
        >>> try:
        >>>     user_cpf = CPF(valor_digitado_pelo_usuario)
        >>> except InvalidIdFormat:
        >>>     print("Formato inválido!")
        >>> else:
        >>>     if not user_cpf.is_valid:
        >>>         print("Número de CPF inválido!")
        
        >>> d = {}
        >>> d[CPF('123.456.789-10')] = 42
        >>> d[CPF('12345678910')]
        42
        
        >>> CPF('123.456.789-10') == CPF('12345678910')
        True
        >>> CPF('123.456.789-10').equals_string('12345678910')
        True
    
    """
    
    def __init__(self, cpf_string):
        """Cria um número de CPF a partir de uma string.
        
        Pontos, espaços e traços serão removidos da string antes dela ser
        processada. Letras e outros caractéres não são removidos e resultam na
        exceção InvalidCharacters.
        
        A string precisa ter 9 ou 11 digitos de comprimento. Caso tiver 9,
        os dois digitos verificadores serão calculados e adicionados a string,
        caso tiver 11, a validade dos digitos será verificada. Não resulta em
        exceção criar um CPF com valor inválido. A validade do CPF pode ser
        verificada pela propriedade is_valid.
        
        Strings com outros tamanhos resultam na exceção InvalidLength.
        
        """
        cpf_digits = strip_symbols(cpf_string)
        require_format(cpf_digits, True)
        
        if len(cpf_digits) == 11:
            self.__valid = (
                has_correct_check_digit(cpf_digits)
                and not is_specifically_invalid_number(cpf_digits)
            )
        else:
            cpf_digits += calc_check_digit(cpf_digits)
            self.__valid = not is_specifically_invalid_number(cpf_digits)
            
        self.__cpf_digits = cpf_digits
    
    
    def equals_string(self, cps_string):
        """Verifica se o CPF é o mesmo que o número contido em uma string.
        
        Esse método é o mesmo que CPF(a) == CPF(b), porém retorna False caso
        a cps_string seja inválida.
        
        Veja também:
            compare_strings(cps_string_a, cps_string_b)
        
        """
        try:
            other = CPF(cps_string)
        except InvalidIdError:
            return False
        else:
            return self == other
    
    
    @property
    def is_valid(self):
        """Se esse número de CPF é válido."""
        return self.__valid
    
    @property
    def digitos_aleatorios(self):
        """Os primeiros 8 digitos do CPF."""
        return self.__cpf_digits[0:8]
    
    @property
    def digito_regiao_fiscal(self):
        """O nono digito do CPF."""
        return self.__cpf_digits[8]
    
    @property
    def digitos_verificadores(self):
        """Os últimos dois digitos do CPF."""
        return self.__cpf_digits[9:11]
    
    @property
    def regiao_fiscal(self):
        """Retorna o número da região fiscal responsável pelo CPF.
        
        Esse é o mesmo valor que digito_regiao_fiscal, exceto para
        o digito zero, que representa a décima região.
        
        """
        
        result = int(self.digito_regiao_fiscal) 
        
        # A décima região fiscal é identificada pelo digito zero.
        if result == 0:
            return 10
        
        return result
    
    @property
    def digits_only(self):
        """Retorna somente os digitos do CPF sem formatação especial."""
        return self.__cpf_digits
    
    
    def __repr__(self):
        """Representação do CPF.
        
        Deve ser:
            CPF('123.456.789-10')
        
        """
        
        return 'CPF(\'' + str(self) + '\')'
    
    def __str__(self):
        """CPF como string.
        
        Deve ser:
            123.456.789-10
        
        Use a propriedade digits_only para string com apenas os digitos.
        
        """
        
        return (
            self.digitos_aleatorios[0:3] +
            '.' + self.digitos_aleatorios[3:6] +
            '.' + self.digitos_aleatorios[6:8] + self.digito_regiao_fiscal +
            '-' + self.digitos_verificadores
        )
    
    
    def __eq__(self, other):
        """Compara um CPF com outro CPF.
        
        Situações verdadeiras:
            Pontuação diferente.
            CPF('123.456.789-10') == CPF('12345678910')
            Digitos Verificadores.corretos e CPF sem os DV.
            CPF('111.111.111-11') == CPF('111.111.111')
            Ambos.
            CPF('111.111.111-11') == CPF('111111111')
        
        Situações falsa:
            Digitos Verificadores.incorretos e CPF sem os DV.
            CPF('123.456.789-10') != CPF('123.456.789')
            Digitos verificadores diferentes.
            CPF('111.111.111-11') != CPF('111.111.111-99')
            
        """
        if not isinstance(other, CPF):
            return False
        
        return self.__cpf_digits == other.__cpf_digits
    
    def __hash__(self):
        return hash(self.__cpf_digits)


def compare_strings(cpf_string_a, cpf_string_b):
    """Retorna se duas strings são o mesmo CPF.
    
    Caso qualquer das strings esteja no formato inválido, o retorno é falso.
    
    Veja CPF.__eq__ para exemplos de situações verdadeiras e falsas.
    """
    try:
        cpf_a = CPF(cpf_string_a)
        cpf_b = CPF(cpf_string_b)
    except InvalidIdFormat:
        return False
    else:
        return cpf_a == cpf_b


def is_valid(cpf_string, allow_missing_check_digits=False):
    """Retorna se um número de CPF é válido.
    
    Args:
        allow_missing_check_digits - Verdadeiro se um número sem os dois 
                                     digitos verificadores for válido.
    """
    try:
        require_valid(cpf_string, allow_missing_check_digits)
    except InvalidIdError:
        return False
    else:
        return True


def require_valid(cpf_string, allow_missing_check_digits=False):
    """Emite exceções para diferentes problemas em um número de CPF.
    
    Como usar:
        try:
            require_valid(valor_digitado_pelo_usuario)
        except InvalidCharacters:
            print('Favor digitar somente números, pontos e traços.')
        except InvalidLength:
            print('Favor digitar 11 digitos.')
        except InvalidCheckDigit:
            print('Você digitou o CPF incorretamente.')
        except InvalidSpecificId:
            print('Este número CPF não existe.')
        else:
            print('CPF digitado é válido.')
        
        
    Args:
        allow_missing_check_digits - Verdadeiro se um número sem os dois 
                                     digitos verificadores for válido.
    """
    cpf_digits = strip_symbols(cpf_string)
    require_format(cpf_digits, allow_missing_check_digits)
    if len(cpf_string) == 11:
        if not has_correct_check_digit(cpf_digits):
            raise InvalidCheckDigit("CPF check digit incorrect")
        if is_specifically_invalid_number(cpf_digits):
            raise InvalidCheckDigit("CPF number specifically invalid")


def strip_symbols(cpf_string):
    """Remove espaços, pontos e traços de uma string."""
    return re.sub(r'[\s.-]', '', cpf_string)

def require_format(cpf_digits, allow_missing_check_digits=False):
    """Emite exceções caso o formato do CPF esteja incorreto."""
    if not cpf_digits.isdigit():
        raise InvalidCharacters("CPF must contain digits only.")
    
    if len(cpf_digits) != 11:
        if not allow_missing_check_digits:
            raise InvalidLength("CPF length must be 11 digits")
        elif len(cpf_digits) != 9:
            raise InvalidLength("CPF length must be either 9 or 11 digits")


def calc_check_digit(cpf_digits):
    """Calcula os 2 digitos verificadores para validar um CPF."""
    # Caso a string tenha 11 digitos, use somente os primeiros 9
    cpf_digits = cpf_digits[:9]
    
    def multiply_digits(digits, weights):
        for a, b in zip(digits, weights):
            yield int(a) * b
    
    dv1 = (sum(multiply_digits(cpf_digits, range(1, 10))) % 11) % 10
    dv2 = (sum(multiply_digits(cpf_digits + str(dv1), range(0, 10))) % 11) % 10
    
    return '%d%d' % (dv1, dv2)

def has_correct_check_digit(cpf_digits):
    """Retorna se o digito verificador em um CPF está correto."""
    dv = calc_check_digit(cpf_digits[:-2])
    return dv == cpf_digits[-2:]


def is_specifically_invalid_number(cpf_digits):
    """Retorna se o número de CPF é especificamente inválido.
    
    Números inválidos são:
        111.111.111-11, 222.222.222-222, 333.333.333-333, etc.
        
        Veja item V, REGRAS DE NEGÓCIO PARA PREENCHIMENTO DOS CAMPOS DO
        DOCUMENTO DE ARRECADAÇÃO DE RECEITAS FEDERAIS, sub-item b1 de
        http://www3.tesouro.gov.br/spb/downloads/arquivos/protocolo_arrecadacao_DARF.pdf
    """
    return all(cpf_digits[i] == cpf_digits[0] for i in range(1, 9))
    