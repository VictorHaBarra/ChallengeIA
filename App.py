import streamlit as st
import pandas as pd
import scipy.sparse as sparse
from implicit.als import AlternatingLeastSquares

# Configurações do ALS
model = AlternatingLeastSquares(factors=10, regularization=0.1, iterations=20)

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

# Cria um mapeamento de IDs de usuários para índices contínuos
user_id_mapping = {user_id: idx for idx, user_id in enumerate(usuarios['ID do Usuário'])}
num_users = len(user_id_mapping)

# Prepara a matriz de interação usuário-produto
interactions = []
for index, row in usuarios.iterrows():
    user_id = row['ID do Usuário']
    for product_id in row['Histórico de Compras']:
        # Adiciona as interações na lista de interações
        interactions.append((user_id_mapping[user_id], product_id, 1))

interaction_df = pd.DataFrame(interactions, columns=['user_id', 'product_id', 'purchase_count'])

# Cria a matriz esparsa de usuário-produto
user_item_matrix = sparse.coo_matrix(
    (interaction_df['purchase_count'], (interaction_df['user_id'], interaction_df['product_id']))
).tocsr()

# Verifica a forma da matriz esparsa
print("Shape of user_item_matrix:", user_item_matrix.shape)  # Debugging line

# Treina o modelo ALS
model.fit(user_item_matrix)

# Função para obter recomendações usando implicit
def get_recommendations(user_id, product_data, n=3):
    if user_id not in user_id_mapping:
        st.warning("Usuário não encontrado.")  # Exibe uma mensagem se o usuário não existir
        return pd.DataFrame()  # Retorna um DataFrame vazio se o usuário não existir
    
    user_index = user_id_mapping[user_id]  # Mapeia o ID do usuário para o índice contínuo

    # Garante que o índice do usuário está dentro do intervalo da matriz
    if user_index >= user_item_matrix.shape[0]:
        st.warning("Índice do usuário fora do intervalo.")  # Exibe uma mensagem se o índice do usuário estiver fora do intervalo
        return pd.DataFrame()

    recommendations = model.recommend(user_index, user_item_matrix, N=n)  # Use user_item_matrix directly
    
    # Ajusta o índice de retorno para o ID do Produto
    product_ids = [rec[0] + 1 for rec in recommendations]  # +1 para coincidir com os IDs de produtos em 'produtos'
    return product_data[product_data['ID do Produto'].isin(product_ids)]

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
    recomendacoes = get_recommendations(user_id, produtos)
    
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
