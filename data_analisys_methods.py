import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def Hamming_Distance(r_a, r_b):
    if len(r_a) != len(r_b):
        raise Exception("Responses lengths do not match!")

    return sum(1 for j in [r_a[i] != r_b[i] for i in range(len(r_a))] if j)


def average_response(r_list):
    r_avg = np.average(r_list, axis=0)
    r_rounded = np.around(r_avg)
    return r_rounded


def boards_diff_ratio(board1, board2):
    n = board1.values.shape[1]
    return 100 * Hamming_Distance(average_response(board1.values), average_response(board2.values))/n


def compute_intraPUF_variation(single_board_responses):
    # for one board
    N = single_board_responses.shape[0]  # number of tries
    n = single_board_responses.shape[1]  # length of a response
    r_avg = average_response(single_board_responses)
    intraPUF_var = 100 * sum(Hamming_Distance(single_board_responses[i], r_avg) for i in range(N)) / (n*N)
    return intraPUF_var


def compute_reliability(boards_list):
    intra_PUF_variations = []
    for single_board_response in boards_list:
        intra_PUF_variations.append(compute_intraPUF_variation(single_board_response.values))

    return 100 - sum(intra_PUF_variations)/len(intra_PUF_variations)


def compute_uniqueness(boards_list):
    M = len(boards_list)  # ilosc matryc
    N = boards_list[0].shape[0]  # ilość pobranych odpowiedzi dla każdej matrycy
    n = boards_list[0].shape[1]  # długość odpowiedzi

    temp_sum = 0
    for i in range(M-1):
        for j in range(1, M):
            if i != j:
                temp_sum += Hamming_Distance(average_response(boards_list[i].values), average_response(boards_list[j].values))/n

    return 100 * 2 * temp_sum / (M*(M-1))

def intra_dist_plot(boards_data):
    intra_PUF_variations = []
    for r_list in boards_data:
        intra_PUF_variations.append(compute_intraPUF_variation(r_list.values))

    print(intra_PUF_variations)

    p1 = sns.distplot(intra_PUF_variations,  bins=round(len(intra_PUF_variations)/1.5), norm_hist=True)
    p1.set_title("Rozkład wartości odchylenia wewnątrz-PUF")
    #plt.hist(intra_PUF_variations)
    p1.set_xlim(0, 20)
    p1.set_xlabel("Odchylenie wewnątrz-PUF (%)")
    p1.set_ylabel("Częstość wystąpienia")
    return p1

def inter_dist_plot(boards_data):
    inter_PUF_variations = []
    M = len(boards_data)
    for i in range(M):
        for j in range(i):
            if(j != i):
                inter_PUF_variations.append(boards_diff_ratio(boards_data[i], boards_data[j]))

    p1 = sns.distplot(inter_PUF_variations,  bins=round(len(inter_PUF_variations)/1.5), norm_hist=True)
    p1.set_title("Rozkład wartości odchylenia między-PUF")
    #plt.hist(intra_PUF_variations)
    p1.set_xlim(0, 100)
    p1.set_ylabel("Częstość wystąpienia")
    p1.set_xlabel("Odchylenie między-PUF (%)")


    return p1


