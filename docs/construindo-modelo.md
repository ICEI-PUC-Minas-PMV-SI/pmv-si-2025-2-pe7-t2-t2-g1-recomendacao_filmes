# Preparação dos dados

Nesta etapa, foram utilizadas técnicas de pré-processamento/tratamento de dados focadas em adaptar os DataFrames originais para o uso com bibliotecas específicas de sistemas de recomendação, como `surprise` (para Filtragem Colaborativa) e `sklearn` (para Filtragem Baseada em Conteúdo).

### Transformação e Separação de Dados (Filtragem Colaborativa)

1.  **Carregamento de Dados Pré-Processados:**
    * Os datasets `ratings_processed.csv` e `movies_processed.csv` foram carregados, assumindo que já continham limpeza de dados e *feature engineering* básicas (como a limpeza de títulos e a codificação de gêneros) realizadas em etapas anteriores.

2.  **Definição do Formato `surprise`:**
    * Para o algoritmo SVD, foi necessário definir o `Reader` que especifica a escala das avaliações, de **0.5 a 5 estrelas**.
    * Os dados de avaliação foram carregados para o objeto `Dataset` da biblioteca `surprise`, utilizando apenas as colunas essenciais: `userId`, `movieId` e `rating`.

3.  **Separação de Dados:**
    * O conjunto de dados foi dividido de forma reprodutível (usando `random_state=42`) em conjuntos de treinamento (75%) e teste (25%) para a avaliação inicial do modelo.

### Preparação de Dados (Filtragem Baseada em Conteúdo)

Para o componente de conteúdo (gêneros), foram aplicadas técnicas de processamento de texto para medir a similaridade entre os filmes:

* **Vetores de Recurso (Feature Engineering):** A coluna de gêneros (`genres`), que utiliza o separador `|`, foi transformada, substituindo o separador por um espaço para que pudesse ser tratada como um *corpus* de texto.
* **Transformação TF-IDF:** O `TfidfVectorizer` foi utilizado para criar uma matriz TF-IDF (Term Frequency-Inverse Document Frequency) a partir dos gêneros. Isso transforma os gêneros em vetores numéricos que ponderam a importância de cada gênero, sendo a base para o cálculo de similaridade.

***

# Descrição do modelo

O sistema de recomendação desenvolvido é um **Modelo Híbrido** que combina a precisão da **Filtragem Colaborativa** com a capacidade de diversificação da **Filtragem Baseada em Conteúdo**.

### Algoritmo de Filtragem Colaborativa: SVD

#### Conceito e Funcionamento:
O SVD (Singular Value Decomposition) é um método de fatoração de matriz que decompõe a esparsa matriz Usuário-Item em três matrizes menores. Ele busca identificar **fatores latentes** que explicam as avaliações dos usuários. Esses fatores podem representar características ocultas (como "filmes de ação e ficção científica" ou "filmes românticos e dramáticos") que influenciam o gosto dos usuários. O modelo aprende a preferência de cada usuário por esses fatores latentes e, em seguida, usa isso para prever a nota que um usuário daria a um item que ele nunca viu.

#### Ajuste de Parâmetros (Primeiro Experimento):

* `n_factors`: 100 (Número de fatores latentes).
* `n_epochs`: 20 (Número de iterações do algoritmo).
* `random_state`: 42 (Garantia de reprodutibilidade).

#### Ajuste de Parâmetros (Modelo Final Otimizado):
O modelo final de SVD foi treinado com parâmetros otimizados (assumindo a conclusão de um GridSearch/ajuste de hiperparâmetros):

* `n_epochs`: 30
* `lr_all` (Taxa de aprendizado): 0.01
* `reg_all` (Termo de regularização): 0.1

### Modelo Híbrido (Re-ranking)

A abordagem final utiliza um **Híbrido de Re-ranking**:

1.  **Candidatos SVD:** O SVD Otimizado gera os 100 melhores filmes com base na nota predita para o usuário (`svd_score`).
2.  **Similaridade de Conteúdo:** O filme favorito do usuário (maior nota) é identificado, e a **Similaridade de Cosseno** baseada em gêneros é calculada entre esse filme favorito e cada candidato SVD (`content_similarity`).
3.  **Boost e Re-ranking:** Um *boost* de `0.5` multiplicado pela similaridade de conteúdo é adicionado ao `svd_score`. O resultado é um `hybrid_score` que favorece filmes não só preditos como "bons" (pelo SVD) mas também "parecidos" com os que o usuário mais gostou (por Gênero). O top N é então selecionado a partir desse novo *score* híbrido.

***

# Avaliação do modelo criado

## Métricas utilizadas

