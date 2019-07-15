import sys
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_name = sys.argv[1]

df = pd.read_csv(file_name)

df_mean = df.mean(axis=0)

compare_matrix = -1 * np.ones((128, 128))
print(compare_matrix.shape) 
index = 0
for i in range(128):
    for j in range(i+1, 128):
        compare_matrix[i, j] = df_mean[index]
        index = index + 1

plt.imshow(compare_matrix)
plt.colorbar()
plt.show()
