from pathlib import Path

import click
import cv2
import numpy as np

from esu_cli.cv import _processing
from esu_cli.cv import _params


@click.command(name="hsv_mask")
@_params.image_process_params
@click.option("--save-mask", is_flag=True, flag_value=True)
@click.argument("image_file", type=click.Path(exists=True, dir_okay=False))
def main(view_scale, save_result, save_mask, image_file):
    """
    Apply HSV mask to an image; Press q to terminate the loop
    """
    img_path = Path(image_file)
    img = cv2.imread(image_file)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.namedWindow("trackbars")
    cv2.resizeWindow("trackbars", 640, 260)
    cv2.createTrackbar("hue_min", "trackbars", 0, 255, _processing.empty_func)
    cv2.createTrackbar("hue_max", "trackbars", 255, 255, _processing.empty_func)
    cv2.createTrackbar("sat_min", "trackbars", 0, 255, _processing.empty_func)
    cv2.createTrackbar("sat_max", "trackbars", 255, 255, _processing.empty_func)
    cv2.createTrackbar("val_min", "trackbars", 0, 255, _processing.empty_func)
    cv2.createTrackbar("val_max", "trackbars", 255, 255, _processing.empty_func)

    click.echo("Press q to exit")
    while True:
        hue_min = cv2.getTrackbarPos("hue_min", "trackbars")
        hue_max = cv2.getTrackbarPos("hue_max", "trackbars")
        sat_min = cv2.getTrackbarPos("sat_min", "trackbars")
        sat_max = cv2.getTrackbarPos("sat_max", "trackbars")
        val_min = cv2.getTrackbarPos("val_min", "trackbars")
        val_max = cv2.getTrackbarPos("val_max", "trackbars")

        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])
        mask = cv2.inRange(img_hsv, lower, upper)
        mask_result = cv2.bitwise_and(img, img, mask=mask)

        img_stack = _processing.stack_image(
            [[img, img_hsv], [mask, mask_result]], scale=view_scale
        )
        if _processing.imshow_with_q_exit("HSV Finder", img_stack):
            break

    click.secho(
        f"HSV mask result:\n"
        f"hue_min: {hue_min}, hue_max: {hue_max}\n"
        f"sat_min: {sat_min}, sat_max: {sat_max}\n"
        f"val_min: {val_min}, val_max: {val_max}\n",
        color="green",
    )
    if save_result:
        _processing.save(img_path, "hsv_mask_result", mask_result)
    if save_mask:
        _processing.save(img_path, "hsv_mask", mask)


if __name__ == "__main__":
    main()
