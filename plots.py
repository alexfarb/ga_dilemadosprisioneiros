import matplotlib.pyplot as plt
import csv
import numpy as np
from math import pi
from matplotlib import rc

# rc('text', usetex=True)

class GetConfigFile(object):  # Classe para ler o arquivo de configuração de parâmetros
    def __init__(self, file):
        self.file = file

    def read_file(self):  # Função que realiza a leitura do arquivo de texto linha por linha
        with open(self.file) as f:
            content = f.read().splitlines()
        return content

class ReadFile(object):

    def __init__(self, chromosome_length, attempt, generations):
        self.chromosome_length = chromosome_length
        self.attempt = attempt
        self.generations = generations

    def read_single_row(self, file):
        with open(file, 'r') as arch:
            reader = csv.reader(arch, delimiter=',')
            file_data = []
            for p in range(0, self.chromosome_length):
                file_data.append(0)
            for row in reader:
                var_index = 0
                for value in row:
                    file_data[var_index] = float(value)
                    var_index += 1
        return file_data

    def read_multiple_rows(self, file):
        with open(file, 'r') as arch:
            index_row = 0
            reader = csv.reader(arch, delimiter=',')
            file_data = np.zeros((self.attempt, self.generations))
            for row in reader:
                var_index = 0
                if row != []:
                    for value in row:
                        file_data[index_row][var_index] = float(value)
                        var_index += 1
                    index_row +=1
        return file_data


# # function that creates latex-table
# def latex_table(celldata,rowlabel,collabel):
#     table = r'\begin{table} \begin{tabular}{|1|'
#     for c in range(0,len(collabel)):
#         # add additional columns
#         table += r'1|'
#     table += r'} \hline'
#
#     # provide the column headers
#     for c in range(0,len(collabel)-1):
#         table += collabel[c]
#         table += r'&'
#     table += collabel[-1]
#     table += r'\\ \hline'
#
#     # populate the table:
#     # this assumes the format to be celldata[index of rows][index of columns]
#     for r in range(0,len(rowlabel)):
#         table += rowlabel[r]
#         table += r'&'
#         for c in range(0,len(collabel)-2):
#             if not isinstance(celldata[r][c], basestring):
#                 table += str(celldata[r][c])
#             else:
#                 table += celldata[r][c]
#             table += r'&'
#
#         if not isinstance(celldata[r][-1], basestring):
#             table += str(celldata[r][-1])
#         else:
#             table += celldata[r][-1]
#         table += r'\\ \hline'
#
#     table += r'\end{tabular} \end{table}'
#
#     return table

