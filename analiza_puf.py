import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from data_analisys_methods import *


def read_files():
    dfs = []
    for i in range(len(sys.argv) - 1):
        file_path = sys.argv[i + 1]
        df = pd.read_csv(file_path, dtype=np.float64)
        print(df.shape)
        dfs.append(df)

        print(file_path)

    return dfs


def main():
    data = read_files()

    #Overall PUF analysis
    uniqueness = compute_uniqueness(data)
    reliability = compute_reliability(data)
    print("Reliability: {}%".format(reliability))
    print("Uniqueness: {}%".format(uniqueness))

    sns.set_style('white')

    plt.figure(1)
    p1 = intra_dist_plot(data)

    plt.figure(2)
    p2 = inter_dist_plot(data)


    plt.show()




if __name__ == '__main__':
    main()