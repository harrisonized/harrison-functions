import numpy as np

# Functions
# # flatten_image_array
# # flat_image_to_array


def flatten_image_array(image_array: np.ndarray, n_colors=3, height=80, width=80):
    """Converts an image array in this format:
    array([[[ 92, 109,  90],
            [ 92, 108,  89],
            [ 91, 107,  88],
            ...,
            [ 96, 109,  93],
            [ 95, 109,  92],
            [ 93, 107,  91]],

           [[ 93, 108,  91],
            [ 91, 108,  88],
            [ 91, 108,  88],
            ...,
            [ 95, 109,  92],
            [ 95, 109,  92],
            [ 95, 109,  92]],

           ...,
           
           [[ 94, 106,  90],
            [ 91, 103,  87],
            [ 93, 105,  89],
            ...,
            [ 96, 111,  94],
            [ 94, 110,  93],
            [ 94, 110,  93]]], dtype=uint8)
           
    To this:
    [92, 92, 91, ..., 96, 95, 93,  # 0:80
     93, 91, 91, ..., 95, 95, 95,  # 80:160
     ...
     94, 91, 93, ..., 96, 94, 94,  # 6320:6400
     109, 108, 107, ..., 109, 109, 107,  # 6400:6480
     108, 108, 108, ..., 109, 109, 109,  # 6480:6560
     ...
     106, 103, 105, ..., 111, 110, 110,  # 12720:12800
     90, 89, 88, ..., 93, 92, 91,  # 12800:12880
     91, 88, 88, ..., 92, 92, 92,  # 12880:12960
     ...
     90, 87, 97..., 94, 93, 93]  # 19120:19200
     
    This was used in ships-in-satellite-imagery to store image data in json
    See: https://www.kaggle.com/rhammell/ships-in-satellite-imagery
    """
    return list(map(int, np.reshape(image_array.swapaxes(2, 1).swapaxes(1, 0), [n_colors*height*width])))
    
    
def flat_image_to_array(flat_image: list, n_colors=3, height=80, width=80):
    """The reverse operation of flatten_image_array().
    """
    return np.reshape(flat_image, [n_colors, height, width]).swapaxes(0, 1).swapaxes(1, 2).astype(np.uint8)
