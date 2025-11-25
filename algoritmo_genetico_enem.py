import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

ARQUIVO_ENEM = 'MICRODADOS_ENEM_2023.csv'
QTD_LEITURA = 50000  

print(f"[1/4] Lendo dados REAIS do ENEM ({ARQUIVO_ENEM})... ")


colunas_desejadas = [
    'NU_INSCRICAO', 
    'NU_NOTA_MT', 'NU_NOTA_CN', 'NU_NOTA_LC', 'NU_NOTA_CH', 
    'NU_NOTA_REDACAO',  
    'Q006',             
    'Q002',           
    'TP_ESCOLA',        
    'TP_COR_RACA',     
    'SG_UF_PROVA'       
]

try:
    df_raw = pd.read_csv(
        ARQUIVO_ENEM, 
        sep=';', 
        encoding='latin1', 
        usecols=colunas_desejadas,
        nrows=QTD_LEITURA
    )
except Exception as e:
    print(f"ERRO CRÍTICO NA LEITURA: {e}")
    exit()


df_enem = df_raw.dropna().copy()


df_enem.rename(columns={'NU_NOTA_REDACAO': 'NU_NOTA_RED', 'SG_UF_PROVA': 'SG_UF_RESIDENCIA'}, inplace=True)


df_enem['MEDIA_GERAL'] = df_enem[['NU_NOTA_MT', 'NU_NOTA_CN', 'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_RED']].mean(axis=1)
df_enem = df_enem[df_enem['MEDIA_GERAL'] > 0] 


df_enem = df_enem.reset_index(drop=True)
TOTAL_CANDIDATOS = len(df_enem)

print(f"    > Sucesso! Temos {TOTAL_CANDIDATOS} candidatos válidos.")

if TOTAL_CANDIDATOS < 200:
    print("    AVISO: Poucos candidatos. O algoritmo pode falhar se não tiver gente suficiente.")


print("\n [2/4] Configurando Algoritmo Genético... ")

TAMANHO_BOLSISTAS = 100
TAMANHO_POPULACAO = 20
GERACOES = 100
TAXA_MUTACAO = 0.1


QT_ESTADOS = df_enem['SG_UF_RESIDENCIA'].nunique()
QT_RACAS = df_enem['TP_COR_RACA'].nunique()
QT_RENDAS = df_enem['Q006'].nunique()

def calcular_fitness(indices_grupo):
    grupo = df_enem.iloc[indices_grupo]
    

    score_performance = grupo['MEDIA_GERAL'].mean() / 850
    if score_performance > 1: score_performance = 1
    

    div_raca = grupo['TP_COR_RACA'].nunique() / QT_RACAS if QT_RACAS > 0 else 0
    div_renda = grupo['Q006'].nunique() / QT_RENDAS if QT_RENDAS > 0 else 0
    score_diversidade = (div_raca + div_renda) / 2
    

    score_regiao = grupo['SG_UF_RESIDENCIA'].nunique() / QT_ESTADOS if QT_ESTADOS > 0 else 0
    
    fitness = (0.5 * score_performance) + (0.3 * score_diversidade) + (0.2 * score_regiao)
    return fitness

def criar_individuo():
    return random.sample(range(TOTAL_CANDIDATOS), TAMANHO_BOLSISTAS)

def crossover(pai1, pai2):
    corte = TAMANHO_BOLSISTAS // 2
    filho = pai1[:corte] + [x for x in pai2 if x not in pai1[:corte]]
    while len(filho) < TAMANHO_BOLSISTAS:
        novo = random.randint(0, TOTAL_CANDIDATOS - 1)
        if novo not in filho: filho.append(novo)
    return filho[:TAMANHO_BOLSISTAS]

def mutacao(individuo):
    if random.random() < TAXA_MUTACAO:
        idx_troca = random.randint(0, TAMANHO_BOLSISTAS - 1)
        novo = random.randint(0, TOTAL_CANDIDATOS - 1)
        while novo in individuo: novo = random.randint(0, TOTAL_CANDIDATOS - 1)
        individuo[idx_troca] = novo
    return individuo

# EXECUCAO
print(f"\n [3/4] Executando Evolução ({GERACOES} Gerações)... ")

populacao = [criar_individuo() for _ in range(TAMANHO_POPULACAO)]
historico_fitness = []

for geracao in range(GERACOES):
    scores = [(ind, calcular_fitness(ind)) for ind in populacao]
    scores.sort(key=lambda x: x[1], reverse=True)
    
    melhor_fitness = scores[0][1]
    historico_fitness.append(melhor_fitness)
    
    if geracao % 10 == 0:
        print(f"   > Geração {geracao}: Melhor Fitness = {melhor_fitness:.4f}")
    
    nova_pop = [scores[0][0], scores[1][0]] 
    
    while len(nova_pop) < TAMANHO_POPULACAO:
        pai1 = random.choice(scores[:10])[0]
        pai2 = random.choice(scores[:10])[0]
        filho = mutacao(crossover(pai1, pai2))
        nova_pop.append(filho)
    populacao = nova_pop

grupo_campeao_indices = scores[0][0]
df_final = df_enem.iloc[grupo_campeao_indices]

print("\n FIM! Resultado Final ")
print(f"Melhor Fitness: {scores[0][1]:.4f}")
print(f"Média Geral do Grupo: {df_final['MEDIA_GERAL'].mean():.2f}")
print(f"Estados Cobertos: {df_final['SG_UF_RESIDENCIA'].nunique()}")

print("\n [4/4] Gerando Gráficos... ")
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(historico_fitness, color='blue')
plt.title('Evolução do Fitness')
plt.xlabel('Geração')

plt.subplot(1, 3, 2)
sns.histplot(df_final['MEDIA_GERAL'], kde=True, color='green')
plt.title('Notas dos Bolsistas Selecionados')

plt.subplot(1, 3, 3)
df_final['TP_COR_RACA'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Diversidade Racial')
plt.ylabel('')

plt.tight_layout()
plt.show()