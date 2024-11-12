import numpy as np
from pso_funcoes import CarregamentoMaximo
from time import time


def pso(n_particulas, n_iteracoes, n_tensoes):
    posicoes = np.random.uniform(Vmin, Vmax, (n_particulas, n_tensoes))
    velocidades = np.zeros((n_particulas,n_tensoes))
    fitness = np.array([CarregamentoMaximo(posicao) for posicao in posicoes])
    pbest = np.copy(posicoes)
    valor_pbest = np.copy(fitness)
    posicao_gbest = np.zeros(n_tensoes)
    valor_gbest = 0
    for i in range(n_particulas):
        if fitness[i] > valor_gbest:
            valor_gbest = fitness[i]
            posicao_gbest = np.copy(posicoes[i])
    print(f'Iteração 0 concluída! Carregamento máximo: {valor_gbest:.4f}')
    for i in range(n_iteracoes):
        r1 = np.random.uniform(0, 1, (n_particulas, n_tensoes))
        r2 = np.random.uniform(0, 1, (n_particulas, n_tensoes))
        velocidades = w * velocidades + c1 * r1 * (pbest - posicoes) + c2 * r2 * (posicao_gbest - posicoes)
        posicoes += velocidades
        for j in range(n_particulas):
            posicoes[j, :] = np.clip(posicoes[j, :], Vmin, Vmax)
        fitness = np.array([CarregamentoMaximo(posicao) for posicao in posicoes])
        for j in range(n_particulas):
            if fitness[j] > valor_pbest[j]:
                valor_pbest[j] = fitness[j]
                pbest[j] = np.copy(posicoes[j])
        melhor_fitness_idx = np.argmax(fitness)
        if fitness[melhor_fitness_idx] > valor_gbest:
            valor_gbest = fitness[melhor_fitness_idx]
            posicao_gbest = np.copy(posicoes[melhor_fitness_idx])
        print(f'Iteração {i + 1} concluída! Carregamento máximo: {valor_gbest:.4f}')
    return valor_gbest, posicao_gbest


n_particulas = 10
n_iteracoes = 20
n_barras = 6
n_tensoes = 3

w = 0.8
c1 = 1.25
c2 = 1.25

Vmin = 0.94
Vmax = 1.1

print('PSO para maximização do carregamento do sistema')
print('-' * 100)

t0 = time()

carregamento_max, valor_vpg = pso(n_particulas, n_iteracoes, n_tensoes)

t1 = time()

# Resultados
print('-' * 100)
print(f'Resultado final:')
variaveis = ['V1','V2','V3']
for i in range(len(variaveis)):
    print(f'{variaveis[i]} = {valor_vpg[i]:.4f} pu')
print(f'Carregamanto máximo = {carregamento_max:.4f}')
print(f'Tempo de execução: {t1 - t0:.2f} s')
print('-' * 100)

