from sympy import *
from tabulate import tabulate


# Função para a matriz Ybus
def roundComplex(z, n):
    real = re(z)
    imag = im(z)
    if imag == 0:
        return round(float(real), n)
    else:
        return round(float(real), n) + 1j * round(float(imag), n)


# DCTE
S_base = 100
erro = 0.0001

# DBAR
n_barras = 6
Pg = [0, 1.4, 0.6, 0, 0, 0]
Pl = [0, 0, 0, 0.9, 1, 0.9]
Qg = [0, 0, 0, 0, 0, 0]
Ql = [0, 0, 0, 0.6, 0.7, 0.6]
Tensao = [1.1, 1.1, 1.1, 0, 0, 0]
Fase = [0, -1, -1, -1, -1, -1]

# DLIN
dlin = [(0.1 + 1j * 0.2, 4, 1, 2),
        (0.05 + 1j * 0.2, 4, 1, 4),
        (0.08 + 1j * 0.3, 6, 1, 5),
        (0.05 + 1j * 0.25, 6, 2, 3),
        (0.05 + 1j * 0.1, 2, 2, 4),
        (0.1 + 1j * 0.3, 4, 2, 5),
        (0.07 + 1j * 0.2, 5, 2, 6),
        (0.12 + 1j * 0.26, 5, 3, 5),
        (0.02 + 1j * 0.10, 2, 3, 6),
        (0.20 + 1j * 0.40, 8, 4, 5),
        (0.10 + 1j * 0.30, 6, 5, 6)]

# Montagem da matriz Ybus
ybus = zeros(n_barras, n_barras)
for item in dlin:
    bsh = item[1] / (2 * S_base)
    y = 1 / item[0]
    barra1 = item[2] - 1
    barra2 = item[3] - 1
    ybus[barra1, barra1] += y + 1j * bsh
    ybus[barra2, barra2] += y + 1j * bsh
    ybus[barra1, barra2] -= y
    ybus[barra2, barra1] -= y

# Display da matriz Ybus
lista_ybus = []
for i in range(0, n_barras):
    linha = []
    for j in range(0, n_barras):
        linha.append(roundComplex((ybus[i, j]), 4))
    lista_ybus.append(linha)

print('-' * 100)
print('Ybus')
print(tabulate(lista_ybus, tablefmt='fancy_grid', numalign="center", stralign='center'))
print('-' * 100)

# Cópia das variáveis para adequação ao código antigo
V = Tensao
Theta = Fase

# Matrizes Gbus e Bbus (Ybus = Gbus + jBbus)
gbus = re(ybus)
bbus = im(ybus)

# Listas para as equações, as variáveis, os chutes e os nomes
equacoes = []
variaveis = []
chute_variaveis = []
nomes_equacoes = []

# Acréscimo das variáveis Theta
for i in range(0, len(Tensao)):
    if Theta[i] == -1:
        Theta[i] = symbols(f"Theta{i + 1}")
        variaveis.append(symbols(f"Theta{i + 1}"))
        chute_variaveis.append((symbols(f"Theta{i + 1}"), 0))

# Acréscimo das variáveis V
for i in range(0, len(Tensao)):
    if Tensao[i] == 0:
        V[i] = symbols(f"V{i + 1}")
        variaveis.append(symbols(f"V{i + 1}"))
        chute_variaveis.append((symbols(f"V{i + 1}"), 1))

# Construção das equações deltaP
for i in range(0, n_barras):
    Pn = Pg[i] - Pl[i]
    if Pn != 0:
        expressao = Pn
        for j in range(0, n_barras):
            expressao -= V[i] * V[j] * (gbus[i, j] * cos(Theta[i] - Theta[j]) + bbus[i, j] * sin(Theta[i] - Theta[j]))
        equacoes.append(expressao)
        nomes_equacoes.append(f"deltaP{i + 1}")

# Construção das equações deltaQ
for i in range(0, n_barras):
    Qn = Qg[i] - Ql[i]
    if Qn != 0:
        expressao = Qn
        for j in range(0, n_barras):
            expressao -= V[i] * V[j] * (gbus[i, j] * sin(Theta[i] - Theta[j]) - bbus[i, j] * cos(Theta[i] - Theta[j]))
        equacoes.append(expressao)
        nomes_equacoes.append(f"deltaQ{i + 1}")

