from funcoes import FluxoDeCargaLimitado
import matplotlib.pyplot as plt

alpha = 0
step = 0.01

tensoes = []
carregamento = []
sucesso = True

while sucesso:
    resultado = FluxoDeCargaLimitado(alpha)
    sucesso = resultado[0]
    if sucesso:
        print(f'Sucesso para alpha = {alpha:.4f}, Qg = {resultado[2]}')
        tensoes.append(resultado[1])
        carregamento.append(alpha)
        alpha += step
    else:
        print(f'Falha para alpha = {alpha:.4f}')

x = carregamento
y = [[], [], [], [], [], []]

for i in range(0, len(tensoes)):
    for j in range(0, len(tensoes[0])):
        y[j].append(tensoes[i][j])

print('Gerando gráfico...')
plt.figure(1)
plt.plot(x, y[0], label='Barra 1')
plt.plot(x, y[1], label='Barra 2')
plt.plot(x, y[2], label='Barra 3')
plt.plot(x, y[3], label='Barra 4')
plt.plot(x, y[4], label='Barra 5')
plt.plot(x, y[5], label='Barra 6')
plt.title("Tensão nas barras em função do carregamento")
plt.xlabel("Carregamento")
plt.ylabel("Magnitude de tensão [pu]")
plt.grid()
plt.legend()
plt.show()

