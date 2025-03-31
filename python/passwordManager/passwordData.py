import json
import os
import re
from utility import InputStyle, decrypt_file, encrypt_file, get_user_input_styled, validate_user_input, print_hidden


class PasswordData:
    def __init__(self, arguments={}):
        if arguments is None:
            arguments = {}
        self._password_dict = {}
        self._master_password = ""
        self._passwords_visible = InputStyle.VISIBLE if arguments.get('passwords_visible',
                                                                       False) else InputStyle.HIDDEN
        self._skip_pass_validation = arguments.get('password_validation', False)
        self._filepath = arguments.get('filepath', './pass.crypt')
        self._existing_password_file = False
        self.app = None
        self.password_length = arguments.get('password_length', 14)

    def enter_password(self, app_name: str, create: bool = False) -> str:
        while True:
            password = get_user_input_styled(self._passwords_visible, f"Enter {app_name} password: ")
            if not validate_user_input(password):
                print(f'Invalid input. Please try again.')
                continue
            if create:
                if not self.__validate_password(password):
                    print(f'Password does not meet security requirements.')
                    continue
                else:
                    confirm_password = get_user_input_styled(self._passwords_visible, f"Please confirm your "
                                                                                       f"{app_name} password: ")
                    if confirm_password != password:
                        print(f'Passwords do not match')
                        continue
            print(f'Password entered: {self.print_style(password)}')
            return password

    def print_style(self, text: str, override_style: InputStyle = None) -> str:
        if override_style == InputStyle.VISIBLE:
            return f'{text}'
        if override_style == InputStyle.HIDDEN:
            return f'{print_hidden(text)}'
        if self._passwords_visible == InputStyle.VISIBLE:
            return f'{text}'
        if self._passwords_visible == InputStyle.HIDDEN:
            return f'{print_hidden(text)}'
        print('Print style not set')
        return ""

    def save_file(self):
        encrypt_file(self._master_password, self._filepath, self.__encode_json())
        print(f'Saved file {self._filepath}')

    def change_password_visibility(self):
        self._passwords_visible = InputStyle.VISIBLE

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
        if self._existing_password_file:
            while True:
                self.__enter_master_password(create=False)
                try:
                    data = decrypt_file(self._master_password, self._filepath)
                    break
                except ValueError:
                    print(f'Could not decrypt {self._filepath} confirm correct master password was entered')
            self.__decode_and_load(data)
            return
        self.__enter_master_password(create=True)

    def set_password_data(self, application, username, password) -> bool:
        self._password_dict[application] = {'username': username, 'password': password}

    def change_master_password(self) -> None:
        self._master_password = self.enter_password(app_name='master', create=True)

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

    def __validate_password(self, password: str, print_errors: bool = True) -> bool:
        good_password = True
        if not self._skip_pass_validation:
            uppercase_pattern = re.compile("[A-Z]")
            lowercase_pattern = re.compile("[a-z]")
            digit_pattern = re.compile("[0-9]")
            special_char_pattern = re.compile("[^A-Za-z0-9]")
            errors = []

            if len(password) < 8:
                errors.append("Password must be at least 8 characters long\n")
            if not uppercase_pattern.search(password):
                errors.append("Password must contain at least one uppercase letter\n")
                good_password = False
            if not lowercase_pattern.search(password):
                errors.append("Password must contain at least one lowercase letter\n")
                good_password = False
            if not digit_pattern.search(password):
                errors.append("Password must contain at least one digit\n")
                good_password = False
            if not special_char_pattern.search(password):
                errors.append("Password must contain at least one special \n")
            if print_errors:
                print(*errors)
            if len(errors) > 0:
                good_password = False

        return good_password

    def __find_file(self) -> None:
        if os.path.exists(self._filepath):
            print(f'Password file: {self._filepath} found.')
            self._existing_password_file = True
            return
        print(f'No previous password file found. If one exists follow the help instructions to load.')

    def __enter_master_password(self, create: bool = False) -> None:
        self._master_password = self.enter_password(app_name='master', create=create)