# Construção do jacobiano
jacobiano = zeros(len(equacoes), len(variaveis))
for i in range(0, len(equacoes)):
    for j in range(0, len(variaveis)):
        jacobiano[i, j] = diff(equacoes[i], variaveis[j])

print("Início do método iterativo")
print("-" * 100)
k = 0
valores_calculados = zeros(len(equacoes), 1)

# Cálculo das equações para o primeiro chute
for i in range(0, len(valores_calculados)):
    valores_calculados[i] = [equacoes[i].subs(chute_variaveis)]

# Display dos valores encontrados
print(f"Iteração {k}")
print("-" * 100)
print("Valores das variáveis")
for i in chute_variaveis:
    if str(i[0])[0] == 'V':
        print(f"{i[0]}: {i[1]:.4f} pu")
    else:
        print(f"{i[0]}: {i[1]:.4f} rad = {float(N(i[1] * 180 / pi)):.4f} [graus]")
print("Valores das equações")
for i in range(0, len(valores_calculados)):
    print(f"{nomes_equacoes[i]} = {valores_calculados[i]:.4f} pu")

while max(abs(valores_calculados)) > erro:
    jac = jacobiano.subs(chute_variaveis)
    delta = -1 * jac.inv() * valores_calculados
    novos_valores = []
    for i in range(0, len(chute_variaveis)):
        novos_valores.append((variaveis[i], chute_variaveis[i][1] + delta[i]))
    chute_variaveis = novos_valores
    for i in range(0, len(valores_calculados)):
        valores_calculados[i] = [equacoes[i].subs(chute_variaveis)]
    # Display dos ajustes
    print("Valores dos ajustes")
    for i in range(0, len(chute_variaveis)):
        if str(variaveis[i])[0] == 'V':
            print(f"delta{variaveis[i]}: {delta[i]:.4f} pu")
        else:
            print(f"delta{variaveis[i]}: {delta[i]:.4f} rad")
    k += 1
    # Display dos novos valores encontrados para as variáveis e os valores das equações
    print("-" * 100)
    print(f"Iteração {k}")
    print("-" * 100)
    print("Valores das variáveis")
    for i in chute_variaveis:
        if str(i[0])[0] == 'V':
            print(f"{i[0]}: {i[1]:.4f} pu")
        else:
            print(f"{i[0]}: {i[1]:.4f} rad = {float(N(i[1] * 180 / pi)):.4f} [graus]")
    print("Valores das equações")
    for i in range(0, len(valores_calculados)):
        print(f"{nomes_equacoes[i]} = {valores_calculados[i]:.4f} pu")
# Display do resultado final
print("-" * 100)
print(f"Resultado final")
print("-" * 100)
print("Valores das variáveis")
for i in chute_variaveis:
    if str(i[0])[0] == 'V':
        print(f"{i[0]}: {i[1]:.4f} pu")
    else:
        print(f"{i[0]}: {i[1]:.4f} rad = {float(N(i[1] * 180 / pi)):.4f} [graus]")
print("Valores das equações")
for i in range(0, len(valores_calculados)):
    print(f"{nomes_equacoes[i]} = {valores_calculados[i]:.4f} pu")
print("-" * 100)

# Atualizando os vetores de tensão e fase com os resultados encontrados
V_resultados = V
Theta_resultados = Theta

for i in range(0, len(V_resultados)):
    for j in range(0, len(chute_variaveis)):
        if V_resultados[i] == chute_variaveis[j][0]:
            V_resultados[i] = chute_variaveis[j][1]

for i in range(0, len(Theta_resultados)):
    for j in range(0, len(chute_variaveis)):
        if Theta_resultados[i] == chute_variaveis[j][0]:
            Theta_resultados[i] = chute_variaveis[j][1]

# Encontrando Pk e Qk
Pk = []
Qk = []

for i in range(0, n_barras):
    expressao1 = 0
    expressao2 = 0
    for j in range(0, n_barras):
        expressao1 += V_resultados[i] * V_resultados[j] * (gbus[i, j] * cos(Theta_resultados[i] - Theta_resultados[j]) +
                                                           bbus[i, j] * sin(Theta_resultados[i] - Theta_resultados[j]))
        expressao2 += V_resultados[i] * V_resultados[j] * (gbus[i, j] * sin(Theta_resultados[i] - Theta_resultados[j])
                                                           - bbus[i, j] * cos(
                    Theta_resultados[i] - Theta_resultados[j]))
    Pk.append(expressao1)
    Qk.append(expressao2)

