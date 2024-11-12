from sympy import *


def MaxAbsLista(lista):
    maior = 0
    for i in range(len(lista)):
        if i == 0:
            maior = abs(lista[i])
        else:
            valor = abs(lista[i])
            if valor > maior:
                maior = valor
    return maior


def FluxoDeCarga(carregamento):
    S_base = 100
    erro = 0.0001
    n_barras = 6
    Pg = [0, 1.4, 0.6, 0, 0, 0]
    Pl = [0, 0, 0, 0.9, 1, 0.9]
    Qg = [0, 0, 0, 0, 0, 0]
    Ql = [0, 0, 0, 0.6, 0.7, 0.6]
    Tensao = [1.1, 1.1, 1.1, 0, 0, 0]
    Fase = [0, -1, -1, -1, -1, -1]
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
    V = Tensao
    Theta = Fase
    gbus = re(ybus)
    bbus = im(ybus)
    equacoes = []
    variaveis = []
    chute_variaveis = []
    nomes_equacoes = []
    for i in range(0, len(Tensao)):
        if Theta[i] == -1:
            Theta[i] = symbols(f"Theta{i + 1}")
            variaveis.append(symbols(f"Theta{i + 1}"))
            chute_variaveis.append((symbols(f"Theta{i + 1}"), 0))
    for i in range(0, len(Tensao)):
        if Tensao[i] == 0:
            V[i] = symbols(f"V{i + 1}")
            variaveis.append(symbols(f"V{i + 1}"))
            chute_variaveis.append((symbols(f"V{i + 1}"), 1))
    for i in range(0, n_barras):
        Pn = (1 + carregamento) * (Pg[i] - Pl[i])
        if Pn != 0:
            expressao = Pn
            for j in range(0, n_barras):
                expressao -= V[i] * V[j] * (
                        gbus[i, j] * cos(Theta[i] - Theta[j]) + bbus[i, j] * sin(Theta[i] - Theta[j]))
            equacoes.append(expressao)
            nomes_equacoes.append(f"deltaP{i + 1}")
    for i in range(0, n_barras):
        Qn = Qg[i] - Ql[i]*(1 + carregamento)
        if Qn != 0:
            expressao = Qn
            for j in range(0, n_barras):
                expressao -= V[i] * V[j] * (
                        gbus[i, j] * sin(Theta[i] - Theta[j]) - bbus[i, j] * cos(Theta[i] - Theta[j]))
            equacoes.append(expressao)
            nomes_equacoes.append(f"deltaQ{i + 1}")
    jacobiano = zeros(len(equacoes), len(variaveis))
    for i in range(0, len(equacoes)):
        for j in range(0, len(variaveis)):
            jacobiano[i, j] = diff(equacoes[i], variaveis[j])
    k = 0
    valores_calculados = zeros(len(equacoes), 1)
    for i in range(0, len(valores_calculados)):
        valores_calculados[i] = [equacoes[i].subs(chute_variaveis)]
    while max(abs(valores_calculados)) > erro:
        jac = jacobiano.subs(chute_variaveis)
        print(jac.det())
        delta = -1 * jac.inv() * valores_calculados
        novos_valores = []
        for i in range(0, len(chute_variaveis)):
            novos_valores.append((variaveis[i], chute_variaveis[i][1] + delta[i]))
        chute_variaveis = novos_valores
        for i in range(0, len(valores_calculados)):
            valores_calculados[i] = [equacoes[i].subs(chute_variaveis)]
        k += 1
        if k > 100:
            return False, [0, 0, 0, 0, 0, 0]
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
    Qk = []
    for i in range(0, 3):
        expressao = 0
        for j in range(0, n_barras):
            expressao += V_resultados[i] * V_resultados[j] * (gbus[i, j] * sin(Theta_resultados[i] - Theta_resultados[j]) - bbus[i, j] * cos(Theta_resultados[i] - Theta_resultados[j]))
        Qk.append(expressao)
    return True, V_resultados, Qk


