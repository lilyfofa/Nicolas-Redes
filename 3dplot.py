import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pso_funcoes import CarregamentoMaximo3D

# Defina o intervalo dos valores de P_g para as barras 2 e 3 (0 a 1.5 pu)
P_g2 = np.linspace(0, 1.5, 11)
P_g3 = np.linspace(0, 1.5, 11)

# Crie a malha de valores de P_g2 e P_g3
P_g2_grid, P_g3_grid = np.meshgrid(P_g2, P_g3)

# Vetorize a função
carregamento_maximo_vetorizado = np.vectorize(CarregamentoMaximo3D)

# Calcule o carregamento para a malha de valores
carregamento = carregamento_maximo_vetorizado(P_g2_grid, P_g3_grid)

# Valor constante para o plano z = 0.9556
z_plane = 0.9556

# Crie uma matriz constante para o plano z = 0.9556
Z_plane = np.full_like(P_g2_grid, z_plane)

# Plot 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Superfície 3D para o carregamento máximo
ax.plot_surface(P_g2_grid, P_g3_grid, carregamento, cmap='viridis', alpha=0.8)

# Superfície 3D para o plano em z = 0.9556
ax.plot_surface(P_g2_grid, P_g3_grid, Z_plane, color='red', alpha=0.5)

# Rótulos e título
ax.set_title('Carregamento versus Pg2 e Pg3')
ax.set_xlabel('Pg2 (pu)')
ax.set_ylabel('Pg3 (pu)')
ax.set_zlabel('Carregamento máximo')
ax.set_title('Carregamento Máximo em Função de Pg2 e Pg3')

# Mostrar o gráfico
plt.show()
