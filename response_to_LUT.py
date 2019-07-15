import sys
from data_analisys_methods import *
import pandas as pd


if len(sys.argv)<2:
    print("Input file not specified")
    sys.exit(-1)

file_path = sys.argv[-1]
df = pd.read_csv(file_path, dtype=np.float64)
average = average_response(df.values)

print("', '".join([str(int(i)) for i in average]))
