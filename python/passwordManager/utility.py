from dataclasses import dataclass
from tkinter.constants import HIDDEN

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode

import os
import getpass
import enum

from typing import Optional
from pycparser.ply.yacc import string_types


class InputStyle(enum.Enum):
    HIDDEN = 1
    VISIBLE = 2


def add_to_clipboard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)
    print(f'{print_hidden(text)} copied to clipboard')


def print_hidden(text: str) -> str:
    return f"{text[0:1] + '*' * (len(text)-1)}"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def generate_password():
    pass


def validate_user_input(user_intput: Optional[str] = "") -> bool:
    if len(user_intput) < 1:
        return False
    elif type(user_intput) != string_types:
        return False
    return True


def hidden_input(instruction: str) -> str:
    hidden_user_input = getpass.getpass(instruction)
    return hidden_user_input


def get_user_input(input_style: InputStyle, instructions: Optional[str] = "") -> Optional[str]:
    if input_style.HIDDEN:
        return hidden_input(instructions)
    if input_style.VISIBLE:
        return input(instructions)


def encrypt_file(password: str, file_path: str, data: str):
    # Generate a random salt
    salt = os.urandom(len(password))

    # Generate a random IV
    iv = os.urandom(16)

    # Derive a key from the password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Pad the data
    encoded_data = data.encode()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(encoded_data) + padder.finalize()

    # Encrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Write the salt, IV, and encrypted data to a new file
    with open(file_path, 'wb') as file:
        file.write(salt + iv + encrypted_data)


def decrypt_file(password: str, file_path: str) -> str:
    # Read the salt, IV, and encrypted data from the file
    with open(file_path, 'rb') as file:
        salt = file.read(len(password))
        iv = file.read(16)
        encrypted_data = file.read()

    # Derive the key from the password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    # key = urlsafe_b64encode(kdf.derive(password.encode()))
    key = kdf.derive(password.encode())

    # Decrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the data
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data.decode('UTF-8')