def FluxoDeCargaLimitado(carregamento, V1=1.1, V2=1.1, V3=1.1, Qg1=0, Qg2=0, Qg3=0):
    S_base = 100
    erro = 0.0001
    n_barras = 6
    Pg = [0, 1.4, 0.6, 0, 0, 0]
    Qg = [Qg1, Qg2, Qg3, 0, 0, 0]
    Pl = [0, 0, 0, 0.9, 1, 0.9]
    Ql = [0, 0, 0, 0.6, 0.7, 0.6]
    Tensao = [V1, V2, V3, 0, 0, 0]
    Fase = [0, -1, -1, -1, -1, -1]
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
    V = Tensao
    Theta = Fase
    gbus = re(ybus)
    bbus = im(ybus)
    equacoes = []
    variaveis = []
    chute_variaveis = []
    nomes_equacoes = []
    for i in range(0, len(Tensao)):
        if Theta[i] == -1:
            Theta[i] = symbols(f"Theta{i + 1}")
            variaveis.append(symbols(f"Theta{i + 1}"))
            chute_variaveis.append((symbols(f"Theta{i + 1}"), 0))
    for i in range(0, len(Tensao)):
        if Tensao[i] == 0:
            V[i] = symbols(f"V{i + 1}")
            variaveis.append(symbols(f"V{i + 1}"))
            chute_variaveis.append((symbols(f"V{i + 1}"), 1))
    for i in range(0, n_barras):
        Pn = (1 + carregamento) * (Pg[i] - Pl[i])
        if Pn != 0:
            expressao = Pn
            for j in range(0, n_barras):
                expressao -= V[i] * V[j] * (
                        gbus[i, j] * cos(Theta[i] - Theta[j]) + bbus[i, j] * sin(Theta[i] - Theta[j]))
            equacoes.append(expressao)
            nomes_equacoes.append(f"deltaP{i + 1}")
    for i in range(0, n_barras):
        Qn = Qg[i] - Ql[i]*(1+carregamento)
        if Qn != 0:
            expressao = Qn
            for j in range(0, n_barras):
                expressao -= V[i] * V[j] * (
                        gbus[i, j] * sin(Theta[i] - Theta[j]) - bbus[i, j] * cos(Theta[i] - Theta[j]))
            equacoes.append(expressao)
            nomes_equacoes.append(f"deltaQ{i + 1}")
    jacobiano = zeros(len(equacoes), len(variaveis))
    for i in range(0, len(equacoes)):
        for j in range(0, len(variaveis)):
            jacobiano[i, j] = diff(equacoes[i], variaveis[j])
    k = 0
    valores_calculados = zeros(len(equacoes), 1)
    for i in range(0, len(valores_calculados)):
        valores_calculados[i] = [equacoes[i].subs(chute_variaveis)]
    while max(abs(valores_calculados)) > erro:
        jac = jacobiano.subs(chute_variaveis)
        delta = -1 * jac.inv() * valores_calculados
        novos_valores = []
        for i in range(0, len(chute_variaveis)):
            novos_valores.append((variaveis[i], chute_variaveis[i][1] + delta[i]))
        chute_variaveis = novos_valores
        for i in range(0, len(valores_calculados)):
            valores_calculados[i] = [equacoes[i].subs(chute_variaveis)]
        k += 1
        if k > 100:
            return False, [0, 0, 0, 0, 0, 0]
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
    Qk = []
    for i in range(0, 3):
        expressao = 0
        for j in range(0, n_barras):
            expressao += V_resultados[i] * V_resultados[j] * (gbus[i, j] * sin(Theta_resultados[i] - Theta_resultados[j]) - bbus[i, j] * cos(Theta_resultados[i] - Theta_resultados[j]))
        Qk.append(expressao)
    if round(MaxAbsLista(Qk), 4) <= 1.5:
        return True, V_resultados, Qk
    else:
        novo_Tensao = [V1, V2, V3, 0, 0, 0]
        novo_Qg = [Qg1, Qg2, Qg3, 0, 0, 0]
        for i in range(len(Qk)):
            if Qk[i] > 1.5:
                novo_Tensao[i] = 0
                novo_Qg[i] = 1.5
            elif Qk[i] < -1.5:
                novo_Tensao[i] = 0
                novo_Qg[i] = -1.5
        return FluxoDeCargaLimitado(carregamento, novo_Tensao[0], novo_Tensao[1], novo_Tensao[2], novo_Qg[0],
                                    novo_Qg[1], novo_Qg[2])
