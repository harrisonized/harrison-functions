import os
from configparser import ConfigParser


# Functions included in this file:
# # get_config_from_ini


def get_defaults_from_ini(section='default', cfg_path='conf/settings.ini'):
    """To be used with conf/settings.ini"""

    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'

    return cfg[section]
