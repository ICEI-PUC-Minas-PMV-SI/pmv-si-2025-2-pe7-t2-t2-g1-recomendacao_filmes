## Preparação dos Dados

A preparação dos dados para o modelo híbrido seguiu as etapas iniciais de carregamento e formatação do *dataset*, mas foi **aprimorada** para atender especificamente aos requisitos da **Filtragem Baseada em Conteúdo (TF-IDF)**, que é o "novo algoritmo" de similaridade introduzido. O modelo **Filtragem Colaborativa (SVD)** utiliza apenas o *dataframe* `ratings_df` (`userId`, `movieId`, `rating`), que é carregado no objeto `surprise.Dataset`, não exigindo pré-processamento adicional além da formatação para a biblioteca `surprise`. O foco do novo pré-processamento foi dar suporte à parte Baseada em Conteúdo do sistema híbrido.

### Ajustes e Novo Pré-processamento

| Etapa | Descrição Detalhada | Razão para o Ajuste (Diferença) |
| :--- | :--- | :--- |
| **1. Coluna `title_clean`** | Criação de uma coluna de título sem o ano (ex: 'Toy Story (1995)' $\rightarrow$ 'Toy Story'). | Essencial para a padronização e para a busca rápida de títulos na matriz de similaridade. Permite que o `indices` mapeie corretamente o título para o índice da matriz. |
| **2. `genres_space_separated`** | A coluna de gêneros (`genres`) é transformada substituindo o separador `|` por um espaço em branco. | **Crucial para o TF-IDF.** Separar por espaço permite que cada gênero seja tratado como um *token* distinto (palavra) na construção do vocabulário do modelo. |
| **3. `rich_content`** | Criação da coluna `rich_content` que, atualmente, é um *alias* para `genres_space_separated`. | Esta etapa é um ponto de **generalização** no *pipeline*. Permite que, no futuro, o modelo Baseado em Conteúdo seja enriquecido facilmente com outros metadados do filme (sinopse, atores, diretores, *tags*) sem alterar o fluxo do TF-IDF. |
| **4. Matriz TF-IDF e Similaridade** | Uso de `TfidfVectorizer` e `linear_kernel` (similaridade de cossenos) para criar a matriz de similaridade. | **Novo processamento.** O modelo híbrido depende de uma **matriz de similaridade** entre filmes. O TF-IDF pondera a importância dos termos (gêneros raros ganham mais peso) e a similaridade de cossenos mede o ângulo entre os vetores de conteúdo. |
| **5. Mapa de Índices (`indices`)** | Criação de um `pd.Series` que mapeia o `title_clean` para o índice numérico do filme no *dataframe* `movies_df` (e, consequentemente, nas matrizes `tfidf_matrix` e `cosine_sim`). | Necessário para a função híbrida, que precisa encontrar rapidamente a posição de um filme (candidato ou favorito) dentro da matriz de similaridade. |

---

## Descrição dos Modelos

O projeto implementa um **Sistema de Recomendação Híbrido** que utiliza a técnica de **Re-ranking Ponderado** (Weighted Re-ranking) para combinar a robustez da Filtragem Colaborativa com a especificidade da Filtragem Baseada em Conteúdo.

Os dois algoritmos implementados são: **SVD (Filtragem Colaborativa)** e **Similaridade de Cossenos com TF-IDF (Filtragem Baseada em Conteúdo)**.

### 1. SVD (Singular Value Decomposition) - Filtragem Colaborativa

#### Conceitos Fundamentais
O SVD é um algoritmo de **Fatoração de Matriz** que decompõe a matriz esparsa de avaliação Usuário-Item em duas matrizes menores, de baixa dimensão (fatores latentes):
* Uma matriz que representa as características latentes dos **Usuários**.
* Uma matriz que representa as características latentes dos **Itens** (Filmes).

Ao multiplicar essas matrizes, o modelo consegue prever a nota que um usuário daria a um filme que ele ainda não viu. Esses fatores latentes capturam padrões de gosto (ex: o usuário gosta de "ação com ficção científica"), mesmo que esses padrões não estejam explicitamente rotulados.

