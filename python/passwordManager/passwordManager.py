#!/user/bin/env python3
"""
This is a description of the program

Usage:
  passwordManager.py [--file=<f>] [--app=<a>] [--length=<l>] [--noPasswordValidation] [--passwordsVisible]

Options:
  -h --help               Show this screen.
  --file=<f>              The encrypted file with passwords. (./pass.crypt by default)
  --app=<a>               Copies the password for a single saved application to clipboard then exits program
  --length=<l>            Override default length(14) of generated password
  --noPasswordValidation  Deactivates password validation regex
  --passwordsVisible      Will print all passwords as plain text to console
"""

from docopt import docopt
from typing import Optional

from passwordData import PasswordData
import utility


def single_password_workflow(pd):
    app = pd.get_app_data(pd.app)
    print(f'App: {app}\n'
          f'Username: {app["username"]}\n'
          f'Password: {pd.print_style(app["password"])}')
    utility.add_to_clipboard(app['password'])
    exit(0)


def control_interface(pd: PasswordData) -> None:
    while True:
        utility.clear_screen()
        print(f'*** Password Manager make selection below ***\n'
              f'[v] View/modify/create passwords\n'
              f'[g] Generate a random password\n'
              f'[s] Save current file with current master password\n'
              f'[c] Change current master password\n'
              f'[q] Exit application\n')

        user_selection = utility.get_validated_user_selection()

        if user_selection == "q":
            exit(0)
        elif user_selection == "s":
            pd.save_file()
        elif user_selection == "v":
            application_view_control(pd)
        elif user_selection == "c":
            pd.change_master_password()
        elif user_selection == "g":
            generated_password = utility.generate_password(pd.password_length)
            print(pd.print_style(generated_password))
            if input('Copy to clipboard [c]') == 'c':
                utility.add_to_clipboard(generated_password)
        else:
            print(f'{user_selection} is not a valid option\n')


def application_view_control(pd):
    while True:
        utility.clear_screen()
        print(f'To view, modify, create, or delete passwords please make a selection below\n'
              f'[v] View available passwords\n'
              f'[c] Create new saved passwords\n'
              f'[m] Modify saved passwords\n'
              f'[s] Save\n'
              f'[q] Exit application\n')

        user_selection = utility.get_validated_user_selection()

        if user_selection == 'v':
            password_viewer_control(pd)
        elif user_selection == 'c':
            password_create_control(pd)
        elif user_selection == 'm':
            password_modify_control(pd)
        elif user_selection == 'b':
            return
        elif user_selection == 's':
            pd.save_file()
        elif user_selection == 'q':
            exit(0)


def viewer(pd) -> Optional[str]:
    if pd.get_num_passwords() == 0:
        print(f'No passwords available please add or load a file to view passwords.')
        input('Press enter to continue...')
        return

    print(f'There are {pd.get_num_passwords()} passwords saved')

    for index, app_name in enumerate(pd.get_saved_apps()):
        print(4 * '*****')
        app = pd.get_app_data(app_name)
        print(f'[{index}] App: {app_name}\n'
              f'Username: {app["username"]}\n'
              f'Password: {pd.print_style(app["password"])}')

    user_selection = utility.get_validated_user_selection()

    return user_selection


def password_viewer_control(pd):
    while True:
        utility.clear_screen()
        print(
            f'Passwords below select [number] of application to copy to clipboard. '
            f'\nSelect [p] to see plain-text. '
            f'\nSelect [b] to return to previous menu.')
        user_selection = viewer(pd)
        if not user_selection:
            return

        if user_selection.lower() == 'b':
            return

        elif user_selection.lower() == 'p':
            pd.change_password_visibility()

        elif user_selection.isdigit():
            user_selection_int = int(user_selection)
            if pd.get_num_passwords() >= user_selection_int >= 0:
                app_name = pd.get_app_name_by_index(user_selection_int)
                app = pd.get_app_data(app_name)
                print(f'App: {app}\n'
                      f'Username: {app["username"]}\n'
                      f'Password: {pd.print_style(app["password"])}')
                utility.add_to_clipboard(app['password'])
            else:
                print(f'Selection of {user_selection} is out of range.')
                input('Press enter to continue...')

        else:
            print(f'Selection of {user_selection} not found in password file. Please check spelling and case.')
            input('Press enter to continue...')


