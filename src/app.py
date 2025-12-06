import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from scipy import sparse
from surprise.dump import load
from sklearn.metrics.pairwise import linear_kernel 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Recomendador Híbrido", layout="wide")

# --- FUNÇÃO DE CARREGAMENTO ULTRA ROBUSTA (COM CORREÇÃO SVD) ---
@st.cache_resource
def load_model_artifacts():
    """
    Carrega artefatos verificando a existência de cada arquivo individualmente.
    Inclui correção para leitura do objeto SVD.
    """
    # 1. Determina a pasta onde ESTE arquivo (app.py) está
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Determina a pasta de artefatos
    artifact_folder = os.path.join(base_dir, 'model_artifacts')

    # Debug na tela
    print(f"📂 Pasta base definida como: {artifact_folder}")

    # 3. Define os caminhos EXATOS
    files = {
        'svd': os.path.join(artifact_folder, 'algo_svd_otimizado.pickle'),
        'movies': os.path.join(artifact_folder, 'movies_for_app.csv'),
        'cosine': os.path.join(artifact_folder, 'cosine_sim_matrix.npy'),
        'indices': os.path.join(artifact_folder, 'indices.pickle'),
        'vectorizer': os.path.join(artifact_folder, 'tfidf_vectorizer.pickle'),
        'tfidf_matrix': os.path.join(artifact_folder, 'tfidf_matrix.npz'),
    }

    # 4. VERIFICAÇÃO PRÉVIA
    missing_files = []
    for name, path in files.items():
        if not os.path.exists(path):
            missing_files.append(f"{name}: {path}")
    
    if missing_files:
        st.error("🚨 ERRO: Alguns arquivos não foram encontrados!")
        for f in missing_files:
            st.code(f)
        return None

    # 5. CARREGAMENTO SEGURO
    try:
        # --- CORREÇÃO DO SVD AQUI ---
        # O surprise.load retorna uma tupla (predictions, algo)
        dump_obj = load(files['svd'])
        
        # Verifica se o modelo está no slot 'algo' (índice 1) ou 'predictions' (índice 0)
        if dump_obj[1] is not None:
            algo_svd = dump_obj[1] # Salvamento correto: dump(file, algo=modelo)
        else:
            algo_svd = dump_obj[0] # Salvamento posicional: dump(file, modelo)
            
        # Carregar Pandas/Numpy
        movies_df = pd.read_csv(files['movies'])
        cosine_sim = np.load(files['cosine'])
        indices = pd.read_pickle(files['indices'])
        
        # Carregar Cold Start
        with open(files['vectorizer'], 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
            
        tfidf_matrix = sparse.load_npz(files['tfidf_matrix'])
        
        return algo_svd, movies_df, cosine_sim, indices, tfidf_vectorizer, tfidf_matrix

    except Exception as e:
        st.error(f"❌ Erro ao ler os arquivos: {e}")
        return None

# --- LÓGICA DE RECOMENDAÇÃO ---

def get_available_tags(movies_df):
    unique_genres = set()
    for genres in movies_df['genres'].dropna().astype(str).str.split('|'):
        unique_genres.update(genres)
    return sorted(list(unique_genres))

def recommend_for_new_user(selected_tags, movies_df, tfidf_vectorizer, tfidf_matrix, n=10):
    query_string = " ".join(selected_tags)
    user_profile_vector = tfidf_vectorizer.transform([query_string])
    cosine_sim_user = linear_kernel(user_profile_vector, tfidf_matrix)
    sim_scores = list(enumerate(cosine_sim_user[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[:n]]
    return movies_df.iloc[top_indices][['movieId', 'title_clean', 'genres']]

def get_hybrid_recommendations(user_id, n, content_weight, algo_svd, movies_df, cosine_sim, indices, movie_ids_rated, favorite_movie_ids):
    sim_scores_favorite_avg = None
    if favorite_movie_ids:
        favorite_titles = movies_df[movies_df['movieId'].isin(favorite_movie_ids)]['title_clean']
        favorite_indices = [indices[t] for t in favorite_titles if t in indices]
        if favorite_indices:
            sim_vectors = cosine_sim[favorite_indices]
            sim_scores_favorite_avg = np.mean(sim_vectors, axis=0)
    
    all_movie_ids = movies_df['movieId'].unique()
    movies_to_predict = [mid for mid in all_movie_ids if mid not in movie_ids_rated]
    
    svd_predictions = []
    
    # Otimização: Se houver muitos filmes, limita a predição aos primeiros 500 para não travar
    # (Remova o [:500] se quiser precisão total, mas pode ficar lento em PC fraco)
    candidatos = movies_to_predict if len(movies_to_predict) < 1000 else movies_to_predict[:1000]

    for movie_id in candidatos:
        pred = algo_svd.predict(uid=user_id, iid=movie_id)
        svd_predictions.append((movie_id, pred.est))
    svd_predictions.sort(key=lambda x: x[1], reverse=True)
    
    hybrid_scores = []
    for movie_id, svd_score in svd_predictions[:200]: 
        hybrid_score = svd_score
        if sim_scores_favorite_avg is not None:
            try:
                title = movies_df.loc[movies_df['movieId'] == movie_id]['title_clean'].iloc[0]
                idx = indices[title]
                content_sim = sim_scores_favorite_avg[idx]
                hybrid_score = svd_score + (content_sim * content_weight)
            except (KeyError, IndexError):
                pass
        hybrid_scores.append((movie_id, hybrid_score))
        
    hybrid_scores.sort(key=lambda x: x[1], reverse=True)
    top_ids = [mid for mid, score in hybrid_scores[:n]]
    return movies_df[movies_df['movieId'].isin(top_ids)][['movieId', 'title_clean', 'genres']]

# --- INTERFACE PRINCIPAL ---

artifacts = load_model_artifacts()

if artifacts is not None:
    (algo_svd, movies_df, cosine_sim, indices, tfidf_vectorizer, tfidf_matrix) = artifacts

    st.title("🎬 Sistema de Recomendação Inteligente")
    st.markdown("---")

    st.sidebar.header("Perfil do Usuário")
    user_type = st.sidebar.radio("Quem é você?", ["Usuário Existente (Login)", "Novo Usuário (Visitante)"])
    recommendations = pd.DataFrame()
    msg_sucesso = ""

    if user_type == "Usuário Existente (Login)":
        st.sidebar.info("Modo: **Híbrido (Histórico + Conteúdo)**")
        user_id = st.sidebar.number_input("Seu ID:", min_value=1, max_value=610, value=50)
        MOCKED_RATED = [1, 2, 3, 4, 5, 50, 60]
        MOCKED_FAVS = [1, 50] 
        content_weight = st.sidebar.slider("Peso do Conteúdo:", 0.0, 1.0, 0.5)
        n_recs = st.sidebar.slider("Qtd. Recomendações:", 5, 20, 10)
        
        if st.sidebar.button("Gerar Recomendações"):
            with st.spinner(f"Analisando perfil do usuário {user_id}..."):
                recommendations = get_hybrid_recommendations(
                    user_id, n_recs, content_weight, algo_svd, movies_df, 
                    cosine_sim, indices, MOCKED_RATED, MOCKED_FAVS
                )
                msg_sucesso = f"Top {n_recs} filmes para você:"

    else:
        st.sidebar.info("Modo: **Cold Start (Baseado em Tags)**")
        st.sidebar.markdown("Selecione o que você gosta:")
        tags_disponiveis = get_available_tags(movies_df)
        selected_tags = st.sidebar.multiselect("Gêneros Favoritos:", tags_disponiveis, default=["Comedy"])
        n_recs = st.sidebar.slider("Qtd. Recomendações:", 5, 20, 10)
        
        if st.sidebar.button("Descobrir Filmes"):
            if not selected_tags:
                st.warning("Selecione pelo menos um gênero!")
            else:
                with st.spinner("Buscando filmes..."):
                    recommendations = recommend_for_new_user(
                        selected_tags, movies_df, tfidf_vectorizer, tfidf_matrix, n=n_recs
                    )
                    msg_sucesso = f"Filmes encontrados para: **{', '.join(selected_tags)}**"

    if not recommendations.empty:
        st.success(msg_sucesso)
        colms = st.columns((1, 4, 2))
        fields = ["ID", "Título", "Gênero"]
        for col, field_name in zip(colms, fields):
            col.write(f"**{field_name}**")
        for i, row in recommendations.iterrows():
            col1, col2, col3 = st.columns((1, 4, 2))
            col1.write(str(row['movieId']))
            col2.write(row['title_clean'])
            col3.write(row['genres'])

else:
    st.warning("O sistema parou porque não conseguiu acessar os dados.")