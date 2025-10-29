import os
import cv2
import numpy as np
mask_dir = "/liuxianguo2/linshuo/GART/data/taichi_red_mask"

for pic_name in os.listdir(mask_dir):
    mask_path = mask_dir + "/" + pic_name
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    _, binary_mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
    inverted_mask = cv2.bitwise_not(binary_mask)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(inverted_mask, connectivity=8)
    min_size_threshold = 10000
    filtered_mask = np.zeros_like(binary_mask)
    for j in range(1, num_labels):
        area = stats[j, cv2.CC_STAT_AREA]
        if area >= min_size_threshold:
            filtered_mask[labels == j] = 255

    deal_mask_path = mask_dir + "_deal/" + pic_name.split(".")[0].split("_")[1][1:] + "." +pic_name.split(".")[1]
    # deal_mask_path = mask_dir + "_deal/" + pic_name.split(".")[0] + "_deal." + pic_name.split(".")[1]
    # end_mask = cv2.bitwise_not(filtered_mask)
    cv2.imwrite(deal_mask_path, filtered_mask)
    print("已处理 "+mask_path)