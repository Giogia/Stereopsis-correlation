import numpy as np
import cv2
import glob
import sys
from camera_calibration import *


def stereo_calibration(left_image, right_image):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    object_p = np.zeros((6 * 7, 3), np.float32)
    object_p[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    object_points = []  # 3d point in real world space
    left_image_points = []  # 2d points in image plane.
    right_image_points = []  # 2d points in image plane.

    left_calibration_images = glob.glob('calibration/left*.jpg')
    right_calibration_images = glob.glob('calibration/right*.jpg')

    # Images should be perfect pairs. Otherwise all the calibration will be false.
    # Be sure that first cam and second cam images are correctly prefixed and numbers are ordered as pairs.
    # Sort will fix the globs to make sure.
    left_calibration_images.sort()
    right_calibration_images.sort()

    # Pairs should be same size. Otherwise we have sync problem.
    if len(left_calibration_images) != len(right_calibration_images):
        print("Numbers of left and right images are not equal. They should be pairs.")
        print("Left images count: ", len(left_calibration_images))
        print("Right images count: ", len(right_calibration_images))
        sys.exit(-1)

    pair_images = zip(left_calibration_images, right_calibration_images)  # Pair the images for single loop handling

    # Iterate through the pairs and find chessboard corners. Add them to arrays
    # If openCV can't find the corners in one image, we discard the pair.
    for left_calibration_img, right_calibration_img in pair_images:

        # Left Object Points
        left = cv2.imread(left_calibration_img)
        gray_left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_left, corners_left = cv2.findChessboardCorners(gray_left, (7, 6),

                                                           cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS)
        # Right Object Points
        right = cv2.imread(right_calibration_img)
        gray_right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_right, corners_right = cv2.findChessboardCorners(gray_right, (7, 6),
                                                             cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS)

        if ret_left and ret_right:  # If both image is okay. Otherwise we explain which pair has a problem and continue
            # Object points
            object_points.append(object_p)

            # Left points
            corners2_left = cv2.cornerSubPix(gray_left, corners_left, (5, 5), (-1, -1), criteria)
            left_image_points.append(corners2_left)

            # Right points
            corners2_right = cv2.cornerSubPix(gray_right, corners_right, (5, 5), (-1, -1), criteria)
            right_image_points.append(corners2_right)

            # Draw and display the corners
            left_calibration_img = cv2.drawChessboardCorners(left_calibration_img, (7, 6), corners2_left, ret_left)
            right_calibration_img = cv2.drawChessboardCorners(right_calibration_img, (7, 6), corners2_right, ret_right)

            cv2.imshow('calibration images', left_calibration_img, right_calibration_img)
            cv2.waitKey(500)

        else:
            print("Chessboard couldn't detected. Image pair: ", left_calibration_img, " and ", right_calibration_img)
            continue

        cv2.destroyAllWindows()

        flag = 0
        # flag |= cv2.CALIB_FIX_INTRINSIC
        flag |= cv2.CALIB_USE_INTRINSIC_GUESS

        k1, d1 = calibrate_camera(left)
        k2, d2 = calibrate_camera(right)

        ret, k1, d1, k2, d2, r, t, e, f = cv2.stereoCalibrate(object_points, left_image_points, right_image_points, k1, d1, k2, d2, None)

        print("Stereo calibration rms: ", ret)
        r1, r2, p1, p2, q, roi_left, roi_right = cv2.stereoRectify(k1, d1, k2, d2, None, r, t,
                                                                   flags=cv2.CALIB_ZERO_DISPARITY, alpha=0.9)

        height, width = left_image.shape[:2]

        left_map_x, left_map_y = cv2.initUndistortRectifyMap(k1, d1, r1, p1, (width, height), cv2.CV_32FC1)
        left_image_rectified = cv2.remap(left_image, left_map_x, left_map_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

        right_map_x, right_map_y = cv2.initUndistortRectifyMap(k2, d2, r2, p2, (width, height), cv2.CV_32FC1)
        right_image_rectified = cv2.remap(right_image, right_map_x, right_map_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

        return left_image_rectified, right_image_rectified
    