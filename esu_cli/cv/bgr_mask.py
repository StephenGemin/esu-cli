from pathlib import Path

import click
import cv2
import numpy as np

from esu_cli.cv import _processing
from esu_cli.cv import _params


@click.command(name="bgr_mask")
@_params.image_process_params
@click.option("--save-mask", is_flag=True, flag_value=True)
@click.argument("image_file", type=click.Path(exists=True, dir_okay=False))
def main(view_scale, save_result, save_mask, image_file):
    """
    Apply BGR mask to an image; Press q to terminate the loop
    Everything is ordered in BGR as that's the default way opencv reads images
    """
    img_path = Path(image_file)
    img = cv2.imread(image_file)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.namedWindow("trackbars")
    cv2.resizeWindow("trackbars", 640, 260)
    cv2.createTrackbar("b_min", "trackbars", 0, 255, _processing.empty_func)
    cv2.createTrackbar("b_max", "trackbars", 255, 255, _processing.empty_func)
    cv2.createTrackbar("g_min", "trackbars", 0, 255, _processing.empty_func)
    cv2.createTrackbar("g_max", "trackbars", 255, 255, _processing.empty_func)
    cv2.createTrackbar("r_min", "trackbars", 0, 255, _processing.empty_func)
    cv2.createTrackbar("r_max", "trackbars", 255, 255, _processing.empty_func)

    click.echo("Press q to exit")
    while True:
        b_min = cv2.getTrackbarPos("b_min", "trackbars")
        b_max = cv2.getTrackbarPos("b_max", "trackbars")
        g_min = cv2.getTrackbarPos("g_min", "trackbars")
        g_max = cv2.getTrackbarPos("g_max", "trackbars")
        r_min = cv2.getTrackbarPos("r_min", "trackbars")
        r_max = cv2.getTrackbarPos("r_max", "trackbars")

        lower = np.array([b_min, g_min, r_min])
        upper = np.array([b_max, g_max, r_max])
        mask = cv2.inRange(img, lower, upper)
        mask_result = cv2.bitwise_and(img, img, mask=mask)

        img_stack = _processing.stack_image([img, mask_result], scale=view_scale)

        if _processing.imshow_with_q_exit("Color Finder", img_stack):
            break

    click.secho(
        f"Color mask result:\n"
        f"r_min: {r_min}, r_max: {r_max}\n"
        f"g_min: {g_min}, g_max: {g_max}\n"
        f"b_min: {b_min}, b_max: {b_max}\n",
        color="green"
    )
    if save_result:
        _processing.save(img_path, "bgr_mask_result", mask_result)
    if save_mask:
        _processing.save(img_path, "hsv_mask", mask)


if __name__ == "__main__":
    main()
