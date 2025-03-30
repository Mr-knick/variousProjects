import json
from utility import *


class PasswordData:
    def __init__(self, arguments={}):
        if arguments is None:
            arguments = {}
        self.__password_dict = {}
        self.__master_password = ""
        self.__passwords_visible = InputStyle.VISIBLE if arguments.get('passwords_visible',
                                                                       False) else InputStyle.HIDDEN
        self.__pass_validation = arguments.get('password_validation', True)
        self.__filepath = arguments.get('filepath', './pass.crypt')
        self.__existing_password_file = False
        self.app = None

    def __encode_json(self) -> json:
        return json.dumps(self.__password_dict).encode()

    def __decode_and_load(self, data: str) -> None:
        decoded_json_data = data
        self.__password_dict = json.loads(decoded_json_data)

    def __set_password(self, app: str, username: str, password: str) -> None:
        if app in self.__password_dict:
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
        self.__password_dict[app] = {'username': username, 'password': password}
        print(f'Password for {app} updated')
        return

    def __validate_password(self, password) -> bool:
        if self.__pass_validation:
            pass
        return True

    def initialization_work_flow(self):
        self.__find_file()
        if self.__existing_password_file:
            self.__enter_master_password()
            data = decrypt_file(self.__master_password, self.__filepath)
            self.__decode_and_load(data)
            return
        self.__enter_master_password(generate=True)

    def __find_file(self) -> None:
        if os.path.exists(self.__filepath):
            print(f'Password file: {self.__filepath} found.')
            self.__existing_password_file = True
            return
        print(f'No previous password file found. If one exists follow the help instructions to load.')

    def change_master_password(self) -> None:
        pass

    def __enter_master_password(self, generate: bool = False) -> None:
        while True:
            password = get_user_input(self.__passwords_visible, "Create or enter your existing master password: ")
            if not validate_user_input(password):
                print(f'Invalid input. Please try again.')
                continue
            if generate:
                if not self.__validate_password(password):
                    print(f'Password does not meet security requirements.')
                    continue
                else:
                    confirm_password = get_user_input(self.__passwords_visible, "Please confirm your master password: ")
                    if confirm_password != password:
                        print(f'Passwords do not match')
                        continue
                    break
        print(f'Password entered: {self._print_style(password)}')
        self.__master_password = password

    def _print_style(self, text: str, override_style: InputStyle = None) -> str:
        if override_style == InputStyle.VISIBLE:
            return f'{text}'
        if override_style == InputStyle.HIDDEN:
            return f'{print_hidden(text)}'
        if self.__passwords_visible == InputStyle.VISIBLE:
            return f'{text}'
        if self.__passwords_visible == InputStyle.HIDDEN:
            return f'{print_hidden(text)}'
        print('Print style not set')
        return ""

    def save_file(self):
        encrypt_file(self.__master_password, self.__filepath, self.__encode_json())
        print(f'Saved file {self.__filepath}')

    def view_applications(self):
        all_passwords = self.password_dict()
        print(
            f'Passwords below select [number] to copy to clipboard. Select [p] to see plain-text. Select [0] to return '
            f'to main menu.')
        if all_passwords.size() == 0:
            print(f'No passwords available please add or load a file to view passwords')
            input()
            return

        print(f'There are {all_passwords.size()} passwords saved')
        i = 0
        tempPassArr = [{}] * all_passwords.size() - 1
        for p in all_passwords:
            app_name = p['app']
            username = p['app']['username']
            password = p['app']['password']
            print(f'[{i}] App: {app_name} : Username {username} : Password {password[0:2]}**********')
            tempPassArr[i] = p
            i += 1
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
            add_to_clipboard(password_to_copy)
            print(f'{tempPassArr[int(user_selection)]["app"]} password copied to clipboard')
