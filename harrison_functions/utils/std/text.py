import re

# Functions
# # title_to_snake_case
# # title_case_to_initials
# # camel_to_snake_case
# # snake_to_pascal_case
# # pascal_to_title_case
# # snake_to_title_case
# # word_wrap
# # add_space_to_prefixes
# # compute_average_bin


def title_to_snake_case(text):
    """Converts "Column Title" to column_title
    """
    return text.lower().replace(' ', '_').replace('-', '_')


def title_case_to_initials(text):
    """Converts "Column Title" to CT
    """
    return ''.join([word[0].upper() for word in text.split()])


def camel_to_snake_case(text):
    """Converts columnTitle to column_title
    Source: Geeks For Geeks
    """
    split_First = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    all_lower_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', split_First).lower()
    return all_lower_case


def snake_to_pascal_case(text):
    """Converts column_title to ColumnTitle
    """
    return ''.join(map(lambda x: x.capitalize(), text.split('_')))


def pascal_to_title_case(text):
    """Converts ColumnTitle to "Column Title"
    Source: Geeks For Geeks
    """
    return ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', text))


def snake_to_title_case(text):
    """Converts column_title to "Column Title"
    """
    return ' '.join(map(lambda x: x.capitalize(), text.split('_')))


def word_wrap(string, n):
    string_list = string.split()
    parsed_list = [string_list[n * i:n * (i + 1)] for i in range((len(string_list) + n - 1) // n)]
    joined_string_list = [' '.join(parsed_list[i]) for i in range(len(parsed_list))]
    final_list = ['<br>'.join(joined_string_list)]
    return final_list[0]


def add_space_to_prefixes(text, prefixes: list):
    prefix_regex = '('+'|'.join(prefixes)+')'
    return re.sub(prefix_regex, r'\1 ', text)


def compute_average_bin(categorical, mode='mean'):
    """Helper function for plot_multiple_scatter and plot_violin
    Takes a str object like '[0, 25)' and returns the average
    """

    lower = float(re.match(r"([\[\(])(?P<lower>[0-9.]+), (?P<upper>[0-9.]+)([\)\]])", categorical).group('lower'))
    upper = float(re.match(r"([\[\(])(?P<lower>[0-9.]+), (?P<upper>[0-9.]+)([\)\]])", categorical).group('upper'))

    if mode == 'mean':
        return (lower + upper) / 2

    if mode == 'lower':
        return lower

    if mode == 'upper':
        return upper
