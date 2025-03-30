import json
import os
from utility import InputStyle, decrypt_file, encrypt_file, get_user_input_styled, validate_user_input, print_hidden


class PasswordData:
    def __init__(self, arguments={}):
        if arguments is None:
            arguments = {}
        self._password_dict = {}
        self.__master_password = ""
        self.__passwords_visible = InputStyle.VISIBLE if arguments.get('passwords_visible',
                                                                       False) else InputStyle.HIDDEN
        self.__pass_validation = arguments.get('password_validation', True)
        self.__filepath = arguments.get('filepath', './pass.crypt')
        self.__existing_password_file = False
        self.app = None

    def enter_password(self, app_name: str, create: bool = False) -> str:
        while True:
            password = get_user_input_styled(self.__passwords_visible, f"Enter {app_name} password: ")
            if not validate_user_input(password):
                print(f'Invalid input. Please try again.')
                continue
            if create:
                if not self.__validate_password(password):
                    print(f'Password does not meet security requirements.')
                    continue
                else:
                    confirm_password = get_user_input_styled(self.__passwords_visible, f"Please confirm your "
                                                                                       f"{app_name} password: ")
                    if confirm_password != password:
                        print(f'Passwords do not match')
                        continue
            print(f'Password entered: {self._print_style(password)}')
            return password

    def print_style(self, text: str, override_style: InputStyle = None) -> str:
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

    def change_password_visibility(self):
        self.__passwords_visible = InputStyle.VISIBLE

    def get_num_passwords(self) -> int:
        return len(self._password_dict)

    def get_saved_apps(self) -> list:
        return sorted(self._password_dict.keys())

    def get_app_name_by_index(self, index) -> str:
        return sorted(self._password_dict.keys())[index]

    def get_app_data(self, app_name) -> dict:
        return self._password_dict[app_name]

    def initialization_work_flow(self):
        self.__find_file()
        if self.__existing_password_file:
            while True:
                self.__enter_master_password(create=False)
                try:
                    data = decrypt_file(self.__master_password, self.__filepath)
                    break
                except ValueError:
                    print(f'Could not decrypt {self.__filepath} confirm correct master password was entered')
            self.__decode_and_load(data)
            return
        self.__enter_master_password(create=True)

    def set_password_data(self, application, username, password) -> bool:
        self._password_dict[application] = {'username': username, 'password': password}

    def change_master_password(self) -> None:
        pass

    def remove_app(self, app_name) -> None:
        del self._password_dict[app_name]

    def __encode_json(self) -> str:
        return json.dumps(self._password_dict)

    def __decode_and_load(self, data: str) -> None:
        decoded_json_data = data
        self._password_dict = json.loads(decoded_json_data)

    def __set_password(self, app: str, username: str, password: str) -> None:
        self._password_dict[app] = {'username': username, 'password': password}
        print(f'Password for {app} updated')
        return

    def __validate_password(self, password) -> bool:
        if self.__pass_validation:
            pass
        return True

    def __find_file(self) -> None:
        if os.path.exists(self.__filepath):
            print(f'Password file: {self.__filepath} found.')
            self.__existing_password_file = True
            return
        print(f'No previous password file found. If one exists follow the help instructions to load.')

    def __enter_master_password(self, create: bool = False) -> None:
        self.__master_password = self.__enter_password(app_name='master', create=create)
