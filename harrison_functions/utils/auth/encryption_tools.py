import os
from cryptography.fernet import Fernet
from configparser import ConfigParser
from ..etc.paths import INI_KEY


# Functions included in this file:
# # generate_new_key
# # encrypt_message
# # decrypt_message


def generate_new_key(enc='utf-8'):
    """Returns the new key as a plaintext string
    Used to generate a unique INI_KEY that's stored as an environmental variable
    Shuffle INI_KEY on a regular basis
    """
    return Fernet.generate_key().decode(enc)


def encrypt_message(message: str, ini_key: str, enc='utf-8'):
    """Given a plaintext message,
    returns an encrypted plaintext string
    
    Use this to generate encrypted keys in the .ini file
    """
    return Fernet(ini_key).encrypt(str.encode(message, enc)).decode(enc)


def decrypt_message(message: str, ini_key: str, enc='utf-8'):
    """Given an encrypted message from a .ini file,
    returns the unencrypted plaintext string
    """
    return Fernet(ini_key).decrypt(str.encode(message, enc)).decode(enc)


def decrypt_single_key(section, key, cfg_path='config/cred.ini'):
    """Given an INI file with a ['postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'
    assert cfg.has_option(section, key), f'Missing key at {key}'

    return decrypt_message(cfg.get(section, key), INI_KEY)
