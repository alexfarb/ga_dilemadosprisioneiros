"""" 

                  Trabalho de Computação Evolucionária

Código referente a tarefa do Dilema dos Prisioneiros

@author: Farb

"""

import random
from random import randint 
import numpy as np
import csv
import plots

class GetConfigFile(object): # Classe para ler o arquivo de configuração de parâmetros
    def __init__(self, file):
        self.file = file
        
    def read_file(self): # Função que realiza a leitura do arquivo de texto linha por linha
        with open(self.file) as f:
            content = f.read().splitlines()
        return content

class Chromosome(object): # Classe onde o Cromossomo é gerado.
    def __init__(self, length, max, min):
        self.length = length
        self.max = max
        self.min = min
        
    def create_chromosome(self):
        return [round(random.uniform(self.min,self.max),5) for x in range(self.length)] # Cria o Cromossomo com no máximo 5 casas decimais

class GeneratePopulation(object): # Classe onde a população é gerada.
    def __init__(self, count):
        self.count = count
        
    def create_population(self, length, max, min):
        chromosome = Chromosome(length, max, min) # Instaciamento
        return [chromosome.create_chromosome() for x in range(self.count)]
        
class Evaluate(object):
# A classe avaliador é a interface do AG com o problema que está sendo otimizado. 
# Nesta classe o cromossomo é decodificado para gerar o individuo, do qual é calculado o fitness.
    def __init__(self, fitness_individual_table, fitness_group_table, c_value, bonus_value):
        self.fitness_individual_table = fitness_individual_table
        self.fitness_group_table = fitness_group_table
        self.c_value = c_value
        self.bonus_value = bonus_value

    def decode(self, chromosome): # Decodifica o Cromossomo
        results = ['C','D']
        individual = []
        for i in range(len(chromosome)): # Necessário criar como vetor, pois o numpy acaba não tornando possível fazer a iteração
            individual.append(i)
        for i in range(len(chromosome)):
            if chromosome[i] < 0.5: # Se o valor for menor que 0.5 o gene recebe C
                individual[i] = results[0]
            elif chromosome[i] > 0.5: # Se o valor for maior que 0.5 o gene recebe D
                individual[i] = results[1]
            else:
                individual[i] = random.choice(results) # Se for exatamente 0.5 faz uma escolha aleatória entre C e D
        return individual
    
    def calculate_fitness_bonus(self, chromosome_test): # Calcula a parcela bônus do Fitness
        fitness_b = []    
        c_genes = [] # Genes da cadeia com 'C'
        c_genes_mean = [] # Média dos Genes com 'C'
        c_count = 0
        c_chain = 0
        chromosome_test_decoded = self.decode(chromosome_test) 
        # Contagem da Cadeia de C's
        for j in range(len(chromosome_test_decoded)): # Percorre o Cromossomo de Teste
            if chromosome_test_decoded[j] == 'C': # Se encontrar um C o contado de C aumenta em 1
                c_count = c_count+1
                c_genes.append(chromosome_test[j])
                if c_count == self.c_value: # Se for igual ao Total de C's pra cadeia
                    c_chain = c_chain+1 # O total de cadeias aumenta em 1
                    c_count = 0 # A contagem de C's volta pra 0
                    c_genes_mean.append(np.mean(c_genes))
                    c_genes = [] # O vetor de armazenamento dos genes com 'C' volta a ser vazio
                else:
                    pass
            else:
                c_count = 0
                
        for i in range(len(c_genes_mean)): 
            fitness_b.append((c_chain*self.bonus_value)*(1 - c_genes_mean[i])) # Aplicação do Bônus e cálculo da segunda parcela do fitness
        
        bonus_len = len(fitness_b)
        # print(fitness_b)
        if bonus_len > 1:
            fitness_bonus = np.sum(fitness_b)
        elif bonus_len == 1:
            fitness_bonus = fitness_b[0]
        else:
            fitness_bonus = 0
        # print(fitness_bonus)
        
        return fitness_bonus
        
    def calculate_fitness_individual(self, chromosome_test, chromosome_opositor): # Cálculo do Fitness Individual  
        chromosome_test_decoded = self.decode(chromosome_test) # Decodifica o Cromossomo de Teste
        chromosome_opositor_decoded = self.decode(chromosome_opositor) # Decodifica o Cromossomo Opositor
        fitness_individual_b = self.calculate_fitness_bonus(chromosome_test) # Cacula o bônus do fitness
        # Emparelhamento dos Cromossomos
        chromosome_joined = list(map(lambda chromosome_test_decoded, chromosome_opositor_decoded: chromosome_test_decoded + chromosome_opositor_decoded, chromosome_test_decoded, chromosome_opositor_decoded))
        fitness_individual_a = [] # Vetor para armazenar a primeira parcela do fitness
        # Parcela 1 do Fitness
        for i in range(len(chromosome_joined)): # Percorre o Cromossomo Emparelhado
        #Valores da Tabela de Fitness Individual
            if chromosome_joined[i] == 'DC':
                fitness_individual_a.append(self.fitness_individual_table[0])
            elif chromosome_joined[i] == 'CC':
                fitness_individual_a.append(self.fitness_individual_table[1])
            elif chromosome_joined[i] == 'DD':
                fitness_individual_a.append(self.fitness_individual_table[2])
            elif chromosome_joined[i] == 'CD':
                fitness_individual_a.append(self.fitness_individual_table[3])
            else:
                pass
        
        return np.mean(fitness_individual_a)+fitness_individual_b

    def calculate_fitness_group(self, chromosome_test, chromosome_opositor): # Cálculo do Fitness em Grupo
        chromosome_test_decoded = self.decode(chromosome_test) # Decodifica o Cromossomo de Teste
        chromosome_opositor_decoded = self.decode(chromosome_opositor) # Decodifica o Cromossomo Opositor
        fitness_group_b = self.calculate_fitness_bonus(chromosome_test) # Cacula o bônus do fitness
        # Emparelhamento dos Cromossomos
        chromosome_joined = list(map(lambda chromosome_test_decoded, chromosome_opositor_decoded: chromosome_test_decoded + chromosome_opositor_decoded, chromosome_test_decoded, chromosome_opositor_decoded))
        fitness_group_a = []
        # Parcela 1 do Fitness
        for i in range(len(chromosome_joined)):# Percorre o Cromossomo Emparelhado
        # Valores da Tabela de Fitness em Grupo
            if chromosome_joined[i] == 'CC':
                fitness_group_a.append(self.fitness_individual_table[0])
            elif chromosome_joined[i] == 'CD':
                fitness_group_a.append(self.fitness_individual_table[1])
            elif chromosome_joined[i] == 'DC':
                fitness_group_a.append(self.fitness_individual_table[1])            
            elif chromosome_joined[i] == 'DD':
                fitness_group_a.append(self.fitness_individual_table[2])
            else:
                pass

        return np.mean(fitness_group_a)+fitness_group_b

