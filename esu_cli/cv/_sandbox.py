"""This is here strictly for debugging and sandbox purposes"""
import cv2
import numpy as np


draw_text_kwargs = {
    "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
    "fontScale": 0.5,
    "color": (255, 0, 0),
    "thickness": 2,
}

# draw_text_kwargs = {
#     "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
#     "fontScale": 0.5,
#     "color": (255, 0, 0),
#     "thickness": 2,
# }
#
#
# def filter_duplicate_poly_lines(approx_poly: np.ndarray, threshold: int) -> np.ndarray:
#     """
#     Sometimes cv2.approxPolyDP will return lines that are very similar,
#     but are still treated as separate boundary lines
#     Ex. (137, 211), (138, 211), (137, 213)
#
#     :param approx_poly: numpy array
#     :param threshold: int threshold pixel limit
#         If an x,y line boundary difference are both within the threshold,
#         that line boundary is removed
#     """
#     ret = approx_poly.copy()
#     ret = np.squeeze(ret, axis=1)
#     for i, v1 in enumerate(ret):
#         for j, v2 in enumerate(ret[i+1:], i+1):
#             x_compare = abs(v2[0] - v1[0]) < threshold
#             y_compare = abs(v2[1] - v1[1]) < threshold
#             if x_compare and y_compare:
#                 ret[j] = [-1, -1]
#     ret = ret[~np.all(ret == -1, axis=1)]
#     ret = np.expand_dims(ret, axis=1)
#     return ret
#
#
# def get_contours(contour_source, draw_on_img):
#     contours, _ = cv2.findContours(
#         contour_source, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
#     )
#     for ind, ct in enumerate(contours):
#         if ind == 86:
#             cv2.drawContours(draw_on_img, ct, -1, (255, 0, 0), thickness=2)
#         peri = cv2.arcLength(ct, True)
#         approx = cv2.approxPolyDP(ct, 0.01*peri, True)
#         filtered_approx = filter_duplicate_poly_lines(approx, 3)
#         corners = len(filtered_approx)
#
#         if ind == 86:
#             for c in filtered_approx:
#                 c = np.squeeze(c, axis=0)
#                 cv2.circle(draw_on_img, tuple(c), 1, (0, 255, 0), thickness=-1)
#
#         x, y, w, h = cv2.boundingRect(filtered_approx)
#         # if corners == 4:
#         #     if h == w:
#         #         shape = "square"
#         #     else:
#         #         shape="rectangle"
#         # else:
#         #     shape = "unknown"
#         # click.secho(f"Index: {ind}, shape: {shape}")
#         # if shape != "unknown":
#         #     cv2.putText(
#         #         draw_on_img,
#         #         f"{ind}: {shape}",
#         #         (x, y + h + 10),
#         #         **draw_text_kwargs
#         #
#         #     )
#         if ind == 86:
#             cv2.imshow(f"Index: {ind}", draw_on_img)
#             q = cv2.waitKey(0) & 0xFF
#             if q == ord("q"):
#                 cv2.destroyAllWindows()


def filter_duplicate_poly_lines(approx_poly: np.ndarray, threshold: int) -> np.ndarray:
    """
    Sometimes cv2.approxPolyDP will return lines that are very similar,
    but are still treated as separate boundary lines
    Ex. (137, 211), (138, 211), (137, 213)

    :param approx_poly: numpy array
    :param threshold: int threshold pixel limit
        If an x,y line boundary difference are both within the threshold,
        that line boundary is removed
    """
    ret = approx_poly.copy()
    ret = np.squeeze(ret, axis=1)
    for i, v1 in enumerate(ret):
        for j, v2 in enumerate(ret[i + 1 :], i + 1):
            x_compare = abs(v2[0] - v1[0]) < threshold
            y_compare = abs(v2[1] - v1[1]) < threshold
            if x_compare and y_compare:
                ret[j] = [-1, -1]
    ret = ret[~np.all(ret == -1, axis=1)]
    ret = np.expand_dims(ret, axis=1)
    return ret


