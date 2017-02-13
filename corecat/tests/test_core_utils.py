# -*- coding: utf-8 -*-

import pytest
from Crypto.Cipher.AES import block_size as AES_block_size
from Crypto import Random
from corecat import utils


def test_encrypt_password():
    """Test password encrypting and checking function."""

    password = 'some_thing_nice_to !see'

    hashed_password = utils.encrypt_password(password)
    assert hashed_password
    assert hashed_password != password

    assert utils.check_password(hashed_password, password)
    assert not utils.check_password(hashed_password, 'inj3ct   ')
    assert not utils.check_password(hashed_password, '')

    hashed_empty_password = utils.encrypt_password('')
    assert hashed_empty_password
    assert hashed_empty_password != password

    for password in (None, True):
        with pytest.raises(TypeError) as exec_info:
            utils.encrypt_password(password)
        assert "Password should be a string!" in str(exec_info)


def test_aes_helpers():
    """Check AES helper functions."""

    keys_list = [
        'A9ll j',
        '0123-0123-0123-0123-0123-0123-01',
        '0123-0123-0123-0123-0123-0123-0123',
        list('moo')
    ]
    raw_lists = [
        '', '012 aj/', '01234567890123',
        '0123456789abcdef', '0123456789abcdef=Z0/?'
    ]

    # Valid
    for key in keys_list:
        assert len(utils.aes_key_pad(key)) == 32

    # Should not be empty string
    with pytest.raises(ValueError) as except_info:
        utils.aes_key_pad('')
    assert 'Key should not be empty!' in str(except_info.value)

    # Valid
    for raw in raw_lists:
        padded_raw = utils.aes_raw_pad(raw)
        assert len(padded_raw) % AES_block_size == 0
        assert raw in padded_raw

    with pytest.raises(TypeError) as except_info:
        utils.aes_raw_pad({'a': 'ops'})
    assert 'Context should be a string!' in str(except_info.value)

    with pytest.raises(ValueError) as except_info:
        raw = Random.new().read(1000)
        utils.aes_raw_pad(raw)
    assert 'Encrypt context was too long (>999).' in str(except_info.value)

    assert utils.aes_raw_unpad(
        utils.aes_raw_pad("12K la0'V")
    ) == "12K la0'V"


def test_aes_password_encrypt_decrypt():
    """Check AES crypto functions."""

    key = '3ncr9p7 K3Y'
    valid_passwords = [
        'h3r3 the passw0rD',
        '01234567890123'
    ]
    db_password_utf8 = u'trời ơi!'

    for password in valid_passwords:
        encrypted_config = utils.aes_encrypt(
            password,
            key
        )
        assert encrypted_config

        assert utils.aes_decrypt(
            encrypted_config,
            key
        ) == password

    assert utils.aes_decrypt(
        utils.aes_encrypt(
            db_password_utf8,
            key
        ),
        key
    ) == db_password_utf8

    with pytest.raises(TypeError) as except_info:
        assert utils.aes_encrypt(None, key)
    assert 'Context should be a string!' \
        in str(except_info.value)


def test_is_valid_format_email():
    """Test is_valid_format_email function."""

    valid_emails = [
        'test@test.test',
        'so.long.i.dont.care.test@te.te.te',
        'iAmS0lesS_wAnNa@B3aUt1.Fu1.lol'
    ]
    invalid_emails = [
        'invalid email bleh bleh',
        'user@mail',
        'usermail@',
        '@usermail',
        'user@mail.',
        'user@.mail',
        'user.mail@domain',
        'user.@mail',
        '.user@mail'
    ]
    for email in valid_emails:
        assert utils.is_valid_format_email(email)
    for email in invalid_emails:
        assert not utils.is_valid_format_email(email)
    with pytest.raises(TypeError):
        utils.is_valid_format_email(list)