class GeneticAlgorithm(object): # Classe onde há a implementação dos operadores genéticos.
# Deve usar cruzamento aritmético e mutação Gaussiana.
# A seleção deve ser por torneio.
# A troca da população será geracional.   
    
    def __init__(self, population, fitness, population_count):
        self.population = population
        self.fitness = fitness
        self.population_count = population_count
    
    def selection(self, ring_size): # Seleção por Torneio.
        selected_winners = []
        for x in range(len(self.population)):
            selected = [randint(0,len(self.population) - 1) for i in range(ring_size)]
            aux = self.fitness[selected[0]]
            index = selected[0]
            for i in range(1,ring_size-1):
                if self.fitness[selected[i]] >= aux:
                    aux = self.fitness[selected[i]]
                    index = selected[i]
            selected_winners.append(self.population[index])
        return selected_winners
    
    def crossover(self, selected_winners, crossover_probability): # Cruzamento Aritmético.
        offspring = []
        i = 0          
        while i < (int(self.population_count/2)):
            chance = random.random()
            alpha = random.random()
            # Coeficiente aleatório de 0 a 1 para o cálculo do cruzamento aritmético
            if chance <= crossover_probability:
                parent_a = np.array(random.choice(selected_winners))
                parent_b = np.array(random.choice(selected_winners))
            else:
                continue
            if parent_a is not parent_b:
                offspring_a = np.round(parent_a + (parent_b - parent_a)*alpha,5) # Cruzamento aritmético
                offspring_b = np.round(parent_b + (parent_a - parent_b)*alpha,5) # Cruzamento aritmético
                i = i+1
            else:
                continue        
            offspring.append(offspring_a.tolist()) 
            offspring.append(offspring_b.tolist())

        return offspring
    
    def mutation(self, offspring, standard_deviation,mutation_probability): # Função para realizar a mutação gaussiana
    # Realiza a mutação gaussiana gene a gene em cada cromossomo da população
        mutated = [[np.absolute(random.gauss(gene, standard_deviation)) if random.random() <= mutation_probability else gene for gene in sublst] for sublst in offspring]  
        new_mut = [[1-(abs(gene-1)) if gene > 1 else gene for gene in sublst] for sublst in mutated]
        new_mut_round = np.round(new_mut,5)
        new_mut_final = new_mut_round.tolist()
        return new_mut_final
    
    def get_best_fitness(self, offspring, offspring_fitness): # Pega o melhor fitness da população
        best_offspring_fitness = offspring_fitness[0]
        best_offspring = offspring[0]
        for i in range(1, self.population_count):
            if offspring_fitness[i] > best_offspring_fitness:
                best_offspring_fitness = offspring_fitness[i]
                best_offspring = offspring[i]
        return best_offspring_fitness, best_offspring    