#### Justificativa da Escolha
O SVD é a **espinha dorsal (base forte)** do modelo porque é extremamente eficaz em capturar **padrões complexos de interação** entre usuários (gostos em comum, mesmo que em filmes diferentes). Ele é a melhor ferramenta para resolver o problema do **"Filme Frio"** (*Cold Start* para itens que foram avaliados, mas o conteúdo não foi enriquecido).

#### Ajuste dos Parâmetros Livres (Otimização)
Para encontrar os melhores hiperparâmetros e evitar *overfitting*, foi utilizado o **`GridSearchCV`** com **3-fold Cross-Validation** (validação cruzada). O objetivo foi minimizar o **RMSE** (Root Mean Squared Error).

| Parâmetro | Valores Testados | Melhor Valor Escolhido | Observação |
| :--- | :--- | :--- | :--- |
| `n_factors` | [50, 100] | **100** | Número de fatores latentes. 100 fatores geralmente oferece um bom equilíbrio entre expressividade do modelo e tempo de computação. |
| `n_epochs` | [20, 30] | **30** | Número de iterações. Mais épocas permitem que o modelo refine melhor o aprendizado. |
| `lr_all` | [0.005, 0.01] | **0.01** | Taxa de Aprendizado. Quão rápido os parâmetros são ajustados. Um valor maior pode acelerar a convergência, mas um valor muito alto pode causar instabilidade. |
| `reg_all` | [0.02, 0.1] | **0.1** | Regularização. Uma penalidade para evitar o *overfitting* (decoração de dados). |

**Melhores Parâmetros (RMSE):** `{'n_factors': 100, 'n_epochs': 30, 'lr_all': 0.01, 'reg_all': 0.1}`

---

### 2. TF-IDF e Similaridade de Cossenos - Filtragem Baseada em Conteúdo

#### Conceitos Fundamentais
A Filtragem Baseada em Conteúdo opera calculando a similaridade entre itens.
* **TF-IDF (`TfidfVectorizer`):** Transforma os metadados (`rich_content`/gêneros) em vetores numéricos. O TF-IDF (*Term Frequency-Inverse Document Frequency*) atribui maior peso (importância) a gêneros que são raros no *dataset* (maior poder de diferenciação).
* **Similaridade de Cossenos (`linear_kernel`):** Calcula o cosseno do ângulo entre os vetores TF-IDF de dois filmes. O valor resultante (entre 0 e 1) mede o quão similares eles são em termos de conteúdo.

#### Justificativa da Escolha
A Filtragem Baseada em Conteúdo é usada para injetar **especificidade semântica** e combater o problema do **"Usuário Frio"** (*Cold Start* para usuários com poucas avaliações) e a **super-especialização** do SVD. Ao calcular a similaridade de conteúdo do filme candidato com o **perfil de gosto médio** do usuário (baseado nos seus filmes com $\text{rating} \ge 4.5$), o modelo pode "impulsionar" filmes que são semanticamente relevantes, mesmo que o SVD não os tenha ranqueado tão alto inicialmente.

#### Mecanismo Híbrido (Re-ranking Ponderado)
A combinação é feita pela função `get_hybrid_recommendations` usando a seguinte fórmula de *boost*:

$$\text{Score Híbrido} = S_{SVD} + (\text{Similaridade Média de Conteúdo} \times \text{Peso})$$

* $S_{SVD}$ é a previsão de nota do SVD otimizado.
* **Similaridade Média de Conteúdo** é o quão parecido o filme candidato é com a média dos filmes que o usuário avaliou com notas altas ($\ge 4.5$).
* O **Peso** (`content_weight` = $0.5$) define a magnitude do *boost* de conteúdo.

O resultado é um reordenamento (*re-ranking*) dos 200 melhores candidatos do SVD.

---

## Avaliação dos Modelos Criados

A avaliação é tipicamente dividida em métricas de **previsão de nota** e métricas de **ranking** (listas Top-N).

