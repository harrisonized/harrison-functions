"""imports queries from the queries folder
>>> from harrison_functions.etc.queries import queries
>>> from harrison_functions.etc.queries import SELECT_ALL_LIMIT_5
"""
from os.path import abspath, sep
from harrison_functions.utils.file_io import dirname_n_times, read_folder_as_dict

root_dir = dirname_n_times(abspath(__file__), 4)

# load queries
query_dict = read_folder_as_dict(
    dirpath=f"{root_dir}{sep}queries{sep}",
    ext='.sql',
)

# add queries folder to the namespace
globals()['queries'] = query_dict

# also add any subfolders to the namespace
for subdir, query_subdict in query_dict.items():
	if subdir in globals():
		subdir = f'{subdir}_'  # append an underscore if overlapping name
	globals()[subdir] = query_subdict