# Leitura dos parâmetros contidos no arquivo txt

data = GetConfigFile('parameters.txt') # Carrega o arquivo de parâmetros
data_file = data.read_file() # Realiza a leitura do arquivo de configuração
population_count = int(data_file[1]) # Tamanho da População - Linha 2
ring_size = int(data_file[3]) # Tamanho do Ring - Linha 4
crossover_probability = float(data_file[5]) # Probabilidade de Crossover - Linha 6
mutation_probability = float(data_file[7]) # Probabilidade de Mutação - Linha 8
standard_deviation = float(data_file[9]) # Desvio-Padrão (Mutação Gaussiana) - Linha 10
fitness_individual_table = data_file[11].split(",") # Tabela do Fitness Individual - Linha 12
fitness_individual_table = list(map(float, fitness_individual_table)) # Tabela do Fitness Individual em um vetor, do melhor para o pior
fitness_group_table = data_file[13].split(",") # Tabela do Fitness Individual - Linha 14
fitness_group_table = list(map(float, fitness_group_table)) # Tabela do Fitness Individual em um vetor, do melhor para o pior
generations = int(data_file[15]) # Número de Gerações
c_value = int(data_file[17]) # Valor do C - Linha 18
bonus_value = float(data_file[19]) # Valor do Bônus - Linha 20
population_opositor_pc = float(data_file[21]) # Tamanho da População Opositora - Linha 22
population_opositor_size = int((population_count*population_opositor_pc)/100) # Transforma para valor númerico a porcentagem da população                               
fitness_class = int(data_file[23]) # Tipo de Fitness que deseja calcular - Linha 24
attempt = 5 # Número de execuções
# Características do Cromossomo
chromosome_length = 30 # Tamanho do individuo a ser repassado como argumento para a geração da população
chromosome_min = 0 # Valor minimo de um gene do cromossomo
chromosome_max = 1 # Valor máximo de um gene do cromossomo

# Função Principal
best_fitness_attempt = []
best_chromossome_attempt = []
c_total_attempt = []
d_total_attempt = []
for i in range(attempt): # Laço iniciar as várias execuções
    population = GeneratePopulation(population_count)
    population_chromosome = population.create_population(chromosome_length,chromosome_max,chromosome_min)
    fitness = Evaluate(fitness_individual_table, fitness_group_table, c_value, bonus_value) # Instanciamento da função de Fitness
    
    # Cálculo do Fitness para a população inicial
    if population_opositor_size == 1: # Caso de Teste 1 (Par-a-Par)
        population_fitness = np.zeros((population_count,1))+100 # Matriz onde será armazenado os fitness do caso 1
        if fitness_class == 0:
            for i in range (population_count):
                if population_opositor_size == 1 and population_fitness[i][0] == 100:
                    random_index = 0
                    while True:
                        random_index = random.randint(i,population_count-1)
                        if random_index != i and population_fitness[random_index][0] == 100: 
                            break
                    population_fitness[i] = fitness.calculate_fitness_individual(population_chromosome[i], population_chromosome[random_index])
                    population_fitness[random_index] = fitness.calculate_fitness_individual(population_chromosome[random_index], population_chromosome[i])
        elif fitness_class == 1:
            for i in range (population_count):
                if population_opositor_size == 1 and population_fitness[i][0] == 100:
                    random_index = 0
                    while True:
                        random_index = random.randint(i,population_count-1)
                        if random_index != i and population_fitness[random_index][0] == 100: 
                            break
                    population_fitness[i] = fitness.calculate_fitness_group(population_chromosome[i], population_chromosome[random_index])
                    population_fitness[random_index] = fitness.calculate_fitness_group(population_chromosome[random_index], population_chromosome[i])
        else:
            pass
        
    elif population_opositor_size > 1: # Casos de Teste 2 e 3
        population_fitness = []
        fitness_total = []
        fitness_vector = []
        fitness_vector_mean = []
        population_chromosome_for_rand = population_chromosome
        if fitness_class == 0:
            for i in range(len(population_chromosome)):
                assist = 0
                population_opositor_index = []
                population_index = list(np.linspace(0, population_count-1, population_count))
                population_index.pop(i)
                for j in range(population_opositor_size):
                    population_opositor_index.append(int(random.choice(population_index)))
                    aux = population_index.index(population_opositor_index[j])
                    population_index.pop(aux)
                for k in range (population_opositor_size):
                    fitness_vector.append(fitness.calculate_fitness_individual(population_chromosome[i], population_chromosome[population_opositor_index[k]]))
                    fitness_vector_size = len(fitness_vector)
            while assist < fitness_vector_size:
                mean_sum = 0
                for m in range(assist, assist+population_opositor_size):
                    mean_sum += fitness_vector[m]
                assist += population_opositor_size
                fitness_vector_mean.append(mean_sum/population_opositor_size)
                population_fitness.append(np.mean(fitness_vector_mean))
