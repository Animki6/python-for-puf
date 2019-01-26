import sys
import pandas as pd
import matplotlib.pyplot as plt

file_path = sys.argv[1]


df = pd.read_csv(file_path)

print(df.shape)

#df = df.drop([1,3,5])

df_mean = df.mean(axis=0)

#print(df_mean)
num_of_error_bits = sum(1 for i in df_mean if i not in (0.0, 1.0))
print(num_of_error_bits)
print(str((num_of_error_bits/len(df_mean))*100)+'%')

labels = list(df)
labels = labels[0:len(labels):100]

plt.plot(range(len(df_mean)), df_mean, 'o')
plt.xticks(range(0,len(df_mean), 100), labels, rotation='vertical')
plt.show()


