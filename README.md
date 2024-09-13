# 🛍️ Sistema de Recomendação de Produtos
Descrição do Projeto;

Este projeto é um protótipo de um sistema de recomendação de produtos, desenvolvido com o objetivo de fornecer recomendações personalizadas com base no histórico de compras e nas preferências dos usuários. Utilizamos Machine Learning e técnicas de IA generativa para melhorar a experiência de recomendação.

# Funcionalidades
- Recomendação de produtos personalizados para usuários com base em seu histórico de compras.
- Visualização das informações detalhadas do usuário, como idade, localização e preferências de compra.
- Exibição de produtos recomendados que o usuário ainda não comprou.
- Integração com uma base de dados de produtos e usuários

# Tecnologias Utilizadas
*Linguagem de Programação*: Python

*Bibliotecas*:
- Pandas para manipulação de dados.
- Streamlit para a interface do usuário.
- Surprise para o algoritmo de recomendação.
- IA Utilizada: Algoritmo SVD (Singular Value Decomposition) para recomendações.

# Estrutura do Projeto
```
├── App.py                # Código principal do sistema de recomendação
├── requirements.txt      # Dependências do projeto
└── README.md             # Descrição do projeto
```
## Como Executar
### Clonar o repositório:
```
git clone https://github.com/seu-repositorio/sistema-recomendacao.git
cd sistema-recomendacao
```
### Instalar as dependências: 
- Utilize um ambiente virtual e instale as bibliotecas necessárias listadas no commands.txt:
```
pip install -r commands.txt
```
### Executar a aplicação: 
- Execute o comando abaixo para iniciar o servidor local do Streamlit:
```
streamlit run App.py
```
### Acessar a aplicação: 
- Abra o navegador e acesse http://localhost:8501 para visualizar o sistema de recomendação.

## Exemplo de Uso
- O usuário pode selecionar um perfil de usuário existente e, em seguida, clicar no botão "🔍 Gerar Recomendações" para visualizar os produtos recomendados.
- O sistema exibe uma lista de produtos que correspondem ao perfil de preferência do usuário e que ele ainda não adquiriu.
## Melhorias Futuras
- Expansão da Base de Dados: Adicionar mais usuários e produtos para aumentar a precisão do sistema de recomendação.
- Melhorias no Algoritmo: Implementar outras técnicas de IA para aumentar a personalização das recomendações.
- Integração com API: Conectar o sistema a uma API externa para carregar dados em tempo real.
### Integrantes do Projeto
*Matheus Chagas de Moraes Sampaio - RM 550489*

*Paulo Henrique Moreira Anguera - RM 99704*

*Victor Hugo Astorino Barra Mansa - RM 550573*