#                population_fitness.append(np.mean(fitness_total))
        elif fitness_class == 1:
            for i in range(len(population_chromosome)):
                assist = 0
                population_opositor_index = []
                population_index = list(np.linspace(0, population_count-1, population_count))
                population_index.pop(i)
                for j in range(population_opositor_size):
                    population_opositor_index.append(int(random.choice(population_index)))
                    aux = population_index.index(population_opositor_index[j])
                    population_index.pop(aux)
                for k in range (population_opositor_size):
                    fitness_vector.append(fitness.calculate_fitness_group(population_chromosome[i], population_chromosome[population_opositor_index[k]]))
                    fitness_vector_size = len(fitness_vector)
            while assist < fitness_vector_size:
                mean_sum = 0
                for m in range(assist, assist+population_opositor_size):
                    mean_sum += fitness_vector[m]
                assist += population_opositor_size
                fitness_vector_mean.append(mean_sum/population_opositor_size)
                population_fitness.append(np.mean(fitness_vector_mean))
#                population_fitness.append(np.mean(fitness_total))
        else:
            pass
    else:
        pass
            
    # Laço para iniciar o AG
    best_fitness_generation = []
    best_offspring_fitness = 0
    c_total_generation = []
    d_total_generation = []
    for i in range(generations): 
        ga = GeneticAlgorithm(population_chromosome, population_fitness, population_count) # Instanciamento da Classe GeneticAlgorithm
        selected = ga.selection(ring_size) # Seleção por Torneio
        offspring = ga.crossover(selected, crossover_probability) # Cruzamento Aritmético
        offspring_mutated = ga.mutation(offspring, standard_deviation, mutation_probability) # Mutação Gaussiana
        
        if population_opositor_size == 1: # Caso de Teste 1 (Par-a-Par)
            offspring_fitness = np.zeros((population_count,1))+100 # Matriz necessária para armazenar o fitness da população de filhos
            if fitness_class == 0:
                for i in range (population_count):
                    if population_opositor_size == 1 and offspring_fitness[i][0] == 100:
                        random_index = 0
                        while True:
                            random_index = random.randint(i,population_count-1)
                            if random_index != i and offspring_fitness[random_index][0] == 100: 
                                break
                        offspring_fitness[i] = fitness.calculate_fitness_individual(offspring_mutated[i], offspring_mutated[random_index])
                        offspring_fitness[random_index] = fitness.calculate_fitness_individual(offspring_mutated[random_index], offspring_mutated[i])
            elif fitness_class == 1:
                for i in range (population_count):
                    if population_opositor_size == 1 and offspring_fitness[i][0] == 100:
                        random_index = 0
                        while True:
                            random_index = random.randint(i,population_count-1)
                            if random_index != i and offspring_fitness[random_index][0] == 100: 
                                break
                        offspring_fitness[i] = fitness.calculate_fitness_group(offspring_mutated[i], offspring_mutated[random_index])
                        offspring_fitness[random_index] = fitness.calculate_fitness_group(offspring_mutated[random_index], offspring_mutated[i])
            else:
                pass
            
        elif population_opositor_size > 1: # Casos de Teste 2 e 3
            offspring_fitness = []
            fitness_total = []
            fitness_vector = []
            fitness_vector_mean = []
            population_chromosome_for_rand = offspring_mutated
            if fitness_class == 0:
                for i in range(len(population_chromosome)):
                    assist = 0
                    population_opositor_index = []
                    population_index = list(np.linspace(0, population_count-1, population_count))
                    population_index.pop(i)
                    for j in range(population_opositor_size):
                        population_opositor_index.append(int(random.choice(population_index)))
                        aux = population_index.index(population_opositor_index[j])
                        population_index.pop(aux)
                    for k in range (population_opositor_size):
                        fitness_vector.append(fitness.calculate_fitness_individual(offspring_mutated[i], offspring_mutated[population_opositor_index[k]]))
                        fitness_vector_size = len(fitness_vector)
                while assist < fitness_vector_size:
                    mean_sum = 0
                    for m in range(assist, assist+population_opositor_size):
                        mean_sum += fitness_vector[m]
                    assist += population_opositor_size
                    fitness_vector_mean.append(mean_sum/population_opositor_size)
                    offspring_fitness.append(np.mean(fitness_vector_mean))
