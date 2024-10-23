import cv2 as cv
import numpy as np


def get_rook_map(side="W"):

    s_map = [
        [30,  30,  20, 20,  20,  20,  30,  30],
        [40,  40,  40,  40, 40,  40,  40,  40],
        [-5,  -5,  -5,  -5,  -5,  -5,  -5,  -5],
        [5,  0,  0,  -5,  -5,  0,  0,  5],
        [5,  0,  0,  -5,  -5,  0,  0,  5],
        [10,  0,  0,  -5,  -5,  0,  0,  10],
        [0,  0,  0,  0,  0,  0,  0,  0],
        [30,  0,  0, 5,  5,  0,  0,  30],
    ]

    
    if side == "B":
        n = 8
        s_map = cv.flip(np.array(s_map), 0)
        final_map = [[0 for ii in range(n)] for jj in range(n)]
        for i in range(len(s_map)):
            for j in range(len(s_map)):
                final_map[i][j] = float(s_map[i][j]/255)
        s_map = final_map

    
    arr = np.array(s_map)
    # Find the minimum and maximum values
    min_val = np.min(arr)
    max_val = np.max(arr)
    # Normalize the array
    if max_val > min_val:
        normalized_array = (arr - min_val) / (max_val - min_val)
    else:
        normalized_array = arr/arr
    #print(normalized_array)
    #cv.imshow("Map", cv.resize(normalized_array, [500, 500], interpolation=0))
    #cv.waitKey(0)
    

    return s_map


if __name__ == "__main__":
    get_rook_map()