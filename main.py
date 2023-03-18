
import utils

import argparse as arg
import cv2

def main():

    parser = arg.ArgumentParser(description='Describe your script here')
    parser.add_argument("-r", "--row", help="the size of row", type=int)
    parser.add_argument("-c", "--column", help="the size of column", type=int)
    parser.add_argument("-hei", "--height", help="the size of seam carving adjusted of row", type=int)
    parser.add_argument("-wid", "--width", help="the size of seam carving ajusted of column", type=int)
    args = parser.parse_args()

    img = cv2.imread('Pierce.jpg')
    img=cv2.resize(img,(args.row,args.column),interpolation=cv2.INTER_AREA)
    energy = utils.energy_map(img)
    print(img.shape[1])
    vari_h=args.row-args.height
    vari_w=args.column-args.width
    Image=utils.seam_carving_hw(img,vari_h,vari_w)

    cv2.imwrite("Image original1.jpg", img)

    cv2.imwrite("Energy1.jpg", energy)
    cv2.imwrite("Seam Carving1.jpg",Image)


if __name__ == "__main__":
	  main()

