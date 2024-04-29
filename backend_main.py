import cv2

from Table import *

if __name__ == '__main__':
    table = Table("Images/table8NoMap.jpg")
    rel_img = table.get_relations_on_image()
    title_window = "relations"
    cv2.namedWindow(title_window)
    cv2.imshow(title_window, rel_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


