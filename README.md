# Dilema dos Prisioneiros
# Objetivo
Implementar um algoritmo genético capaz de simular uma população diante do Dilema dos Prisioneiros, e a partir do comportamento desta a cada geração, analisar a qual situação a população tende. Para a análise são utilizados gráficos e tabelas, além de que a conclusão é baseada em perguntas propostas no comando do trabalho.
# Metodologia
Neste trabalho a seguinte abordagem quanto ao dilema dos prisioneiros:
*	Duas pessoas cometeram um crime. Elas são presas. Para que o governo consiga prendê-los, ele precisa que elas confessem e mostrem provas sobre o crime. Elas são interrogadas separadas.
*	Se as duas pessoas não confessarem (isto é, cooperarem entre si), então o governo terá de soltá-los em 6 meses devido à falta de provas.
*	No entanto, se uma delas ficar calada e a outra confessar, a pessoa que cooperou com o parceiro de crime (ficou calado) vai ser preso por 30 anos, enquanto o outro que confessou, por ter ajudado a polícia, será solto na hora.
*	Se ambos confessarem, então ambos são presos por 10 anos por terem cooperado com a justiça.
A modelagem do algoritmo genético é feita da seguinte forma:
*	Cada indivíduo é uma cadeia de números reais entre 0 e 1, onde 0 é máxima cooperação com o parceiro e 1 é a máxima delação do parceiro. Ou seja, abaixo de 0,5 é cooperação (não delação) e acima de 0,5 é delação.
*	Cada cromossomo possui 30 genes.
*	Existem dois tipos de Fitness: Individual e Grupo
Os tipos de Fitness levam em consideração o pareamento entre cooperação (C) e delação (D), normalizados de 0 a 1, e de forma proporcional ao tempo de prisão.
