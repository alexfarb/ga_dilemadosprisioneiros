# Dilema dos Prisioneiros
# Objetivo
Implementar um algoritmo genético capaz de simular uma população diante do Dilema dos Prisioneiros, e a partir do comportamento desta a cada geração, analisar a qual situação a população tende. Para a análise são utilizados gráficos e tabelas, além de que a conclusão é baseada em perguntas propostas no comando do trabalho.
# Metodologia
Este trabalho considera a seguinte abordagem quanto ao dilema dos prisioneiros:
*	Duas pessoas cometeram um crime. Elas são presas. Para que o governo consiga prendê-los, ele precisa que elas confessem e mostrem provas sobre o crime. Elas são interrogadas separadas.
*	Se as duas pessoas não confessarem (isto é, cooperarem entre si), então o governo terá de soltá-los em 6 meses devido à falta de provas.
*	No entanto, se uma delas ficar calada e a outra confessar, a pessoa que cooperou com o parceiro de crime (ficou calado) vai ser preso por 30 anos, enquanto o outro que confessou, por ter ajudado a polícia, será solto na hora.
*	Se ambos confessarem, então ambos são presos por 10 anos por terem cooperado com a justiça.
A modelagem do algoritmo genético é feita da seguinte forma:
*	Cada indivíduo é uma cadeia de números reais entre 0 e 1, onde 0 é máxima cooperação com o parceiro e 1 é a máxima delação do parceiro. Ou seja, abaixo de 0,5 é cooperação (não delação) e acima de 0,5 é delação.
*	Cada cromossomo possui 30 genes.
*	Existem dois tipos de Fitness: Individual e Grupo
Os tipos de Fitness levam em consideração o pareamento entre cooperação (C) e delação (D), normalizados de 0 a 1, e de forma proporcional ao tempo de prisão.<br/>
Existe também uma parcela bônus do fitness, onde é levada em consideração a quantidade de cadeias de C encontradas no indivíduo de teste, essa parcela de bônus é dada pela fórmula abaixo.<br/>
<br/>
Bônus = (numerocadeias*valorbonus)*(1-mediagenes_c)<br/>
<br/>
Essa parcela bônus é adicionada a média encontrada na primeira parcela do fitness.<br/>
Quanto aos operadores do algoritmo genético, é utilizada a seleção por torneio, cruzamento aritmético, mutação gaussiana e o total de indivíduos da população é igual a 50.<br/> 
Há 3 casos de testes para a avaliação do problema proposto: (1) quando os indivíduos são comparados par-a-par, (2) quando um indivíduo é comparado com 10% da população e (3) quando um indivíduo é comparado a 30% da população. E em cada caso desse, é necessário verificar as seguintes situações: fixa-se uma valor de C e varia-se o bônus e fixa-se o bônus e varia-se o C.
