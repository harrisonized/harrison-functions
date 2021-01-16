import os

# Functions included in this file:
# # create_nested_folder


def create_nested_folder(current_dir, new_dir):
    """Example:
    current_dir = data/folder_1/folder_2
    new_dir = folder_3/folder_4

    Output: data/folder_1/folder_2/folder_3/folder_4
    """
    new_folder_list = new_dir.strip('/').split('/')
    for new_folder in new_folder_list:
        new_dir = f'{current_dir}/{new_folder}'
        try:
            os.mkdir(new_dir)
        except:
            pass
        current_dir=new_dir
