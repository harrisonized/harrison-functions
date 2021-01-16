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

Example function:

```python
from harrison_functions.pandas.data import dict_to_col
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

This code is copyright by Harrison Wang in 2019. This code is for personal use ONLY. I deliberately chose not to include a license, and you certainly do NOT have permission to use it (if you somehow manage to get a copy of it in the first place)!