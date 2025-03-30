import pytest
from passwordManager import PasswordData
from utility import InputStyle, decrypt_file, encrypt_file

sample_password_dict = {
    'gmail': {'username': 'admin1234', 'password': 'password1234'},
    'facebook': {'username': 'test1234', 'password': 'password1234'}
}


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
    data = "test_data1234567896!@#$%^&*()"
    encrypt_file(password, str(file_path), data)
    decrypted_data = decrypt_file(password, str(file_path))

    assert decrypted_data == data


def test_password_data_initialization_workflow_no_file(tmp_path, monkeypatch):
    pd = PasswordData({'filepath': str(tmp_path / "test_file")})
    monkeypatch.setattr('getpass.getpass', lambda _: 'test_password')
    pd.initialization_work_flow()
    assert pd._PasswordData__master_password == 'test_password'


def test_set_password(tmp_path, monkeypatch):
    pass


def test_validate_password(tmp_path):
    pass
