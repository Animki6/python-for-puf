import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



df = []
board_names = []
for i in range(len(sys.argv)-1):
    file_path = sys.argv[i+1]

    df.append(pd.read_csv(file_path))
    board_names.append(os.path.basename(file_path).split('.')[0])

    print(len(df))
    print(file_path)

df_mean = []
intra_var = []
inter_var = []
inter_var_tics = []

for i in range(len(df)):
    df_mean.append(df[i].mean(axis=0))
    df_std = df[i].std(axis=0)
    print('Max standard deviation: {}'.format(max(df_std)))
    num_of_error_bits = sum(1 for i in df_mean[i] if i not in (0.0, 1.0)) # Hamming Distance!
    print(num_of_error_bits)
    intra_var.append(num_of_error_bits/len(df_mean[i]))
    print(str(intra_var[i]*100)+'%')
    majority_out = [round(n) for n in df_mean[i]]
    print('{}'.format(hex(int(''.join([str(s) for s in majority_out]), 2))))

    # suma = 0
    # for i in range(df[i].shape[0]):
    #     suma += (sum(1 for j in range(df[i].shape[1]) if df_mean[i][j] != df[i].iloc[i, j])/df[i].shape[1])*100

    # IC = suma/df[i].shape[0]
    # print('ID : {}%'.format(IC))

for i in range(len(df)):
    for j in range(i):
        if (j != i):
            num_of_error_bits = sum(1 for k in abs(df_mean[i]-df_mean[j]) if k == 1.) # Hamming Distance!
            temp_inter_var = 100 * num_of_error_bits/len(df_mean[i])
            inter_var.append(temp_inter_var)
            inter_var_tics.append("({},{})".format(i, j))
            print("Inter puf variation ({},{}) {}".format(i, j, temp_inter_var))

maen_inter_PUF = sum(inter_var)/len(inter_var)
print("Mean inter puf var: {}%".format(maen_inter_PUF))

#plt.figure(1)
#ax1 = plt.subplot(len(df), 1, 1)
fig, axes = plt.subplots(len(df), 1)

for i in range(len(df)):
    axes[i].text(-30, 0.25, "b_"+ board_names[i], fontsize=14)
    axes[i].plot(range(len(df_mean[i])), df_mean[i], '.')
    text_str = "intra puf variations: {:.2f}%".format(100*intra_var[i])
    axes[i].text(140, 0.5, text_str, fontsize=12)

#plt.xticks(range(0,len(df_mean), 100), labels, rotation='vertical')
plt.subplots_adjust(left=0.15, right=0.75)

plt.show()

plt.figure(2)
plt.title("InterPUF variation")
plt.plot(inter_var, linestyle='', marker='o')
plt.axhline(maen_inter_PUF, linestyle='dashed')
avg_description = "average: {:.2f}%".format(maen_inter_PUF)
plt.text(0, maen_inter_PUF, avg_description)
plt.xticks(range(len(inter_var)), inter_var_tics)
plt.ylim(0, 100)

plt.show()


