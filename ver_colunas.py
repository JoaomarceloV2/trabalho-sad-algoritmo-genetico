import pandas as pd

ARQUIVO = 'MICRODADOS_ENEM_2023.csv'

try:
 
    print("--- Tentando ler com ponto e vírgula (;) ---")
    df = pd.read_csv(ARQUIVO, sep=';', encoding='latin1', nrows=0)
    

    colunas = list(df.columns)
    print("Separador correto! Aqui estão as colunas:")
    print(colunas)
    

    print("\n--- Verificação ---")
    if 'SG_UF_RESIDENCIA' in colunas: print("✅ SG_UF_RESIDENCIA encontrado!")
    else: print("❌ SG_UF_RESIDENCIA NÃO achado.")
    
    if 'NU_NOTA_RED' in colunas: print("✅ NU_NOTA_RED encontrado!")
    else: print("❌ NU_NOTA_RED NÃO achado (será que mudou de nome?)")

except:
    print("\nERRO: O separador não parece ser ponto e vírgula (;).")
    print("Tentando com vírgula (,)...")
    try:
        df = pd.read_csv(ARQUIVO, sep=',', encoding='latin1', nrows=0)
        print("Separador é VÍRGULA! Colunas:")
        print(list(df.columns))
    except Exception as e:
        print(f"Não consegui ler o arquivo. Erro: {e}")