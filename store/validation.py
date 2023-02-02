import logging
import string


def invalid_whitespace(items: list) -> str | None:
    for item in items:
        if item == ' ':
            return 'Nenhum item pode ser um espaço em branco'
        elif item[0] == ' ':
            return 'Nenhum item pode iniciar com um espaço em branco'
        elif item[-1] == ' ':
            return 'Nenhum item pode finalizar com um espaço em branco'
    return None


def invalid_username(username: str) -> str | None:
    if len(username) < 2:
        return 'Nome de usuário curto, precisa ter 3 ou mais caracteres'

    for char in username:
        if char not in string.ascii_lowercase + string.digits:
            return f'Nome de usuário não pode conter " {char} "'

    return None


def invalid_email(email: str) -> str | None:
    if '@' not in email or '.' not in email:
        return 'O email fornecido é inválido'
    return None


def invalid_password(password: str, password_confirm: str) -> str | None:
    if len(password) < 8:
        return 'Senha muito pequena, precisa ter 8 ou mais caracteres'

    found_lowercase_in_password = False
    for char in string.ascii_lowercase:
        if char in password:
            found_lowercase_in_password = True
            break
    if not found_lowercase_in_password:
        return 'Sua senha não contém letras minúsculas'

    found_uppercase_in_password = False
    for char in string.ascii_uppercase:
        if char in password:
            found_uppercase_in_password = True
            break
    if not found_uppercase_in_password:
        return 'Sua senha não contém letras maiúsculas'

    found_digits_in_password = False
    for char in string.digits:
        if char in password:
            found_digits_in_password = True
            break
    if not found_digits_in_password:
        return 'Sua senha não contém números'

    found_punctuation_in_password = False
    for char in string.punctuation:
        if char in password:
            found_punctuation_in_password = True
            break
    if not found_punctuation_in_password:
        return 'Sua senha não contém caracteres especiais'

    if password != password_confirm:
        return 'As senhas não coincidem'

    return None
