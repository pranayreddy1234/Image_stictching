
import cv2
import numpy as np
import random

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(left_img,None)
    kp2, des2 = sift.detectAndCompute(right_img,None)

    good_matches = {}
    good_matches_distance = {}
    required_matches = {}
    for i in range(len(kp1)):
        x = np.tile(des1[i, : ], (len(des2), 1))
        distance = np.sqrt(np.sum(np.square(x - des2), axis = 1))
        A, B = np.argpartition(distance, 1)[0:2]
        #minimum_index = np.argmin(distance)
        if distance[A] < distance[B]:
            good_matches.update({kp1[i]:[kp2[A],kp2[B]]})
            good_matches_distance.update({kp1[i] : [distance[A],distance[B]]})
        else:
            good_matches.update({kp1[i]:[kp2[B],kp2[A]]})
            good_matches_distance.update({kp1[i] : [distance[B],distance[A]]})

    for i in range(len(kp1)):
        if good_matches_distance[kp1[i]][0] < 0.5*good_matches_distance[kp1[i]][1]:
            required_matches.update({kp1[i] : good_matches[kp1[i]][0]})

    required_kp1= list(required_matches.keys())[:200]


    points1 = np.zeros((len(required_kp1), 2), dtype=np.float32)
    points2 = np.zeros((len(required_kp1), 2), dtype=np.float32)

    for i in range(len(required_kp1)):
        try:
            points1[i, :] = required_kp1[i].pt
            points2[i, :] = required_matches[required_kp1[i]].pt
        except IndexError:
            pass 

    h, mask = cv2.findHomography(points2, points1, cv2.RANSAC, 10.0) 

    height, width, channels = left_img.shape

    right_image_warp = cv2.warpPerspective(right_img, h, (2418, left_img.shape[0]), flags=cv2.INTER_LINEAR)
    right_image_warp[0:left_img.shape[0],0:left_img.shape[1]] = left_img
    return right_image_warp
    raise NotImplementedError

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task1_result.jpg',result_image)


