#!/user/bin/env python3
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

from docopt import docopt

from passwordData import PasswordData
import utility


def single_password_workflow(pd):
    pass


def control_interface(pd: PasswordData) -> None:
    while True:
        utility.clear_screen()
        print(f'*** Password Manager make selection below ***\n'
              f'[v] View/modify/create passwords\n'
              f'[g] Generate a random password\n'
              f'[s] Save current file with current master password\n'
              f'[c] Change current master password\n'
              f'[q] Exit application\n')

        user_selection = input().strip().lower()
        if not utility.validate_user_input(user_selection):
            continue

        if user_selection == "q":
            exit(0)
        elif user_selection == "s":
            pd.save_file()
        elif user_selection == "v":
            application_view_control(pd)
        elif user_selection == "c":
            pd.change_master_password()
        elif user_selection == "g":
            utility.generate_password()
        else:
            print(f'{user_selection} is not a valid option\n')


def application_view_control(pd):
    while True:
        utility.clear_screen()
        print(f'To view, modify, create, or delete passwords please make a selection below\n'
              f'[v] View available applications\n'
              f'[c] Create available applications\n'
              f'[m] Modify available applications\n'
              f'[s] Save\n'
              f'[q] Exit application\n')

        user_selection = input().strip().lower()
        if not utility.validate_user_input(user_selection):
            continue

        if user_selection == 'v':
            application_viewer_control(pd)
        elif user_selection == 'c':
            application_create_control(pd)
        elif user_selection == 'm':
            application_modify_control(pd)
        elif user_selection == 's':
            pd.save_file()
        elif user_selection == 'q':
            exit(0)


def application_viewer_control(pd):
    pass


def application_create_control(pd):
    pass


def application_modify_control(pd):
    pass
    # select, change, or delete


def process_user_input() -> dict:
    return_dict = {}
    args = docopt(__doc__)
    if args['--file'] is not None:
        return_dict['filepath'] = args['--file']
    if args['--app'] is not None:
        return_dict['app'] = args['--app']
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
