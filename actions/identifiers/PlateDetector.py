import math
import cv2
import numpy as np
import matplotlib.pyplot as plt


class PlateDetector(object):
    def __init__(self) -> None:
        pass

    def detect_plates(
        image_path,
        min_area=1800,
        scale_by=0.5,
        threshold=172,
        canny_upper=150,
        canny_lower=50,
        circularity_c=0.75,
        show=False,
    ):
        # preprocess
        image = cv2.imread(image_path)
        image = cv2.resize(image, (0, 0), fx=scale_by, fy=scale_by)
        orig = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 1)
        if threshold != 0:
            _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_TOZERO)
        else:
            thresh = blur
        can = cv2.Canny(thresh, canny_upper, canny_lower)  # TODO: pay attention here!
        kernel = np.ones((3, 3), np.uint8)
        can = cv2.dilate(can, kernel, iterations=1)
        can = cv2.morphologyEx(can, cv2.MORPH_CLOSE, kernel)

        # find the contours
        contours, hierarchy = cv2.findContours(
            can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        found_plates = []
        found = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)

            # print(area)
            if area > min_area:
                # cv2.drawContours(orig, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objCor = len(approx)
                x, y, width, height = cv2.boundingRect(approx)
                circularity = (4 * math.pi * area) / (peri**2)
                if objCor > 5 and circularity > circularity_c:
                    cx, cy = x + (width // 2), y + (height // 2)
                    found_plates.append(
                        {
                            "cnt": cnt,
                            "area": area,
                            "bbox": [x, y, width, height],
                            "center": [cx, cy],
                            "circularity": circularity,
                        }
                    )
                    found += 1

                    if show:
                        cv2.rectangle(
                            orig, (x, y), (x + width, y + height), (0, 255, 0), 2
                        )
                        cv2.circle(
                            orig,
                            (x + (width // 2), y + (height // 2)),
                            5,
                            (255, 0, 255),
                            cv2.FILLED,
                        )
                        cv2.putText(
                            orig,
                            f"{found} ({cx},{cy})",
                            (cx - 10, cy - 10),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.7,
                            (0, 0, 0),
                            2,
                        )
        if show:
            img_cont = image.copy()
            cv2.drawContours(img_cont, contours, -1, (0, 255, 0), 2)
            # _, axes = plt.subplots(1, 4, figsize=(20, 20))
            # for ax, img, title in zip(
            #     axes.flatten(),
            #     [thresh, can, img_cont[:, :, ::-1], orig[:, :, ::-1]],
            #     ["threshold", "canny", "contours", "detector"],
            # ):
            #     ax.imshow(img, cmap="gray")
            #     ax.set_title(title)
            # return orig
            plt.figure(figsize=(12, 16))
            plt.imshow(orig[:, :, ::-1], aspect="equal")
        return found_plates
        # return sorted(found_plates, key=lambda x: x["area"], reverse=True)
