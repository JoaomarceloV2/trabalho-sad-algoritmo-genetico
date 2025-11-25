# Otimização de Seleção de Bolsistas (ENEM) via Algoritmo Genético

Este repositório contém a implementação de um Algoritmo Genético desenvolvido para a disciplina de Sistemas de Apoio à Decisão. O objetivo do projeto é selecionar um grupo otimizado de 100 candidatos do ENEM, maximizando simultaneamente três critérios conflitantes:
1. Performance Acadêmica (Média das Notas);
2. Diversidade Socioeconômica e Racial;
3. Cobertura Geográfica (Estados da Federação).

## Tecnologias Utilizadas
* Python 3.12
* Pandas (Manipulação de dados)
* Matplotlib e Seaborn (Visualização de dados)

## Arquivos do Projeto
* `algoritmo_genetico_enem.py`: Script principal contendo a lógica do algoritmo evolutivo e geração dos gráficos.
* `ver_colunas.py`: Script auxiliar para verificação da estrutura do dataset.

## Instruções de Execução

Para executar o projeto localmente, siga os passos abaixo:

1. Instale as dependências necessárias:
   ```bash
   pip install pandas matplotlib seaborn
Obtenção dos Dados: Devido ao tamanho do arquivo, a base de dados não está incluída neste repositório.

Baixe os Microdados do ENEM 2023 no Portal de Dados Abertos do INEP.

Extraia o arquivo MICRODADOS_ENEM_2023.csv.

Mova o arquivo CSV para a mesma pasta onde se encontra o script algoritmo_genetico_enem.py.

Execução:

Bash

python algoritmo_genetico_enem.py
Resultados Obtidos
O algoritmo demonstrou convergência robusta, atingindo um índice de aptidão (fitness) superior a 0.80. O grupo final selecionado apresentou média geral próxima a 590 pontos, com representatividade de mais de 20 unidades federativas e diversidade racial proporcional à amostra.
