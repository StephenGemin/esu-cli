from pathlib import Path

import click
import cv2

from esu_cli.cv import _processing
from esu_cli.cv import _params


@click.command(name="thresh")
@_params.image_process_params
@click.argument("image_file", type=click.Path(exists=True, dir_okay=False))
def main(view_scale, save_result, image_file):
    """
    Threshold viewer; Press q to terminate the loop
    """
    img_path = Path(image_file)
    img = cv2.imread(image_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow("trackbars")
    cv2.resizeWindow("trackbars", 640, 260)
    cv2.createTrackbar("min_thresh", "trackbars", 0, 255, _processing.empty_func)
    cv2.createTrackbar("max_thresh", "trackbars", 255, 255, _processing.empty_func)

    click.echo("Press q to exit")
    while True:
        min_thresh = cv2.getTrackbarPos("min_thresh", "trackbars")
        max_thresh = cv2.getTrackbarPos("max_thresh", "trackbars")

        _, img_thresh = cv2.threshold(
            img_gray, min_thresh, max_thresh, cv2.THRESH_BINARY
        )

        img_stack = _processing.stack_image([img_thresh], scale=view_scale)
        if _processing.imshow_with_q_exit("Thresh Finder", img_stack):
            break

    click.secho(f"Threshold viewer result:\n" f"min: {min_thresh}, max: {max_thresh}\n", color="green")
    if save_result:
        _processing.save(img_path, "thresh_result", img_thresh)


if __name__ == "__main__":
    main()

