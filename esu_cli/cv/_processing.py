import logging
from pathlib import Path
from typing import List, Union

import cv2
import numpy as np

logger = logging.getLogger(__name__)


# args is here to stop opencv from throwing missing argument error
# when trackbar loop values change
def empty_func(*args):
    pass


def imshow_with_q_exit(window, image):
    cv2.imshow(window, image)
    q = cv2.waitKey(1) & 0xFF
    if q == ord("q"):
        cv2.destroyAllWindows()
        return True
    return False


def _resize_reshape(image: np.ndarray, master: np.ndarray, scale: float) -> np.ndarray:
    kwargs = {}
    if scale is None or scale == 1 or scale < 0:
        kwargs.update(fx=1, fy=1)
        kwargs.update(interpolation=None)
    else:
        kwargs.update(fx=scale, fy=scale)
        if scale < 1:
            kwargs.update(interpolation=cv2.INTER_AREA)
        else:  # scale > 1
            kwargs.update(interpolation=cv2.INTER_CUBIC)

    if image.shape[:2] == master.shape[:2]:  # RGB
        image = cv2.resize(image, (0, 0), **kwargs)
    else:  # GRAY
        image = cv2.resize(image, (master.shape[1], master.shape[0]), **kwargs)
    if len(image.shape) == 2:  # ensure all images have the same shape
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image


def _is_tiled(image_array):
    return isinstance(image_array[0], list)


def stack_image(
    image_array: Union[List[np.ndarray], List[List[np.ndarray]]],
    *,
    scale: float = None,
) -> Union[List[np.ndarray], List[List[np.ndarray]]]:
    """
    Exampe inputs
    [[img1, img2], [img3, img4]]  # tiled symmetrical
    [img1, img2, img3, img4_]  # row

    :param image_array: single list or list of list of images
    :param scale: scale images up or down ... applies to both fx,fy.
        This value will be ignored if user passes fx, fy
    :return: stacked image output
    """
    rows = len(image_array)
    cols = len(image_array[0])

    if _is_tiled(image_array):
        master = image_array[0][0]
        for x in range(rows):
            for y in range(cols):
                image_array[x][y] = _resize_reshape(image_array[x][y], master, scale)
        image_blank = np.zeros((master.shape[1], master.shape[0], 3), dtype=np.int8)
        row = [image_blank] * rows
        for x in range(rows):
            row[x] = np.hstack(image_array[x])
        ver = np.vstack(row)
    else:  # single row
        for x in range(rows):
            image_array[x] = _resize_reshape(image_array[x], image_array[0], scale)
        ver = np.hstack(image_array)
    return ver


def save(img_path: Path, save_file_name: str, img_arr: np.ndarray):
    save_path = img_path.parents[0].joinpath(
        f"{img_path.stem}_{save_file_name}{img_path.suffix}"
    )
    cv2.imwrite(str(save_path), img_arr)
    logger.info(f"Save path: {save_path}")


# # Original function from YouTube.  Keeping it here just because
#  See https://www.youtube.com/watch?v=Wv0PSs0dmVI
# def stack_image(scale, imgArray):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range(0, rows):
#             for y in range(0, cols):
#                 if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:  # RGB
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (0,0), None, scale, scale)
#                 else:  # GRAY
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
#                 # ensure all images have the same shape
#                 if len(imgArray[x][y].shape) == 2:
#                     imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
#         imageBlank = np.zeros((height, width, 3), np.int8)
#         hor = [imageBlank] * rows
#         hor_con = [imageBlank] * rows
#         for x in range(rows):
#             hor[x] = np.hstack(imgArray[x])
#         ver = np.vstack(hor)
#     else:
#         for x in range(0, rows):
#             if imgArray[x].shape[:2] == imgArray[0].shape[:2]:  # RGB
#                 imgArray[x] = cv2.resize(imgArray[x], (0,0), None, scale, scale)
#             else:  # GRAY
#                 imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
#             if len(imgArray[x].shape) == 2:
#                 imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
#         hor = np.hstack(imgArray)
#         ver = hor
#     return ver
