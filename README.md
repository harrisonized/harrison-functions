## Installation

Using conda:

```bash
conda activate <env>
conda develop ~/github/harrison-functions
```

Using pip method 1 (preferred):

```bash
conda activate <env>
cd github/harrison-functions
python setup.py develop
```

Using pip method 2:

```bash
conda activate <env>
pip install -e github/harrison-functions
```



## Getting Started

Try importing a function:

```python
from harrison_functions.utils.file_io import read_ini_as_dict
```

To use the files in the configs folder:

1. Put an INI_KEY in your bashrc.
2. Use the output of the `encrypt_message ` function in `harrison_functions.utils.std.encryption` to replace the fields in `configs/databases.ini`.

To read the queries in the queries folder as a dictionary:

```python
from harrison_functions.etc.queries import queries
```



## Uninstalling

Using conda:

```bash
conda develop -u ~/github/harrison-function  # to uninstall
```

Using pip:

```bash
pip uninstall harrison-functions
```



## Copyright

This code is copyright by Harrison Wang in 2019. This code is for personal use ONLY, not for distribution or profit.