import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = None
for i in range(len(sys.argv)-1):
    file_path = sys.argv[i+1]
    if df is None:
        df = pd.read_csv(file_path)
    else:
        df = df.append(pd.read_csv(file_path), ignore_index=True)
    print(df.shape)
    print(file_path)

print(df.shape)

#df = df.iloc[:, :127]

print(df.shape)
df_mean = df.mean(axis=0)
df_std = df.std(axis=0)
print('Max standard deviation: {}'.format(max(df_std)))
num_of_error_bits = sum(1 for i in df_mean if i not in (0.0, 1.0)) # Hamming Distance!
list_of_error_bits = [i for i, x in enumerate(df_mean) if x not in (0.0, 1.0)]
print(list_of_error_bits)
print(num_of_error_bits)
print(str((num_of_error_bits/len(df_mean))*100)+'%')

suma = 0
for i in range(df.shape[0]):
    suma += (sum(1 for j in range(df.shape[1]) if df_mean[j] != df.iloc[i, j])/df.shape[1])*100

IC = suma/df.shape[0]
print('ID : {}%'.format(IC))
labels = list(df)
labels = labels[0:len(labels):100]

plt.figure(1)
plt.plot(range(len(df_mean)), df_mean, 'o')
plt.xticks(range(0,len(df_mean), 100), labels, rotation='vertical')


plt.show()