def password_create_control(pd):
    print('Name of new application:')
    app_name = utility.get_validated_user_selection()
    print('Username within application:')
    username = utility.get_validated_user_selection()
    print('Auto generate[g] or create[c] password')
    while True:
        user_selection_password_generation = utility.get_validated_user_selection()
        if user_selection_password_generation == 'g':
            new_password = utility.generate_password()
            break
        elif user_selection_password_generation == 'c':
            new_password = pd.enter_password(app_name, create=True)
            break
        else:
            print(f'Please select g or c')
            input('Press enter to continue...')

    pd.set_password_data(app_name, username, new_password)
    print(f'Password created for App: {app_name}\n Username: {username}\n Password: {pd.print_style(new_password)}')
    input('Press enter to continue...')


def password_modify_control(pd):
    while True:
        utility.clear_screen()
        print(
            f'Passwords below select [number] of application to modify'
            f'Select [b] to return to previous menu.'
            f'[s] Save\n'
            f'[q] Exit application\n')
        user_selection = viewer(pd)
        if not user_selection:
            return

        if user_selection == 'b':
            return
        elif user_selection == "s":
            pd.save_file()
        elif user_selection == 'q':
            exit(0)
        elif user_selection.isdigit():
            user_selection_int = int(user_selection)
            if pd.get_num_passwords() >= user_selection_int >= 0:
                app_name = pd.get_app_name_by_index(user_selection_int)
                app = pd.get_app_data(app_name)
                username = app["username"]
                password = app["password"]
                print(f'App: {app_name}\n'
                      f'Username: {app["username"]}\n'
                      f'Password: {pd.print_style(app["password"])}')
                print('\nSelect [d] to remove entry.'
                      '\nSelect [u] to change user name.'
                      '\nSelect [c] to change password.'
                      '\nSelect [g] to generate new password.'
                      '\nSelect [b] to return to previous menu')
                while True:
                    user_selection_modification = utility.get_validated_user_selection()
                    if user_selection_modification == 'b':
                        break
                    elif user_selection_modification == 'g':
                        new_password = utility.generate_password()
                        pd.set_password_data(app_name, username, new_password)
                        input('Password changed. Press enter to continue...')
                        return
                    elif user_selection_modification == 'c':
                        new_password = pd.enter_password(app_name, create=True)
                        pd.set_password_data(app_name, username, new_password)
                        input('Password changed. Press enter to continue...')
                        return
                    elif user_selection_modification == 'd':
                        print(f'Confirm delete of {app_name} [y]')
                        if utility.get_validated_user_selection() == 'y':
                            pd.remove_app(app_name)
                            input(f'{app_name} deleted. Press enter to continue...')
                            return
                        else:
                            input('Deletion canceled. Press enter to continue...')
                            return
                    elif user_selection_modification == 'u':
                        while True:
                            new_username = input(f'Input username for {app_name}')
                            print(f'Confirm set username of {new_username} [y]')
                            if utility.get_validated_user_selection() == 'y':
                                pd.set_password_data(app_name, new_username, password)
                            input('Username changed. Press enter to continue...')
                            return
                    print(f'Selection of {user_selection} is not a valid selection.')
                    input('Press enter to continue...')
            else:
                print(f'Selection of {user_selection} is out of range.')
                input('Press enter to continue...')

        else:
            print(f'Selection of {user_selection} not found in password file. Please check spelling and case.')
            input('Press enter to continue...')


def process_user_input() -> dict:
    return_dict = {}
    args = docopt(__doc__)
    if args['--file'] is not None:
        return_dict['filepath'] = args['--file']
    if args['--app'] is not None:
        return_dict['app'] = args['--app']
    if args['--length'] is not None:
        return_dict['length'] = args['--length']
    return_dict['password_validation'] = args.get('--noPasswordValidation', False)
    return_dict['passwords_visible'] = args.get('--passwordsVisible', False)
    return return_dict


def main():
    pd = PasswordData(process_user_input())
    pd.initialization_work_flow()
    if pd.app:
        single_password_workflow(pd)
        pass
    else:
        control_interface(pd)


if __name__ == "__main__":
    main()
