import pytest
from passwordManager import PasswordData
from utility import InputStyle, decrypt_file, encrypt_file
from unittest.mock import patch, MagicMock


def test_password_data_init():
    pd = PasswordData({'filepath': './pass.crypt'})
    assert pd._PasswordData__password_dict == {}
    assert pd._PasswordData__master_password == ""
    assert pd._PasswordData__passwords_visible == InputStyle.HIDDEN
    assert pd._PasswordData__pass_validation
    assert pd._PasswordData__filepath == './pass.crypt'


def test_encrypt_decrypt_file(tmp_path):
    password = "test_password"
    file_path = tmp_path / "test_file"
    data = "test_data"
    encrypt_file(password, str(file_path), data)
    decrypted_data = decrypt_file(password, str(file_path))

    assert decrypted_data == data



def test_password_data_initialization_workflow(tmp_path, mock_get_user_input=None):
    pd = PasswordData({'filepath': str(tmp_path / "test_file")})
    mock_get_user_input('test')
    monkeypatch.setattr('builtins.input', lambda _: "test input")
    get_user_input
    mocker.patch('your_module.input', return_value='No')
    pd._PasswordData__enter_master_password.input = lambda: 'some_input'

    pd._PasswordData__enter_master_password.input = lambda: 'some_input'
    mock_get_user_input.return_value = 'test_password'
    pd.initialization_work_flow()
    assert pd._PasswordData__master_password == 'test_password'


def test_password_data_save_file(tmp_path):
    pd = PasswordData({'filepath': str(tmp_path / "test_file")})
    pd.__password_dict = {"test_app": {"username": "test_username", "password": "test_password"}}
    pd.save_file()
    assert (tmp_path / "test_file").exists()


def test_password_data_view_applications(capsys):
    pd = PasswordData({'filepath': './pass.crypt'})
    pd.__password_dict = {"test_app": {"username": "test_username", "password": "test_password"}}
    pd.view_applications()
    captured = capsys.readouterr()
    assert "test_app" in captured.out
    assert "test_username" in captured.out
    assert "test_password" in captured.out

def test_password_data_control_interface(capsys, monkeypatch):
    pd = PasswordData({'filepath': './pass.crypt'})
    pd.__password_dict = {"test_app": {"username": "test_username", "password": "test_password"}}
    monkeypatch.setattr('builtins.input', lambda: 'q')
    control_interface(pd)
    captured = capsys.readouterr()
    assert "Password Manager" in captured.out


# These tests cover the following scenarios:
#
#
# 1. Initialization of the PasswordData class.
# 2. Encryption and decryption of files.
# 3. Initialization workflow of the PasswordData class.
# 4. Saving a file using the PasswordData class.
# 5. Viewing applications using the PasswordData class.
# 6. Control interface of the PasswordData class.
#
#
# Note that these tests are just a starting point and you may need to add more tests to cover all the scenarios.