#                    offspring_fitness.append(np.mean(fitness_total))
            elif fitness_class == 1:
                for i in range(len(population_chromosome)):
                    assist = 0
                    population_opositor_index = []
                    population_index = list(np.linspace(0, population_count-1, population_count))
                    population_index.pop(i)
                    for j in range(population_opositor_size):
                        population_opositor_index.append(int(random.choice(population_index)))
                        aux = population_index.index(population_opositor_index[j])
                        population_index.pop(aux)
                    for k in range (population_opositor_size):
                        fitness_vector.append(fitness.calculate_fitness_group(offspring_mutated[i], offspring_mutated[population_opositor_index[k]]))
                        fitness_vector_size = len(fitness_vector)
                while assist < fitness_vector_size:
                    mean_sum = 0
                    for m in range(assist, assist+population_opositor_size):
                        mean_sum += fitness_vector[m]
                    assist += population_opositor_size
                    fitness_vector_mean.append(mean_sum/population_opositor_size)
                    offspring_fitness.append(np.mean(fitness_vector_mean))
#                    offspring_fitness.append(np.mean(fitness_total))
            else:
                pass                                
        else:
            pass

        # if's necessários para se obter o melhor fitness em lista
        if population_opositor_size == 1:
            best_offspring_fitness, best_offspring = ga.get_best_fitness(offspring_mutated, offspring_fitness)
            best_offspring_fitness = best_offspring_fitness[0]
        elif population_opositor_size > 1:
            best_offspring_fitness, best_offspring = ga.get_best_fitness(offspring_mutated, offspring_fitness)            
        else:
            pass
        
        # Salva a população decodificada
        population_decoded = []
        population_decoded_c = []
        population_decoded_d = []
        
        # Decodifica a População
        for p in range(population_count):
            population_decoded.append(fitness.decode(offspring_mutated[p]))
        
        # Contagem de 'C' e 'D na população
        c_count = 0
        d_count = 0        
        for k in range(population_count):
            population_decoded_chromosome = population_decoded[k]
            for l in range(len(population_decoded_chromosome)):
                if population_decoded_chromosome[l] == 'C':
                    c_count = c_count + 1
                elif population_decoded_chromosome[l] == 'D':
                    d_count = d_count + 1
                else:
                    pass
                            
        # População final da Geração
        population_chromosome = offspring_mutated
        population_fitness = offspring_fitness
        best_fitness_generation.append(best_offspring_fitness)
    
        c_total_generation.append(c_count)
        d_total_generation.append(d_count)     
    
    c_total_attempt.append(c_total_generation)
    d_total_attempt.append(d_total_generation)
    best_fitness_attempt.append(best_fitness_generation) # Armazena os fitness de cada geração por execução
    best_chromossome_attempt.append(best_offspring) # Melhor cromossomo por execução
        
    
# Salva os Fitness por geração de cada execução em um .csv
best_individual_attempt = []
for k in range(len(best_chromossome_attempt)):
    best_individual_attempt.append(fitness.decode(best_chromossome_attempt[k]))

with open('best_fitness_attempt_scenario_x.csv','w') as outfile:
    best_fitness_attempt_data = csv.writer(outfile)
    for row in best_fitness_attempt:
        best_fitness_attempt_data.writerow(row)

        
with open('c_total_attempt_scenario_x.csv','w') as outfile:
    c_total_attempt_data = csv.writer(outfile)
    for row in c_total_attempt:
        c_total_attempt_data.writerow(row)
        
with open('d_total_attempt_scenario_x.csv','w') as outfile:
    d_total_attempt_data = csv.writer(outfile)
    for row in d_total_attempt:
        d_total_attempt_data.writerow(row)

with open('best_individual_attempt_scenario_x.csv','w') as outfile:
    best_individual_attempt_data = csv.writer(outfile)
    for row in best_individual_attempt:
        best_individual_attempt_data.writerow(row)

plots.plot()