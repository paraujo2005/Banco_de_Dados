import streamlit as st
import mysql.connector
import pandas as pd

# Função de conexão com o banco de dados
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="user_biblioteca",
        password="IDP@biblioteca1234",
        database="Biblioteca"
    )

# Configuração da página
st.set_page_config(
    page_title="Sistema Biblioteca",
    page_icon="📚",
    layout="wide"
)

def apresentar_emprestimos():
    st.title("Gerenciar Emprestimos")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            e.id_emprestimo, 
            c.nome_cliente, 
            l.titulo, 
            e.status, 
            e.data_emprestimo, 
            e.data_devolucao_prevista, 
            e.data_devolucao, 
            e.quantidade_renovacoes
        FROM 
            emprestimos e
        JOIN 
            clientes c ON e.id_cliente = c.id_cliente
        JOIN 
            exemplares ex ON e.id_exemplar = ex.id_exemplar
        JOIN 
            livros l ON ex.id_livro = l.id_livro
    """)
    emprestimos = cursor.fetchall()

    df = pd.DataFrame(emprestimos, columns=[
        'id_emprestimo', 
        'Nome do Cliente', 
        'Título do Livro', 
        'Status', 
        'Data de Emprestimo', 
        'Data Prevista de Devolução', 
        'Data de Devolução', 
        'Renovações'
    ])

    df['Data de Devolução'] = df['Data de Devolução'].fillna('Null')
    df['Renovações'] = df['Renovações'].fillna('Null')

    df_sem_id = df.drop(columns=['id_emprestimo'])

    st.dataframe(df_sem_id, use_container_width=True)
    
    cursor.close()
    conn.close()

apresentar_emprestimos()