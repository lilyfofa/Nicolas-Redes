import numpy as np
from pso_funcoes import CarregamentoMaximo
from time import time


def pso(n_particulas, n_iteracoes, n_tensoes, n_pgs):
    # Parâmetros iniciais
    tensoes = np.random.uniform(Vmin, Vmax, (n_particulas, n_tensoes))
    geracoes = np.random.uniform(Pgmin, Pgmax, (n_particulas, n_pgs))
    posicoes = np.block([tensoes, geracoes])
    velocidades = np.zeros((n_particulas, n_tensoes + n_pgs))
    fitness = np.array([CarregamentoMaximo(posicao) for posicao in posicoes])
    pbest = np.copy(posicoes)
    valor_pbest = np.copy(fitness)
    posicao_gbest = np.zeros(n_tensoes + n_tensoes)
    valor_gbest = 0
    for i in range(n_particulas):
        if fitness[i] > valor_gbest:
            valor_gbest = fitness[i]
            posicao_gbest = np.copy(posicoes[i])
    print(f'Iteração 0 concluída! Carregamento máximo: {valor_gbest}')
    for i in range(n_iteracoes):
        r1 = np.random.uniform(0, 1, (n_particulas, n_tensoes+n_pgs))
        r2 = np.random.uniform(0, 1, (n_particulas, n_tensoes+n_pgs))
        velocidades = w * velocidades + c1 * r1 * (pbest - posicoes) + c2 * r2 * (posicao_gbest - posicoes)
        posicoes += velocidades
        for j in range(n_particulas):
            posicoes[j, :n_tensoes] = np.clip(posicoes[j, :n_tensoes], Vmin, Vmax)
            posicoes[j, n_tensoes:] = np.clip(posicoes[j, n_tensoes:], Pgmin, Pgmax)
        fitness = np.array([CarregamentoMaximo(posicao) for posicao in posicoes])
        for j in range(n_particulas):
            if fitness[j] > valor_pbest[j]:
                valor_pbest[j] = fitness[j]
                pbest[j] = np.copy(posicoes[j])
        melhor_fitness_idx = np.argmax(fitness)
        if fitness[melhor_fitness_idx] > valor_gbest:
            valor_gbest = fitness[melhor_fitness_idx]
            posicao_gbest = np.copy(posicoes[melhor_fitness_idx])
        print(f'Iteração {i + 1} concluída! Carregamento máximo: {valor_gbest}')
    return valor_gbest, posicao_gbest


n_particulas = 10
n_iteracoes = 20
n_barras = 6
n_tensoes = 3
n_pgs = 2

w = 0.8
c1 = 1.25
c2 = 1.25

Vmin = 0.94
Vmax = 1.1

Pgmin = 0
Pgmax = 100

print('PSO para maximização do carregamento do sistema')
print('-' * 50)

t0 = time()

carregamento_max, valor_vpg = pso(n_particulas, n_iteracoes, n_tensoes, n_pgs)

t1 = time()

# Resultados
print('-' * 50)
print(f'Resultado final:')
variaveis = ['V1','V2', 'V3', 'Pg2', 'Pg3']
for i in range(len(variaveis)):
    print(f'{variaveis[i]} = {valor_vpg[i]} pu')
print(f'Carregamanto máximo = {carregamento_max}')
print(f'Tempo de execução: {t1 - t0:.2f} s')
print('-' * 50)
