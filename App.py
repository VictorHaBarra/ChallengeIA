import streamlit as st
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

# Função para obter recomendações
def get_recommendations(user_id, user_data, product_data, n=3):
    # Obtenha o histórico de compras do usuário
    historico = user_data.loc[user_data['ID do Usuário'] == user_id, 'Histórico de Compras'].values[0]
    
    # Filtrar os produtos que o usuário ainda não comprou
    produtos_nao_comprados = product_data[~product_data['ID do Produto'].isin(historico)]
    
    # Ajustar o número de recomendações se for maior do que os produtos restantes
    n_recomendacoes = min(n, len(produtos_nao_comprados))
    
    # Gerar as recomendações
    recomendacoes = produtos_nao_comprados.sample(n_recomendacoes)
    
    return recomendacoes

# Dados de produtos
produtos = pd.DataFrame({
    'ID do Produto': [1, 2, 3, 4, 5],
    'Nome do Produto': ['Gel de Limpeza Facial', 'Creme Hidratante', 'Óleo para Barba', 'Perfume Masculino', 'Shampoo Anticaspa'],
    'Categoria': ['Cuidados com a Pele', 'Cuidados com a Pele', 'Barba', 'Fragrâncias', 'Cabelo'],
    'Preço': [25.99, 19.99, 15.50, 39.99, 12.99],
    'Descrição': ['Limpa profundamente a pele', 'Hidratação intensa', 'Suaviza e nutre a barba', 'Aroma elegante e duradouro', 'Combate a caspa e a oleosidade']
})

# Dados de usuários
usuarios = pd.DataFrame({
    'ID do Usuário': [101, 102, 103, 104, 105],
    'Idade': [30, 25, 35, 28, 40],
    'Localização': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Porto Alegre', 'Salvador'],
    'Histórico de Compras': [[2, 4], [1, 3, 5], [1, 2, 4], [3, 5], [1, 4]],
    'Preferências': [['Cuidados com a Pele'], ['Barba', 'Cabelo'], ['Fragrâncias'], ['Cuidados com a Pele', 'Cabelo'], ['Barba']]
})

# Estilização com CSS
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .product-card {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
    }
    .product-card h4 {
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título estilizado
st.title("🛍️ Sistema de Recomendação de Produtos")

# Selecionar Usuário
st.subheader("Selecione um Usuário")
user_id = st.selectbox("Usuários disponíveis:", usuarios['ID do Usuário'])

# Mostrar informações do usuário
st.subheader("Informações do Usuário")
user_info = usuarios[usuarios['ID do Usuário'] == user_id].iloc[0]
st.markdown(f"**Idade**: {user_info['Idade']}")
st.markdown(f"**Localização**: {user_info['Localização']}")
st.markdown(f"**Preferências**: {', '.join(user_info['Preferências'])}")

# Botão para gerar recomendações
if st.button('🔍 Gerar Recomendações'):
    recomendacoes = get_recommendations(user_id, usuarios, produtos)
    
    st.subheader("🛒 Recomendações de Produtos")
    
    if recomendacoes.empty:
        st.warning("Nenhuma recomendação disponível. O usuário já comprou todos os produtos.")
    else:
        for idx, row in recomendacoes.iterrows():
            # Cartão de produto estilizado
            st.markdown(f"""
            <div class='product-card'>
                <h4>**{row['Nome do Produto']}**</h4>
                <p>Categoria: {row['Categoria']}</p>
                <p>Preço: R$ {row['Preço']}</p>
                <p>Descrição: {row['Descrição']}</p>
            </div>
            """, unsafe_allow_html=True)