def get_contours(contour_source, draw_on_img):
    contours, _ = cv2.findContours(
        contour_source, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    filtered_contours = []
    for ind, ct in enumerate(contours):
        cv2.drawContours(draw_on_img, ct, -1, (255, 0, 0), thickness=2)
        peri = cv2.arcLength(ct, True)
        approx = cv2.approxPolyDP(ct, 0.01 * peri, True)
        filtered_approx = filter_duplicate_poly_lines(approx, 3)
        filtered_contours.append(filtered_approx)
        corners = len(filtered_approx)

        for c in filtered_approx:
            c = np.squeeze(c, axis=0)
            cv2.circle(draw_on_img, tuple(c), 1, (0, 255, 0), thickness=-1)

        x, y, w, h = cv2.boundingRect(filtered_approx)
        print(x, y, w, h)
        # if corners == 4:
        #     if h == w:
        #         shape = "square"
        #     else:
        #         shape="rectangle"
        # else:
        #     shape = "unknown"
        # click.secho(f"Index: {ind}, shape: {shape}")
        # if shape != "unknown":
        #     cv2.putText(
        #         draw_on_img,
        #         f"{ind}: {shape}",
        #         (x, y + h + 10),
        #         **draw_text_kwargs
        #
        #     )
        # cv2.imshow(f"Index: {ind}", draw_on_img)
        # q = cv2.waitKey(0) & 0xFF
        # if q == ord("q"):
        #     cv2.destroyAllWindows()
    return filtered_contours


def other():
    pass
    # img_blur = cv2.GaussianBlur(mask2, (13, 13), 1)
    # # cv2.imshow("blurred", img_blur)
    # img_canny = cv2.Canny(img_blur, 5, 15)
    # cv2.imshow("canny", img_canny)

    # cv2.imshow("mask2 vs blur", cv2.bitwise_not(mask2, mask2, mask=img_blur))

    # img_contour = img.copy()
    # get_contours(img_canny, img_contour)
    # # cv2.imshow("contour", img_contour)
    # # q = cv2.waitKey(0) & 0xFF
    # # if q == ord("q"):
    # #     cv2.destroyAllWindows()
    # #     return

    # cv2.imshow("original", img)
    # cv2.imshow("HSV", img_hsv)
    # cv2.imshow("mask", mask)
    # cv2.imshow("mask_result", mask_result)
    # cv2.imshow("Color Finder", img_stack)
    #
    # lower2 = np.array([0, 0, 37])
    # upper2 = np.array([179, 107, 255])
    # mask2 = cv2.inRange(img_hsv, lower2, upper2)
    # masked_file = r""
    #
    #
    # img_blur = cv2.GaussianBlur(mask2, (13, 13), 1)
    # # cv2.imshow("blurred", img_blur)
    # img_canny = cv2.Canny(img_blur, 8, 10)
    # cv2.imshow("canny", img_canny)
    #
    # # cv2.imshow("mask2 vs blur", cv2.bitwise_not(mask2, mask2, mask=img_blur))
    #
    # img_contour = img_canny.copy()
    # get_contours(img_canny, img_contour)
    # cv2.imshow("contour", img_contour)
    #
    # # cv2.imshow("mask2", mask2)
    # # cv2.imwrite(r"", mask2)
    # # break


def show(img):
    cv2.imshow("temp", img)
    q = cv2.waitKey(0) & 0xFF
    if q == ord("q"):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    t = cv2.imread("")
    lower = np.array([48, 44, 42])
    upper = np.array([56, 52, 50])
    mask = cv2.inRange(t, lower, upper)
    mask_result = cv2.bitwise_and(t, t, mask=mask)
    masked_file = ""
    # cv2.imwrite(masked_file, mask_result)

    # from color picker
    # hue=147 sat=15 lum=46
    # red=46 green=48 blue=52

    img = cv2.imread(masked_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_blur = cv2.GaussianBlur(img, (13, 13), 1)
    img_canny = cv2.Canny(img_gray, 146, 200)
    img_copy = img.copy()
    contours = get_contours(img_canny, img_copy)

    width = 1300
    height = 143
    pixel_tolerance = 5

    color = [52, 48, 46]
    color_tolerance = 2
    color_min = [c - color_tolerance for c in color]
    color_max = [c + color_tolerance for c in color]
    img_color_range = cv2.inRange(img, np.array(color_min), np.array(color_max))

    for ind, c in enumerate(contours):
        c = np.squeeze(c, axis=1)
        x, y, w, h = cv2.boundingRect(c)
        if w in range(width - pixel_tolerance, width + pixel_tolerance) and h in range(
            height - pixel_tolerance, height + pixel_tolerance
        ):
            # if 1290<w < 1310 and 130<h < 150:
            print(f"match found, index {ind}")
        c_x, c_y = int(x + w / 2), int(y + h / 2)

        if img_color_range[c_y][c_x] > 0:
            print(f"color match found, index {ind}")