### Métrica Principal: Precision@k (Precision at k)

| Métrica | Fórmula e Definição | Justificativa |
| :--- | :--- | :--- |
| **Precision@k** | **Resposta:** Dos $k$ filmes recomendados, quantos o usuário realmente considerou **relevantes** ($\text{rating} \ge 4.0$)? | **Alinhamento com o Objetivo:** O principal objetivo de um sistema de recomendação é entregar uma **lista concisa e de alta qualidade (o Top-N)**. A *Precision@k* mede a **eficiência** do modelo em garantir que, em uma lista curta ($k=10$), a maioria dos filmes seja realmente relevante. É crucial para a experiência do usuário, pois minimiza a chance de receber recomendações "ruins". |

### Métricas Secundárias (Previsão de Nota e Ranking)

| Métrica | Função e Uso | Justificativa |
| :--- | :--- | :--- |
| **RMSE (Root Mean Squared Error)** | Média quadrática da diferença entre a nota real ($\text{true\_r}$) e a nota prevista ($\text{est}$). | Avalia a **acurácia da previsão de nota**. É sensível a grandes erros (punição mais severa). Ideal para otimização do SVD. |
| **MAE (Mean Absolute Error)** | Média do valor absoluto da diferença entre a nota real e a nota prevista. | Mais robusta a *outliers* que o RMSE. Fornece uma medida mais intuitiva do erro médio de previsão. |
| **Recall@k** | **Resposta:** Dos filmes que o usuário gostou, quantos foram incluídos nos $k$ recomendados? | Avalia o **poder de cobertura** do modelo. Complementa o Precision@k, indicando se o modelo está encontrando uma proporção significativa dos itens que o usuário gosta. |

---

## Discussão dos Resultados Obtidos

Os resultados do **SVD Original** (não otimizado, `n_factors=100`, `n_epochs=20`) são comparados com o **SVD Otimizado** e o **Modelo Híbrido** (utilizando o SVD Otimizado como base).

| Modelo | RMSE (Erro de Nota) | MAE (Erro de Nota) | **Precision@10 (Métrica Principal)** | Recall@10 |
| :--- | :--- | :--- | :--- | :--- |
| **SVD Original** | $0.8820$ | $0.6784$ | $0.3651$ | $0.2787$ |
| **SVD Otimizado** | $0.6817$ | $0.5300$ | $\mathbf{0.4733}$ | $0.3764$ |
| **Modelo Híbrido** | N/A (Não avaliado por nota) | N/A (Não avaliado por nota) | Espera-se ser maior que SVD Otimizado | Espera-se ser maior que SVD Otimizado |

> **Nota:** O Modelo Híbrido não pode ser avaliado diretamente pelas métricas de previsão de nota (RMSE/MAE) porque a fórmula híbrida artificialmente *boosta* a nota, resultando em scores irrealisticamente altos (Score Híbrido > 5.0), o que não é uma previsão de nota verdadeira, mas sim um score de *ranking*.

### Comparação de Desempenho (Baseado na Métrica Principal: Precision@10)

* **SVD Otimizado vs. SVD Original:**
    * **Vantagem (Otimizado):** O SVD Otimizado demonstrou uma melhoria significativa no erro de previsão ($\text{RMSE}: 0.8820 \rightarrow 0.6817$) e, mais crucialmente, um aumento de $\approx 30\%$ na **Precision@10** ($\mathbf{0.3651 \rightarrow 0.4733}$). Isso valida o processo de `GridSearchCV`, mostrando que o ajuste de parâmetros (`n_epochs=30`, `reg_all=0.1`, etc.) melhorou dramaticamente a capacidade do modelo de rankear filmes relevantes no Top-10.
    * **Limitação (SVD):** Mesmo otimizado, o SVD puro ainda sofre com o **problema da especificidade**. Ele pode recomendar filmes populares ou com padrões de gosto amplos, mas pode falhar em rankear um filme de nicho que o usuário amaria, mas que poucos outros usuários semelhantes avaliaram.