def plot ():

    data = GetConfigFile('parameters.txt') # Carrega o arquivo de parâmetros
    data_file = data.read_file() # Realiza a leitura do arquivo de configuração
    population_count = int(data_file[1]) # Tamanho da População - Linha 2
    generations = int(data_file[15]) # Número de Gerações
    c_value = int(data_file[17]) # Valor do C - Linha 18
    bonus_value = float(data_file[19]) # Valor do Bônus - Linha 20
    bonus_value_pc = bonus_value * 100
    population_opositor_pc = float(data_file[21]) # Tamanho da População Opositora - Linha 22
    population_opositor_value = population_opositor_pc
    population_opositor_size = int((population_count*population_opositor_pc)/100) # Transforma para valor númerico a porcentagem da população
    fitness_class = int(data_file[23]) # Tipo de Fitness que deseja calcular - Linha 24

    fitness_name = []
    if fitness_class == 0:
        fitness_name.append('Individual')
    elif fitness_class == 1:
        fitness_name.append('Grupo')
    else:
        pass

    opositor_name = []
    if population_opositor_size == 1:
        opositor_name.append('Par-a-par')
    elif population_opositor_size > 1:
        opositor_name.append('%s %% de Opositores' %(population_opositor_value))
    else:
        pass

    m1 = 30 # Número de Genes
    n1 = generations # Número de Gerações
    attempt = 5 # Número de execuções do código

    rf = ReadFile(m1, attempt, n1)
    best_fitness_attempt_scenario_x = rf.read_multiple_rows('best_fitness_attempt_scenario_x.csv')
    # best_individual_attempt_scenario_x = rf.read_multiple_rows_str('best_individual_attempt_scenario_x.csv')
    # print(best_individual_attempt_scenario_x)
    c_total_attempt_scenario_x = rf.read_multiple_rows('c_total_attempt_scenario_x.csv')
    d_total_attempt_scenario_x = rf.read_multiple_rows('d_total_attempt_scenario_x.csv')

    # Lê o arquivo com os melhores indivíduos por execução
    individual_data_file = GetConfigFile('best_individual_attempt_scenario_x.csv')
    individual_attempt = individual_data_file.read_file()
    individual_attempt_1 = individual_attempt[0]
    individual_attempt_2 = individual_attempt[2]
    individual_attempt_3 = individual_attempt[4]
    individual_attempt_4 = individual_attempt[6]
    individual_attempt_5 = individual_attempt[8]
    individual_data = [[individual_attempt_1], [individual_attempt_2], [individual_attempt_3], [individual_attempt_4], [individual_attempt_5]]

    best_fitness_attempt_scenario_x_mean = np.mean(best_fitness_attempt_scenario_x, axis = 0)
    best_fitness_attempt_scenario_x_std = np.std(best_fitness_attempt_scenario_x, axis = 0)
    c_total_attempt_scenario_x_mean = np.mean(c_total_attempt_scenario_x, axis=0)
    c_total_attempt_scenario_x_std = np.std(c_total_attempt_scenario_x, axis=0)
    d_total_attempt_scenario_x_mean = np.mean(d_total_attempt_scenario_x, axis=0)
    d_total_attempt_scenario_x_std = np.std(d_total_attempt_scenario_x, axis=0)
    c_total_attempt_scenario_x_vecmean = [c_total_attempt_scenario_x_mean[n1-n1], c_total_attempt_scenario_x_mean[n1-(n1-1)], c_total_attempt_scenario_x_mean[n1-(n1-2)], c_total_attempt_scenario_x_mean[n1-(n1-3)], c_total_attempt_scenario_x_mean[n1-(n1-4)] ,c_total_attempt_scenario_x_mean[n1-5], c_total_attempt_scenario_x_mean[n1-4], c_total_attempt_scenario_x_mean[n1-3], c_total_attempt_scenario_x_mean[n1-2], c_total_attempt_scenario_x_mean[n1-1]]
    c_total_attempt_scenario_x_vecstd = [c_total_attempt_scenario_x_std[n1-n1], c_total_attempt_scenario_x_std[n1-(n1-1)], c_total_attempt_scenario_x_std[n1-(n1-2)], c_total_attempt_scenario_x_std[n1-(n1-3)], c_total_attempt_scenario_x_std[n1-(n1-4)] ,c_total_attempt_scenario_x_std[n1-5], c_total_attempt_scenario_x_std[n1-4], c_total_attempt_scenario_x_std[n1-3], c_total_attempt_scenario_x_std[n1-2], c_total_attempt_scenario_x_std[n1-1]]
    d_total_attempt_scenario_x_vecmean = [d_total_attempt_scenario_x_mean[n1-n1], d_total_attempt_scenario_x_mean[n1-(n1-1)], d_total_attempt_scenario_x_mean[n1-(n1-2)], d_total_attempt_scenario_x_mean[n1-(n1-3)], d_total_attempt_scenario_x_mean[n1-(n1-4)] ,d_total_attempt_scenario_x_mean[n1-5],d_total_attempt_scenario_x_mean[n1-4], d_total_attempt_scenario_x_mean[n1-3], d_total_attempt_scenario_x_mean[n1-2], d_total_attempt_scenario_x_mean[n1-1]]
    d_total_attempt_scenario_x_vecstd = [d_total_attempt_scenario_x_std[n1-n1], d_total_attempt_scenario_x_std[n1-(n1-1)], d_total_attempt_scenario_x_std[n1-(n1-2)], d_total_attempt_scenario_x_std[n1-(n1-3)], d_total_attempt_scenario_x_std[n1-(n1-4)] ,d_total_attempt_scenario_x_std[n1-5],d_total_attempt_scenario_x_std[n1-4], d_total_attempt_scenario_x_std[n1-3], d_total_attempt_scenario_x_std[n1-2], d_total_attempt_scenario_x_std[n1-1]]

    # Plots
    # Parte 1 - Média e Desvio Padrão do Fitness do Melhor Indivíduo

    N = 10 # Número de amostras para se analizar o impacto de C e D
    ind = np.arange(N)  # Total de Grupos a serem plotados no gráfico de barras
    width = 0.35       # Largura das barras

    fig, ax = plt.subplots()
    title = "Caso de Teste = %s, Fitness = %s, Valor de C = %s, Bônus = %s %%" %(opositor_name[0], fitness_name[0], c_value, bonus_value_pc)
    plt.suptitle(title,y=1, fontsize = 14)
    plt.subplot(311)
    plt.title('Média e Desvio Padrão do Fitness por Geração')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    x = np.linspace(0,n1-1,n1)
    plt.xlim((0,n1))
    plt.errorbar(x,best_fitness_attempt_scenario_x_mean,yerr=best_fitness_attempt_scenario_x_std,errorevery=10,ecolor='red',label='Média (Linha Azul)\nDesvio-Padrão (Barra Vermelha)')
    plt.legend()
    plt.tight_layout()
    # Parte 2, Total de C e D por execução
    plt.subplot(312)
    rects1 = plt.bar(ind, c_total_attempt_scenario_x_vecmean, width, color='r', yerr=c_total_attempt_scenario_x_vecstd)
    rects2 = plt.bar(ind + width, d_total_attempt_scenario_x_vecmean, width, color='y', yerr=d_total_attempt_scenario_x_vecstd)
    plt.ylabel('Total de Ocorrências')
    plt.xlabel('Gerações')
    plt.title('Média e Desvio Padrão do Total de Cooperações(C) e Delações(D)')
    plt.xticks(ind + width / 2, (n1-(n1-1), n1-(n1-2), n1-(n1-3), n1-(n1-4), n1-(n1-5), n1-4, n1-3, n1-2, n1-1, n1))
    plt.legend((rects1[0], rects2[0]), ('Cooperações(C)', 'Delações(D)'), loc='upper left')
    # plt.grid('on')
    # ax.xaxis.grid(True)  # vertical lines
    # ax.yaxis.grid(False)  # vertical lines
    plt.tight_layout()

    plt.subplot(313)
    # plt.title('Melhor Indivíduo por Execução')
    cell_data = individual_data
    # row_label = (['%d' % x for x in (1, 2, 3, 4, 5)])
    row_label = ('1','2', '3', '4', '5')
    col_label = ('Melhor Indivíduo','Melhor Indivíduo')
    plt.axis('off')
    the_table = plt.table(cellText=cell_data,
                          rowLabels=row_label,
                          colLabels=col_label,
                          cellLoc='center',
                          loc='center')

    the_table.set_fontsize(18)

    plt.show()
