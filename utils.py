
import cv2
import numpy as np
import time

def energy_map(Image):
    """Calculate the energy"""
    # Vertical and horizontal energy by gradient Sobel
    b, g, r = cv2.split(Image)
    bener = np.absolute(cv2.Sobel(b, -1, 1, 0)) + np.absolute(cv2.Sobel(b, -1, 0, 1))
    gener = np.absolute(cv2.Sobel(g, -1, 1, 0)) + np.absolute(cv2.Sobel(g, -1, 0, 1))
    rener = np.absolute(cv2.Sobel(r, -1, 1, 0)) + np.absolute(cv2.Sobel(r, -1, 0, 1))
    # somme of BGR
    return bener + gener + rener


def find_seam_enermap(energy):
    """dynamic planning for finding the seam"""
    hei, wid = energy.shape
    seam = np.zeros(energy.shape)
    for i in range(1, hei):
        for j in range(0, wid):
            if j == 0:
                minidx = np.argmin(energy[i - 1, j:j + 2]) + j
                energy[i, j] += int(energy[i - 1, minidx])
                seam[i, j] = minidx
            else:
                minidx = np.argmin(energy[i - 1, j - 1:j + 2]) + j - 1
                energy[i, j] += int(energy[i - 1, minidx])
                seam[i, j] = minidx
    # return the seam and energy
    return energy, seam


def delete_seam_pixel_col(Image, seam, Energy):
    hei, wid, _ = Image.shape
    out_col = np.zeros((hei, wid - 1, 3))
    j = np.argmin(Energy[-1])
    for i in range(hei - 1, 0, -1):
           out_col[i, :, 0] = np.delete(Image[i, :, 0], [j]) # each line deleted the minimal point on b
           out_col[i, :, 1] = np.delete(Image[i, :, 1], [j]) # each line deleted the minimal point on g
           out_col[i, :, 2] = np.delete(Image[i, :, 2], [j]) # each line deleted the minimal point on r
           j = int(seam[i][j])
    return out_col


def delete_seam_pixel_row(Image, seam, Energy):
    hei, wid, _ = Image.shape
    out_row = np.zeros((hei-1, wid, 3))
    i = np.argmin(Energy[-1])
    for j in range(wid-1, 0, -1):
            out_row[:, j, 0] = np.delete(Image[:, j, 0], [i])    # each column deleted the minimal point on b
            out_row[:, j, 1] = np.delete(Image[:, j, 1], [i])  # each column deleted the minimal point on g
            out_row[:, j, 2] = np.delete(Image[:, j, 2], [i])  # each column deleted the minimal point on r
            i = int(seam[i][j])
    return out_row


def seam_carving_hw(Image, wsmall, hsmall):
    t_st=time.time()
    for dh in range(wsmall):
        energy = energy_map(Image)
        Energy, seam = find_seam_enermap(energy)
        Image = delete_seam_pixel_col(Image, seam, Energy)
        print(wsmall - dh)
    for dw in range(hsmall):
        energy = energy_map(Image)
        Energy, seam = find_seam_enermap(energy)
        Image = delete_seam_pixel_row(Image, seam, Energy)
        print(hsmall - dw)
    t_end = time.time()
    print('durant time=',t_end-t_st,'s')
    return Image








