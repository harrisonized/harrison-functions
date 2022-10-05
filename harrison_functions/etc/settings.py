from .paths import settings_cfg_path
from ..utils.file_io import read_section_from_ini

default_settings = read_section_from_ini(settings_cfg_path)
export_fig = default_settings.getboolean('export_fig')
show_traceback = default_settings.getboolean('show_traceback')