* **Modelo Híbrido (Re-ranking Ponderado) vs. SVD Otimizado:**
    * **Vantagem (Híbrido):** O modelo híbrido foi criado para mitigar a limitação do SVD. Ao aplicar um ***boost* de conteúdo** (Similaridade de Gêneros) aos candidatos mais bem ranqueados pelo SVD, ele garante que filmes semanticamente próximos aos "favoritos" do usuário ($\text{rating} \ge 4.5$) sejam promovidos no *ranking* final. No contexto prático, isso aumenta a especificidade das recomendações.
    * **Limitação (Híbrido):** A eficácia do modelo híbrido depende da qualidade do **conteúdo rico**. Como o `rich_content` atual usa apenas gêneros, ele pode simplificar demais o gosto. Aumentar o peso (`content_weight`) sem um conteúdo mais rico (sinopses, atores) pode levar a **recomendações redundantes** (só filmes de um gênero específico) e diminuir a **serendipidade** (a capacidade de recomendar algo inesperado, mas bom).

### Conclusão da Discussão
O *pipeline* de otimização SVD foi bem-sucedido em reduzir o erro e aumentar a **Precision@10**. A introdução do **Modelo Híbrido** representa um refinamento do Top-N, garantindo que a lista final não só seja preditivamente acurada (graças ao SVD) mas também **semanticamente coerente** com o gosto mais forte e específico do usuário (graças ao *boost* de TF-IDF).

## Refinamento e Generalização do Pipeline (Tarefa 5)

O *pipeline* de pesquisa e análise de dados inicial é expandido para um modelo **Modular e Iterativo**, capaz de suportar o desenvolvimento, avaliação e comparação de múltiplos modelos (como o SVD, o TF-IDF e o Híbrido).

### Pipeline de Pesquisa e Análise de Dados Revisado e Generalizado

O pipeline agora é dividido em **Módulos**, permitindo que cada etapa seja revisitada e modificada de forma independente.

| Módulo | Etapas Chave | Propósito e Generalização |
| :--- | :--- | :--- |
| **0. Formulação do Problema e Objetivos** | Definir o Problema de Negócio, a Questão de Pesquisa e as **Métricas Primárias e Secundárias**. | **Generalização:** Esta etapa deve definir o **objetivo do *ranking*** (ex: maximizar Precision@k), guiando todas as escolhas subsequentes. |
| **1. Coleta e Ingestão de Dados** | Carregamento dos *datasets* brutos (`ratings_df`, `movies_df`). | **Modularidade:** Módulo de entrada que pode ser facilmente alterado para diferentes fontes de dados (API, DB, arquivos). |
| **2. Preparação de Dados e *Feature Engineering*** | Sub-etapa A: Limpeza (tratamento de *outliers* e *nulls*). Sub-etapa B: **Engenharia de Características Específicas** (CF vs CB). Sub-etapa C: Separação de Dados (Treino/Teste/Validação). | **Generalização:** Deve ser flexível para criar diferentes *datasets* de entrada para diferentes modelos (ex: dados esparsos para CF, vetores de texto para CB). |
| **3. Treinamento e Otimização de Modelos** | 3.1. Seleção de Algoritmos. 3.2. **Otimização de Hiperparâmetros** (GridSearch/Bayesiana) **vinculada à Métrica Primária**. 3.3. Treinamento Definitivo. | **Modularidade:** Garante que cada modelo ($M_1, M_2, \dots, M_N$) tenha seu próprio sub-módulo de treino e otimização. |
| **4. Avaliação e Geração de Previsões** | 4.1. Avaliação Pura (RMSE, MAE). 4.2. Avaliação de Ranking (*Precision@k*, *Recall@k*). 4.3. **Combinação/Refinamento** (Modelo Híbrido). | **Generalização:** Garante a avaliação em diferentes níveis (previsão vs. ranking), essencial em sistemas de aprendizado de máquina. |
| **5. Comparação e Análise Crítica** | Comparar o desempenho dos modelos ($M_1$ vs $M_2$ vs Híbrido) usando a métrica principal. Análise das vantagens, limitações e alinhamento com os objetivos de negócio. | **Generalização:** Módulo de decisão final sobre qual modelo (ou combinação) deve ser promovido para produção. |
| **6. Documentação e Deploy (Monitoramento Contínuo)** | Registro de todos os experimentos, *hyperparâmetros* e resultados. Estruturação do código para produção. | **Generalização:** Enfatiza a importância de documentar as decisões e o **monitoramento pós-*deploy*** (MLOps), garantindo que o modelo se adapte a mudanças nos dados. |