A avaliação do modelo SVD foi realizada utilizando métricas de erro de predição e métricas baseadas na qualidade do *top N* de recomendação.

| Métrica | Tipo | Justificativa |
| :--- | :--- | :--- |
| **RMSE** (Root Mean Squared Error) | Erro de Predição | Mede o desvio quadrático médio. É a métrica mais comum para sistemas de recomendação baseados em predição de nota e é mais sensível a erros grandes. |
| **MAE** (Mean Absolute Error) | Erro de Predição | Mede a diferença absoluta média entre a nota prevista e a real. É menos sensível a *outliers* que o RMSE, fornecendo uma visão mais robusta do erro médio. |
| **Precision@k** (k=10, Threshold $\ge 4.0$) | Qualidade de *Ranking* | Mede a proporção de recomendações no Top-10 que são realmente relevantes (notas $\ge 4.0$). É crucial para avaliar a relevância do *ranking* de saída. |
| **Recall@k** (k=10, Threshold $\ge 4.0$) | Qualidade de *Ranking* | Mede a proporção de todos os itens relevantes (notas $\ge 4.0$) que foram incluídos no Top-10. É útil para medir o quanto o modelo "lembra" dos bons filmes para o usuário. |

## Discussão dos resultados obtidos

A avaliação do modelo SVD (não otimizado, no conjunto de teste) forneceu os seguintes resultados:

| Métrica | Valor Obtido |
| :--- | :--- |
| **RMSE** | 0.8820 |
| **MAE** | 0.6784 |
| **Precision@10** | 0.3651 |
| **Recall@10** | 0.2787 |

* **Qualidade de Predição (RMSE/MAE):** Os valores de erro de **0.8820 (RMSE)** e **0.6784 (MAE)** demonstram que o modelo SVD é capaz de prever as notas de forma consistente e com um erro relativamente baixo em uma escala de 0.5 a 5.0. O erro absoluto médio de **0.68** é aceitável, indicando que a filtragem colaborativa é uma base sólida.
* **Qualidade de Relevância (Precision/Recall):**
    * **Precision@10 (36.51%):** Sugere que, em média, cerca de 36.5% dos filmes recomendados no Top-10 são, de fato, filmes que o usuário gostaria (nota $\ge 4.0$). Este valor é razoável, mas indica margem para melhoria na taxa de acerto do ranking.
    * **Recall@10 (27.87%):** Mostra que o modelo está perdendo uma parte significativa dos filmes relevantes do usuário (apenas cerca de 28% são capturados no Top-10). Isso é esperado, dada a alta esparsidade da matriz.

Em relação à **questão de pesquisa** levantada na etapa anterior (*"É possível antecipar os gostos... combinando técnicas...?"*):
O SVD puro já provou ser eficaz na predição de notas. A introdução do **modelo híbrido** (que não foi avaliado por essas métricas de classificação no notebook, mas sim por exemplo prático) visa mitigar a baixa cobertura do *Recall* e a falta de diversidade, buscando incorporar o gosto explícito (gêneros) nos filmes que o SVD já prediz como promissores. O *re-ranking* híbrido é a resposta prática para tentar melhorar a relevância percebida das recomendações, indo além da simples predição de notas.

***

# Pipeline de pesquisa e análise de dados

O pipeline de pesquisa e análise de dados para a construção do modelo seguiu as seguintes etapas:

1.  **Preparação de Dados para SVD:** Carregamento, definição da escala de notas (`Reader`) e criação do objeto `Dataset` para a biblioteca `surprise`.
2.  **Separação de Dados:** Divisão em conjunto de treinamento e teste (75%/25%) para avaliação inicial do SVD.
3.  **Modelagem Colaborativa:** Treinamento do modelo SVD com parâmetros iniciais (`n_factors=100`, `n_epochs=20`).
4.  **Avaliação:** Cálculo das métricas de erro (RMSE, MAE) e de *ranking* (Precision@k, Recall@k) no conjunto de teste.
5.  **Preparação de Conteúdo:** Aplicação de TF-IDF nos gêneros e cálculo da Matriz de Similaridade de Cosseno entre filmes.
6.  **Modelagem Híbrida Final:**
    * Treinamento do modelo SVD Otimizado no conjunto de dados completo (`full trainset`).
    * Implementação da função de **Recomendação Híbrida** (SVD score + *Content Boost* baseado no filme favorito do usuário) para gerar as recomendações finais.

## Observações importantes

Todas as tarefas de modelagem e avaliação foram realizadas em Python, utilizando as bibliotecas `surprise` e `sklearn`, e os códigos completos para o treinamento do SVD e a função de recomendação híbrida estão documentados no notebook, e devem ser incluídos na pasta "src" para replicabilidade.