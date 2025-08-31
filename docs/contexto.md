# Introdução

Os sistemas de recomendação desempenham um papel fundamental na forma como interagimos com conteúdos digitais, especialmente em plataformas de streaming, comércio eletrônico e redes sociais. Essas ferramentas têm como principal objetivo prever as preferências dos usuários e oferecer sugestões personalizadas, aumentando tanto a satisfação quanto o engajamento. Nesse cenário, o conjunto de dados MovieLens (ml-latest-small) surge como um recurso de grande relevância para pesquisas e experimentos voltados ao desenvolvimento de algoritmos de recomendação, fornecendo informações sobre avaliações, marcações (tags) e características de filmes.

Este trabalho tem como propósito construir e avaliar um sistema de recomendação utilizando o dataset MovieLens, aplicando técnicas de filtragem colaborativa e filtragem baseada em conteúdo. A análise envolve desde a exploração e preparação dos dados até a implementação de modelos capazes de prever avaliações e sugerir filmes personalizados aos usuários. A escolha desse conjunto de dados se justifica por sua ampla utilização na comunidade acadêmica, sua riqueza de informações e pela oportunidade de aplicar métodos de aprendizado de máquina em um contexto prático e realista.

O público-alvo deste estudo inclui estudantes, pesquisadores e profissionais da área de Ciência de Dados interessados em compreender e implementar sistemas de recomendação, bem como equipes de produto e engenharia que visam melhorar a experiência do usuário em plataformas digitais. Dessa forma, este projeto busca aliar conhecimento teórico e aplicação prática, contribuindo para o entendimento e aprimoramento de soluções de personalização baseadas em dados.

## Problema

O crescimento acelerado do volume de conteúdos audiovisuais disponíveis em plataformas digitais torna cada vez mais difícil para os usuários decidirem o que assistir. A simples disponibilização de catálogos extensos, sem mecanismos inteligentes de filtragem, resulta em uma experiência de navegação pouco eficiente, levando à dispersão do usuário e, em muitos casos, à insatisfação. Nesse cenário, surge a necessidade de sistemas de recomendação capazes de prever as preferências individuais e sugerir filmes de forma personalizada.

O conjunto de dados MovieLens (ml-latest-small) fornece uma base adequada para enfrentar esse desafio, pois reúne informações sobre avaliações e tags aplicadas a milhares de filmes por centenas de usuários. O problema que este projeto busca resolver é justamente a criação de um modelo capaz de prever as avaliações de usuários e recomendar filmes que atendam às suas preferências, explorando tanto a filtragem colaborativa quanto a filtragem baseada em conteúdo.

O contexto de aplicação deste estudo se insere no domínio dos sistemas de recomendação para plataformas de mídia e entretenimento, como serviços de streaming de filmes. Embora o projeto tenha caráter acadêmico e experimental, suas abordagens e resultados podem ser utilizados como base para soluções reais que visam aumentar o engajamento, a retenção e a satisfação do usuário por meio de recomendações mais assertivas.

## Questão de pesquisa

A questão de pesquisa é o ponto de partida e a base orientadora de todo o trabalho a ser desenvolvido. Ela deve estar diretamente alinhada ao problema identificado e expressar, de forma clara, o que se deseja investigar ou comprovar.

O papel da questão de pesquisa é guiar todas as etapas do projeto — desde a definição da metodologia até a análise e interpretação dos resultados. Ao término da investigação ou experimentação, o objetivo é que seja possível responder a essa questão de forma fundamentada, utilizando evidências obtidas ao longo do processo.

**Dica:** Formule a questão de pesquisa de forma específica e objetiva, evitando perguntas muito amplas ou genéricas. Pergunte-se: "Ao final do trabalho, minha pesquisa terá condições de responder claramente a essa pergunta?"