### Descrição das Alterações e Justificativas

As principais alterações foram a **modularização** e o foco em **múltiplas saídas de dados**, tornando o processo mais replicável:

* **Separação por Função:** O pipeline revisado separa claramente o **Treinamento (Módulo 3)** da **Avaliação/Re-ranking (Módulo 4)**. Isso permite que um modelo base (SVD Otimizado) seja treinado uma única vez e, em seguida, usado por diferentes estratégias de *ranking* (SVD puro, Híbrido com $W=0.5$, etc.), melhorando a **reutilização e modularidade**.
* **Abertura para *Feature Engineering***: A etapa **2.2 (Engenharia de Características Específicas)** foi destacada para o Enriquecimento de Conteúdo (vital para o híbrido). Isso garante que o pipeline suporte a criação de *features* especializadas para diferentes tipos de modelos (ex: *one-hot encoding* para dados categóricos, vetores TF-IDF para texto).
* **Ênfase na Métrica Principal:** O **Módulo 0** e o **Módulo 3** agora são explicitamente vinculados à Métrica Principal. Isso garante que a otimização de parâmetros (`GridSearchCV`) seja sempre direcionada ao objetivo de negócio (ex: minimizar RMSE para a previsão de nota ou maximizar Precision@k para o *ranking* final).


# Instruções de Uso do Modelo Híbrido

### Função Principal de Recomendação

A função **`get_hybrid_recommendations`** é a interface principal para obter a lista final de filmes recomendados.

| Parâmetro | Tipo | Descrição |
| :--- | :--- | :--- |
| `user_id` | `int` | **ID do usuário** para o qual as recomendações serão geradas. |
| `n` | `int` | O número de recomendações **Top-N** a serem retornadas (padrão: 10). |
| `content_weight` | `float` | **Peso** dado ao *boost* de similaridade de conteúdo no score híbrido (padrão: 0.5). |
| `rating_threshold` | `float` | **Nota mínima** para um filme ser considerado "favorito" do usuário e usado para calcular o perfil de conteúdo (padrão: 4.5). |

### Exemplo de Uso

Para obter as 10 melhores recomendações híbridas para o **Usuário 50**, usando a ponderação padrão:

```python
user_example_id = 50 
recomendacoes_finais = get_hybrid_recommendations(
    user_id=user_example_id, 
    n=10, 
    content_weight=0.5, 
    rating_threshold=4.5
)

print(f"\n--- Top 10 Recomendações HÍBRIDAS para o Usuário {user_example_id} ---")
print(recomendacoes_finais)
```

## Resultado Esperado (Exemplo de Saída)

| movieId | title_clean | genres |
| :---: | :--- | :--- |
| 1041 | Secrets & Lies | Drama |
| 1104 | Streetcar Named Desire, A | Drama |
| 1178 | Paths Of Glory | Drama |
| **...** | **...** | **...** |


## Recomendações para Ajuste

As seguintes recomendações podem ser usadas para otimizar a performance do sistema de recomendação:

* **Ajuste da Especificidade:**
    * Para tornar as recomendações mais baseadas em conteúdo (e, portanto, mais específicas aos gêneros favoritos), **aumente o `content_weight`** (ex: de `0.5` para `0.8`).

* **Ajuste da Qualidade:**
    * Para garantir que apenas os filmes mais amados do usuário influenciem o perfil de conteúdo, **aumente o `rating_threshold`** (ex: de `4.5` para `5.0`).