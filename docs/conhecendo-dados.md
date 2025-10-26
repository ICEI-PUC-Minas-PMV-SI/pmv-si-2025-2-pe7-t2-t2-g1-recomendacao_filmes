# Conhecendo os dados

Nesta seção, foi registrada uma detalhada análise descritiva e exploratória da base de dados MovieLens (ml-latest-small), com o objetivo de compreender a estrutura dos dados, detectar vieses e preparar as informações para o sistema de recomendação.

O trabalho se concentrou na análise dos datasets `movies.csv`, `ratings.csv` e `tags.csv`.

### Análise do Catálogo de Filmes (`movies.csv`)

#### Pré-processamento e Variáveis

O dataset `movies.csv` contém 9.742 filmes, sem registros nulos ou IDs duplicados.

1.  **Extração do Ano e Limpeza de Títulos:**
    * O ano de lançamento foi extraído do campo `title` e armazenado na nova coluna `year`.
    * Uma função de limpeza (`normalize_title`) foi aplicada para padronizar os títulos, removendo o ano, aplicando *Title Case* e corrigindo numerais romanos.

2.  **Codificação de Gêneros (One-Hot Encoding - OHE):**
    * A coluna `genres` foi transformada em um formato *One-Hot Encoding* (OHE), criando **19 colunas binárias**.
    * O valor `(no genres listed)` foi tratado como ausente (`NaN`) antes do OHE para evitar que se tornasse uma categoria.

#### Medidas de Centralidade e Dispersão (Gêneros)

| Métrica | Valor |
| :--- | :--- |
| Número total de filmes | 9.742 |
| Número de gêneros distintos | 19 |
| Média de gêneros por filme | 2.263 |
| **Mediana/Moda de gêneros** | **2.0** |
| Desvio padrão | 1.129 |
| Mínimo / Máximo | 0 / 10 |

* A distribuição de gêneros é concentrada em categorias simples: a maioria dos filmes possui 1 ou 2 gêneros.
* A concentração máxima de filmes (pico da distribuição) ocorre em 2 gêneros.
* Os gêneros **Drama** (4.361) e **Comédia** (3.756) são os mais representativos do catálogo.

#### Medidas de Centralidade e Dispersão (Ano de Lançamento)

| Métrica | Valor |
| :--- | :--- |
| Média dos anos | 1994.6 |
| Mediana | 1999.0 |
| Mínimo | 1902.0 |
| Máximo | 2018.0 |

* O auge da produção cinematográfica nesse dataset ocorreu entre 1995 e 2010.

---

### Análise do Dataset de Avaliações (`ratings.csv`)

#### Estrutura e Notas

* **Total de Avaliações:** 100.836.
* **Usuários únicos:** 610.
* **Filmes únicos avaliados:** 9.724.
* **Distribuição das Notas:** Média e mediana globais de **3.5**. A nota mais frequente (moda) é **4.0**. A distribuição tem um **viés positivo**.
* **Conversão Temporal:** O `timestamp` (Unix epoch) foi convertido para `datetime`, cobrindo o período de 1996-03-29 até 2018-09-24.

#### Esparsidade e Matriz Usuário-Item

* **Atividade por Filme:** A maioria dos filmes é pouco avaliada (mediana de 3 avaliações/filme).
* **Atividade por Usuário:** A distribuição é desigual. A mediana é de 70.5 avaliações/usuário, com *outliers* extremamente ativos (máximo de 2.698 avaliações).
* **Matriz Usuário-Item:** Foi construída uma matriz esparsa de 610 usuários x 9724 filmes contendo notas centralizadas (removendo o viés de nota de cada item), essencial para a **filtragem colaborativa**.

> *Trecho de Código Relevante (Centralização e Matriz Esparsa) — O código deve ser inserido aqui, conforme extraído do seu notebook original.*

---

### Análise do Dataset de Tags (`tags.csv`)

* **Estrutura:** O dataset é pequeno (3.683 tags), com apenas **58 usuários únicos** contribuindo com tags.
* **Tags Mais Frequentes:** A tag **"in netflix queue"** domina (131 ocorrências), seguida por **"atmospheric"** (41).
* **Comprimento:** As tags são, em média, curtas (mediana de 9 caracteres), mas há *outliers* com tags muito longas (máximo de 85).

***

## Descrição dos achados

A análise descritiva e exploratória revelou características cruciais para a construção do sistema de recomendação:

1.  **Viés Positivo nas Avaliações (Centralidade):** A distribuição das notas está deslocada para o lado positivo. A média (3.5) e a moda (4.0) indicam que os usuários tendem a classificar os filmes de forma favorável. Isso deve ser considerado, pois a alta frequência de notas altas pode dificultar a diferenciação de itens realmente *excelentes* em um modelo preditivo.

2.  **Esparsidade e Desigualdade de Atividade (Long Tail):** O dataset é inerentemente esparso (muitos filmes não foram avaliados).
    * **Usuários Ativos:** Uma pequena parcela dos usuários é extremamente ativa, avaliando mais de 2.000 filmes (o que inflaciona a média). Isso gera um desafio de *cold-start* e a necessidade de técnicas de **normalização** para que esses usuários não dominem os modelos.
    * **Filmes Populares:** A maioria dos filmes recebeu pouquíssimas avaliações (mediana de 3), enquanto poucos títulos concentram a maior parte do *feedback*.

3.  **Domínio de Gêneros:** O catálogo é predominantemente composto por **Drama** e **Comédia**, o que pode levar a uma tendência de concentração nas recomendações, favorecendo esses gêneros mais comuns.

4.  **Correlação:** A **similaridade de cosseno** foi utilizada como medida de correlação entre os vetores de avaliação dos filmes (após a centralização das notas). Essa é uma **correlação forte** o suficiente para ser a base do motor de recomendação (filtragem colaborativa item-item).

***

## Ferramentas utilizadas

As análises e o pré-processamento dos dados foram realizados utilizando a linguagem de programação Python.

| Ferramenta/Biblioteca | Aplicação |
| :--- | :--- |
| **Python** | Linguagem de programação principal para a análise e modelagem. |
| **`pandas`** | Estruturação e manipulação eficiente dos dados em tabelas (DataFrames). |
| **`numpy`** | Suporte para operações matemáticas e estatísticas de alto desempenho. |
| **`matplotlib.pyplot`** | Visualização de dados e geração de gráficos (histogramas, boxplots, gráficos de linha e barra). |
| **`re`** | Aplicação de expressões regulares para limpeza e padronização de textos (títulos e tags). |
| **`sklearn.preprocessing.LabelEncoder`** | Utilizada para converter IDs de usuários e filmes em índices numéricos sequenciais. |
| **`scipy.sparse.csr_matrix`** | Criação e otimização da matriz esparsa de avaliações, essencial para lidar com a esparsidade do dataset. |
| **`sklearn.metrics.pairwise.cosine_similarity`** | Cálculo da similaridade de cosseno (medida de correlação/proximidade) para a matriz de similaridade item-item. |

***

*Nota: A função `normalize_title` e a criação da matriz de similaridade (S) foram implementadas para suportar as etapas de modelagem, que utilizam a correlação e a limpeza de dados como base, conforme demonstrado na seção 'Conhecendo os dados'.*