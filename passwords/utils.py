import random
import string


def generate_password(length=12):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols),
    ]
    for i in range(length - 4):
        password.append(random.choice(lowercase + uppercase + digits + symbols))
    random.shuffle(password)
    return "".join(password)