> **Links Úteis**:
> - [Questão de pesquisa](https://www.enago.com.br/academy/how-to-develop-good-research-question-types-examples/)
> - [Problema de pesquisa](https://blog.even3.com.br/problema-de-pesquisa/)

## Objetivos preliminares

**Objetivo Geral**

Desenvolver e avaliar um sistema de recomendação de filmes utilizando o conjunto de dados MovieLens (ml-latest-small), aplicando modelos de aprendizado de máquina adequados para prever avaliações de usuários e gerar recomendações personalizadas. O sistema deverá explorar tanto a filtragem colaborativa quanto a filtragem baseada em conteúdo, permitindo sugerir filmes que atendam às preferências individuais.

## Justificativa

A escolha do conjunto de dados MovieLens (ml-latest-small) justifica-se por sua ampla utilização em pesquisas acadêmicas e práticas relacionadas a sistemas de recomendação. Criado pelo grupo GroupLens da Universidade de Minnesota, esse dataset fornece informações organizadas sobre avaliações e preferências de usuários, o que permite explorar diferentes abordagens de filtragem colaborativa e baseada em conteúdo. Embora seja uma versão reduzida, contendo 100.836 avaliações, 3.683 tags, 9.742 filmes e 610 usuários, ele é suficientemente representativo para a realização de experimentos consistentes e controlados.

O estudo desse problema é relevante tanto no contexto acadêmico, por possibilitar a aplicação prática de técnicas de Ciência de Dados e Machine Learning, quanto no profissional, já que sistemas de recomendação são amplamente utilizados em plataformas digitais. Empresas como Netflix e Amazon investem bilhões de dólares anualmente em tecnologias de recomendação, e estimativas da McKinsey (2013) indicam que cerca de 35% das vendas da Amazon e 75% do que é assistido na Netflix são resultado direto de recomendações automatizadas. Esses números evidenciam o impacto econômico e estratégico dessas ferramentas.

Além disso, compreender e desenvolver modelos eficazes de recomendação tem também um impacto social, pois ajuda usuários a encontrarem conteúdos mais relevantes em meio a grandes volumes de informação, reduzindo a sobrecarga cognitiva e aumentando a satisfação com os serviços digitais. Do ponto de vista econômico, a aplicação de tais modelos melhora métricas essenciais como retenção, engajamento e tempo de permanência em plataformas de mídia, aspectos cruciais para a sustentabilidade financeira dessas empresas.

Assim, os objetivos específicos do projeto — prever avaliações de usuários e recomendar filmes personalizados — foram definidos para responder de forma direta ao problema identificado: a dificuldade de selecionar conteúdos relevantes em grandes catálogos digitais. A investigação nesse contexto contribui para o avanço da área de sistemas de recomendação, com potencial de aplicação tanto em ambientes de pesquisa quanto em soluções práticas voltadas ao mercado de entretenimento e tecnologia.

## Público-Alvo

Nesta seção, descreva quem poderá se beneficiar com a sua investigação, apresentando os diferentes perfis de pessoas ou grupos impactados.

O objetivo aqui não é definir clientes específicos ou papéis exatos dentro da aplicação, mas sim compreender o perfil dos usuários e partes interessadas. Para isso, considere:
* Conhecimentos prévios relacionados ao domínio do problema e ao uso de tecnologia;
* Nível de familiaridade com recursos digitais e possíveis barreiras de uso;
* Contexto profissional e hierárquico, quando aplicável (ex.: nível de decisão, responsabilidades, área de atuação);
* Necessidades e expectativas que podem ser atendidas pelo projeto.

**Dica:** Seja objetivo e baseie suas descrições em informações reais ou plausíveis para o contexto escolhido. Isso ajudará a manter o foco no desenvolvimento de soluções relevantes e aplicáveis.

> **Links Úteis**:
> - [Público-alvo](https://blog.hotmart.com/pt-br/publico-alvo/)
> - [Como definir o público alvo](https://exame.com/pme/5-dicas-essenciais-para-definir-o-publico-alvo-do-seu-negocio/)
> - [Público-alvo: o que é, tipos, como definir seu público e exemplos](https://klickpages.com.br/blog/publico-alvo-o-que-e/)
> - [Qual a diferença entre público-alvo e persona?](https://rockcontent.com/blog/diferenca-publico-alvo-e-persona/)

## Estado da arte

Trabalhos Relacionados
1. Sistema de Recomendação com Filtragem baseada em Conteúdo e Colaborativa

Problema e contexto: Desenvolvimento de sistema de recomendação de filmes para previsão de avaliações e sugestões personalizadas.

Dataset: MovieLens 1M; 1 milhão de avaliações de 6.040 usuários sobre 3.700 filmes.

Abordagem: Filtragem colaborativa via fatoração de matrizes; filtragem baseada em conteúdo utilizando gênero, diretores e atores.

Métricas: RMSE para avaliação de previsões; precisão das recomendações.

Resultados: Conclusão de que a combinação de filtragem colaborativa e baseada em conteúdo melhora a acurácia e a relevância das recomendações.

2. Sistema de Recomendação com Opiniões de Usuários e SVD

Problema e contexto: Previsão de preferências em produtos da Amazon, utilizando avaliações e opiniões de usuários.

Dataset: Amazon Reviews; informações de usuários, produtos e avaliações (texto e notas).

Abordagem: Filtragem colaborativa com SVD; Processamento de Linguagem Natural (NLP) para analisar sentimento das opiniões.

Métricas: RMSE para previsões numéricas; análise qualitativa de sentimento.

Resultados: Integração de NLP melhora compreensão do comportamento do usuário; limitações incluem complexidade de processamento de texto.

3. Sistema de Recomendação de Livros com Embeddings de Redes Neurais

Problema e contexto: Recomendação de livros a partir de artigos da Wikipédia e links internos.

Dataset: Dados da Wikipédia sobre livros e links; atributos textuais e relacionais.

Abordagem: Embeddings de redes neurais para representar livros e links em espaço vetorial; classificação supervisionada para prever presença de links.

Métricas: Acurácia na classificação supervisionada; proximidade vetorial como medida de similaridade.

Resultados: Modelos de embedding permitem identificar livros semelhantes; limitação na dependência de dados textuais.

4. Sistema de Recomendação de Filmes – Linha de Base

Problema e contexto: Criação de recomendações simples para filmes utilizando abordagens básicas.

Dataset: TMDB 5000 Movie Dataset; títulos, gêneros, elenco e metadados de filmes.

Abordagem: Recomendação baseada em popularidade e filtragem básica por conteúdo ou colaborativa.

Métricas: Precisão das listas de recomendações; comparações com métodos mais complexos.

Resultados: Sistemas simples funcionam bem em cenários de pequeno porte, mas possuem limitação em personalização.

5. Sistema de Recomendação com Múltiplas Abordagens

Problema e contexto: Comparação de diferentes estratégias de recomendação para prever avaliações e sugerir filmes.

Dataset: MovieLens Full Dataset (26 milhões de avaliações) e Small Dataset (100 mil avaliações); metadados do TMDB.

Abordagem: Popularidade ponderada, filtragem baseada em conteúdo, filtragem colaborativa.

Métricas: RMSE, precisão, recall.

Resultados: Modelos híbridos combinando abordagens distintas obtêm melhores resultados; destaca-se importância de balancear popularidade e personalização.

Síntese Crítica

Os estudos analisados concordam que a combinação de filtragem colaborativa e baseada em conteúdo aumenta significativamente a precisão e a relevância das recomendações em relação a abordagens isoladas. Divergências aparecem no tipo de dados utilizados: alguns trabalhos focam em avaliações explícitas (MovieLens, Amazon), enquanto outros exploram textos ou metadados (livros, TMDB).

As lacunas ainda existentes incluem a generalização para novos usuários e itens (cold start), a limitação de dados demográficos e contexto social, e desafios técnicos relacionados à esparsidade e escalabilidade das matrizes de avaliação. Além disso, poucos trabalhos exploram métricas qualitativas de satisfação do usuário ou impactos éticos de sistemas de recomendação.

O projeto em desenvolvimento se alinha a esses estudos ao implementar um modelo híbrido de recomendação, utilizando filtragem colaborativa e baseada em conteúdo, com o objetivo de prever avaliações e gerar listas personalizadas. Assim, pretende-se explorar o potencial do dataset MovieLens ml-latest-small para validar modelos em cenários acadêmicos e simulações de plataformas de streaming, contribuindo para o estudo de estratégias híbridas e avaliação de desempenho em sistemas de recomendação.

# Descrição do _dataset_ selecionado

Identificação e origem

O conjunto de dados utilizado é o MovieLens Small Latest Dataset, hospedado na plataforma Kaggle pelo usuário Shubham Mehta Kaggle+1. Ele é uma versão reduzida da base oficial do MovieLens e está disponível em formato CSV, com aproximadamente 994 KB Kaggle. A licença de uso segue os termos estipulados pelo MovieLens, permitindo utilização para fins acadêmicos e de pesquisa, e exige que o uso seja não comercial.

Visão geral
Este dataset contém registros produzidos por 610 usuários, que coletivamente geraram 100.836 avaliações e aplicaram 3.683 tags a 9.742 filmes, no período de 29 de março de 1996 a 24 de setembro de 2018 Kaggle+1. Trata-se de uma base compacta, ideal para experimentos, ensino e prototipagem em sistemas de recomendação.
Atributos

O conjunto é composto por quatro arquivos no formato CSV:
links.csv, movies.csv, ratings.csv e tags.csv.

ratings.csv: Contém as avaliações dos filmes.
userId: O ID do usuário anônimo.
movieId: O ID do filme.
rating: A avaliação de 5 estrelas, com incrementos de 0,5 estrelas.
timestamp: O momento da avaliação em segundos desde 1º de janeiro de 1970 (UTC).

tags.csv: Contém as tags aplicadas aos filmes.
userId: O ID do usuário anônimo.
movieId: O ID do filme.
tag: A tag gerada pelo usuário, geralmente uma palavra ou frase curta.
timestamp: O momento da tag em segundos desde 1º de janeiro de 1970 (UTC).

movies.csv: Contém informações sobre os filmes.
movieId: O ID do filme.
title: O título do filme, incluindo o ano de lançamento entre parênteses.
genres: Uma lista de gêneros separados por pipe (|).

links.csv: Contém identificadores que ligam os filmes a outras bases de dados.
movieId: O ID do filme no MovieLens.
imdbId: O ID do filme no IMDb.
tmdbId: O ID do filme no The Movie Database (TMDb).


# Canvas analítico

Nesta seção, você deverá estruturar e preencher o seu Canvas Analítico, que tem como objetivo registrar a organização das ideias e apresentar o modelo de negócio do projeto.

O Canvas deve ser preenchido integralmente, mesmo que algumas informações ainda não estejam totalmente definidas. Nessa etapa inicial, é aceitável trabalhar com hipóteses ou estimativas, desde que sejam coerentes com o problema e o contexto definidos.

**Dica:** O Canvas Analítico serve como guia visual para alinhar expectativas e direcionar o desenvolvimento. Ele poderá (e deverá) ser revisitado e atualizado ao longo do projeto.

> **Links Úteis**:
> - [Modelo do Canvas Analítico](https://github.com/ICEI-PUC-Minas-PMV-SI/PesquisaExperimentacao-Template/blob/main/help/Software-Analtics-Canvas-v1.0.pdf)

# Vídeo de apresentação da Etapa 01

Nesta etapa, o grupo deverá produzir um vídeo de 5 a 8 minutos apresentando o trabalho realizado, no qual cada integrante deve dizer seu nome e apresentar uma parte do conteúdo desenvolvido, garantindo que todos participem ativamente da gravação. A ausência de participação de qualquer membro resultará em penalização na nota final desta etapa. Recomenda-se que o grupo elabore previamente um roteiro para organizar a ordem das falas, distribuir o tempo de forma equilibrada e assegurar que todos os tópicos relevantes sejam apresentados de maneira clara e objetiva.

# Referências

Inclua todas as referências (livros, artigos, sites, etc) utilizados no desenvolvimento do trabalho utilizando o padrão ABNT.

> **Links Úteis**:
> - [Padrão ABNT PUC Minas](https://portal.pucminas.br/biblioteca/index_padrao.php?pagina=5886)
