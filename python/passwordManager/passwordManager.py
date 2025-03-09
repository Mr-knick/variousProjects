"""
This is a description of the program

Usage:
  passwordManager.py [--file=<f>] [--app=<a>] [--noPasswordValidation] [--passwordsVisible]

Options:
  -h --help               Show this screen.
  --file=<f>              The encrypted file with passwords. (./pass.crypt by default)
  --app=<a>               Copies the password for a single saved application to clipboard then exits program
  --noPasswordValidation  Deactivates password validation regex
  --passwordsVisible      Will print all passwords as plain text to console
"""

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
import json
from docopt import docopt

import enum
from typing import Optional

from pycparser.ply.yacc import string_types


class InputStyle(enum.Enum):
    HIDDEN = 1
    VISIBLE = 2

class PasswordData:
    def __init__(self, arguments=None):
        if arguments is None:
            arguments = {}
        self._password_dict = {}
        self._passwords_visible = InputStyle.VISIBLE if arguments.get('passwords_visible', False) else InputStyle.HIDDEN
        self._pass_validation = arguments.get('password_validation', True)
        self._filepath = arguments.get('filepath', './pass.crypt')

    def encode(self) -> json:
        return json.dumps(self._password_dict).encode()

    def decode(self, data: bytearray) -> None:
        decoded_json_data = data.decode()
        self._password_dict = json.loads(decoded_json_data)

    def set_password(self, app, username, password):
        if app in self._password_dict:
            print(f'Password already exists for {app} updating value. Do you wish to replace (yes/no) [no]')
            # warning setup logging
            user_input = input().lower().strip()
            while True:
                if not user_input or user_input in ("no", "n"):
                    print(f'Password not {app} updated')
                    return
                elif user_input in ("yes", "y"):
                    break
                else:
                    print(f'Invalid input please select (y or n) or q to quit')
                    if user_input == "q":
                        exit(0)
        self._password_dict[app] = {'username': username, 'password': password}
        print(f'Password for {app} updated')
        return

    def validate_username(self, username):
        pass

    def validate_password(self, password):
        pass

    def loaded_info(self):
        # print(f'Applications currently saved: {}')
        # for app in self.password_dict:
        #     print(f'app')

        print(f'Settings:')
        print(f'PasswordLength: {self.settings_dict.get('password_length', "Default (16)")}')
        # print(f'PasswordLength: {self.settings_dict.get('password_length', "Default (16)")}')

    def find_file(self):
        if os.path.exists(self.settings_dict['filepath']):
            print(f'Password file: {self.settings_dict['filepath']} found.')
            return
        print(f'No previous password file found. If one exists follow the help instructions to load.')

    def enter_master_password(self):
        while True:
            password = get_user_input(self._passwords_visible, "Create or enter your existing master password: ")
            if not validate_user_input(password):
                print(f'Invalid input. Please try again.')
                continue
        print(f'Password entered (but not shown): {print_hidden(password)}')
        return password


def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)
    print(f'{print_hidden(text)} copied to clipboard')

def print_hidden(text: str) -> str:
    return f'{text[0:1] + '*' * (len(text)-1)}'

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

def control_interface(pd):
    while True:
        user_selection = input()
        clear_screen()

        if user_selection == "q":
            exit(0)
        elif user_selection == 1:
            load_file(pd)
        elif user_selection == 2:
            save_file(pd)
        elif user_selection == 3:
            view_applications(pd)
        elif user_selection == 4:
            generate_password()
        elif user_selection == 5:
            change_settings(pd)
        else:
            print(f'{user_selection} is not a valid option\n')

        print(f'Password Manager make selection below\n'
              f'[L] Load File {pd.settings_dict.get('file', 'File not found')}\n'
              f'[2] Save File {pd.settings_dict.get('file', 'File not found')}\n'
              f'[3] View available applications\n'
              f'[4] Generate a random password\n'
              f'[5] Settings\n'
              f'[q] Exit application\n')

        # View Applications -> view password as plain-text
        # copy password to clipboard for a given application

def load_file(pd):
    pass

def save_file(pd):
    pass

def view_applications(pd):
    all_passwords = pd.password_dict()
    print(f'Passwords below select [number] to copy to clipboard. Select [p] to see plain-text. Select [0] to return to main menu.')
    if all_passwords.size() == 0:
        print(f'No passwords available please add or load a file to view passwords')
        input()
        return

    print(f'There are {all_passwords.size()} passwords saved')
    i = 0
    tempPassArr = [{}] * all_passwords.size()-1
    for p in all_passwords:
        app_name = p['app']
        username = p['app']['username']
        password = p['app']['password']
        print(f'[{i}] App: {app_name} : Username {username} : Password {password[0:2]}**********')
        tempPassArr[i] = p
        i+=1
    user_selection = input()
    if user_selection == 'p':
        i = 0
        for p in all_passwords:
            app_name = p['app']
            username = p['app']['username']
            password = p['app']['password']
            print(f'[{i}] App: {app_name} : Username {username} : Password {password}')
            i += 1
    elif user_selection == 0:
        return
    elif int(user_selection) in tempPassArr:
        password_to_copy = tempPassArr[int(user_selection)]['app']['password']
        addToClipBoard(password_to_copy)
        print(f'{tempPassArr[int(user_selection)]['app']} password copied to clipboard')

def change_settings(pd):
    pass

def process_user_input() -> dict:
    args = docopt(__doc__)
    filepath = args.get('--file', None)
    app = args.get('--app', None)
    password_validation = args.get('--noPasswordValidation', False)
    passwords_visible = args.get('--passwordsVisible', False)
    return { 'filepath': filepath,
             'app': app,
             'password_validation': password_validation,
             'passwords_visible': passwords_visible }

def main():
    pd = PasswordData(process_user_input())
    pd.find_file
    pd.enter_master_password

    # control_interface(pd)
    encrypt_file('password', 'test_file.crypt', 'this is my string of json')
    t = decrypt_file('password', 'test_file.crypt')
    print(t)

if __name__ == "__main__":
    main()