# Criação da tabela com o resumo dos dados de barra
tabela1 = [['Barra', 'V [pu]', 'Theta [rad]', 'P [pu]', 'Q [pu]']]

for i in range(0, n_barras):
    linha = [i + 1, V_resultados[i], Theta_resultados[i], Pk[i], Qk[i]]
    tabela1.append(linha)

print("Tabela 1 - Resumo dos dados de barra após resolução do sistema.")
print(tabulate(tabela1, headers='firstrow', tablefmt='fancy_grid', numalign="center", floatfmt=".4f"))
print("-" * 100)

# Encontrando o fluxo de potência nas linhas
Vk, Vm, Thetak, Thetam, ykm, bshkm = symbols('Vk Vm Thetak Thetam ykm bshkm')

Pkm = Vk * Vk * re(ykm) - Vk * Vm * re(ykm) * cos(Thetak - Thetam) - Vk * Vm * im(ykm) * sin(Thetak - Thetam)
Qkm = -Vk * Vk * (im(ykm) + bshkm) + Vk * Vm * im(ykm) * cos(Thetak - Thetam) - Vk * Vm * re(ykm) * sin(Thetak - Thetam)
Pmk = Vm * Vm * re(ykm) - Vk * Vm * re(ykm) * cos(Thetak - Thetam) + Vk * Vm * im(ykm) * sin(Thetak - Thetam)



Plinha = []
Plinha2 = []
Qlinha = []
Slinha = []

for carga in dlin:
    valor1 = Pkm.subs([(Vk, V[carga[2] - 1]), (Vm, V[carga[3] - 1]), (ykm, 1 / carga[0]), (Thetak, Theta[carga[2] - 1]),
                       (Thetam, Theta[carga[3] - 1])])
    valor2 = Qkm.subs([(Vk, V[carga[2] - 1]), (Vm, V[carga[3] - 1]), (ykm, 1 / carga[0]), (Thetak, Theta[carga[2] - 1]),
                       (Thetam, Theta[carga[3] - 1]), (bshkm, carga[1] / 200)])
    valor3 = sqrt(valor1 ** 2 + valor2 ** 2)
    valor4 = Pmk.subs([(Vk, V[carga[2] - 1]), (Vm, V[carga[3] - 1]), (ykm, 1 / carga[0]), (Thetak, Theta[carga[2] - 1]),
                       (Thetam, Theta[carga[3] - 1])])
    Plinha.append(valor1)
    Qlinha.append(valor2)
    Slinha.append(valor3)
    Plinha2.append(valor4)

# Encontrando as perdas de potência ativa nas linhas
soma = 0
Perdas = []
for item in dlin:
    barra1 = item[2] - 1
    barra2 = item[3] - 1
    carga = item[0]
    V1 = V[barra1] * cos(Theta[barra1]) + I * V[barra1] * sin(Theta[barra1])
    V2 = V[barra2] * cos(Theta[barra2]) + I * V[barra2] * sin(Theta[barra2])
    queda = abs(V1 - V2)
    P = re(queda ** 2 / carga)
    soma += P
    Perdas.append(P)

# Criação da tabela com os dados de linha
tabela2 = [['Linha', 'Impedância [pu]', 'Bsh [pu]', 'Pkm [pu]', 'Pmk [pu]', 'Qkm [pu]', 'Skm [pu]', 'Perdas [pu]']]

for i in range(0, len(dlin)):
    linha = [f"{dlin[i][2]} e {dlin[i][3]}", dlin[i][0], dlin[i][1] / (2 * S_base),
             Plinha[i], Plinha2[i], Qlinha[i], Slinha[i], Perdas[i]]
    tabela2.append(linha)

print("Tabela 2 - Dados de linha após resolução do sistema")
print(tabulate(tabela2, headers='firstrow', tablefmt='fancy_grid', numalign="center", floatfmt=".4f",
               stralign="center"))
print(f"Perdas totais: {soma:.4f} pu")
print("-" * 100)

# EmpelTec Jr.
print("(c) 2024 - EmpelTec Jr. - Todos os direitos reservados")
