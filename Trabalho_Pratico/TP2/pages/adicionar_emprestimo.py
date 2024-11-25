import streamlit as st
import mysql.connector
import datetime

# Configuração da página
st.set_page_config(
    page_title="Sistema Biblioteca",
    page_icon="📚",
    layout="centered"
)

# Conexão com o banco de dados
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="user_biblioteca",
        password="IDP@biblioteca1234",
        database="Biblioteca"
    )

def validar_cliente(cliente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_emprestimo FROM emprestimos WHERE id_cliente = %s", (cliente,))
    validar_cliente = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(validar_cliente) < 2:
        return True
    else:
        return False

def validar_emprestimo(id_livro):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_exemplar FROM exemplares WHERE id_livro = %s AND disponibilidade = 1", (id_livro,))
    validar_emprestimo = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(validar_emprestimo) > 0:
        return True
    else:
        return False

def pag_adicionar_eprestimo():
    #Pagina de Adicionar Emprestimo
    st.title("Adicionar Emprestimo")

    #Definir Livro e Cliente
    busca_por_livro = st.radio("Como deseja inserir o livro?", ("Título", "ISBN"))
    conn = get_connection()
    cursor = conn.cursor()

    #Livro
    #Buscar por Título
    if busca_por_livro == "Título":
        cursor.execute("SELECT titulo FROM livros")
        titulos = cursor.fetchall()
        titulos = [titulo[0] for titulo in titulos]
        livro_selecionado = st.selectbox("Selecione o livro por Título", titulos)
        cursor.execute("SELECT id_livro FROM livros WHERE titulo = %s", (livro_selecionado,))
        livro_id = cursor.fetchone()[0]
    #Buscar por ISBN
    elif busca_por_livro == "ISBN":
        cursor.execute("SELECT isbn FROM livros")
        isbns = cursor.fetchall()
        isbns = [isbn[0] for isbn in isbns]
        livro_selecionado = st.selectbox("Selecione o livro por ISBN", isbns)
        cursor.execute("SELECT id_livro FROM livros WHERE isbn = %s", (livro_selecionado,))
        livro_id = cursor.fetchone()[0]

    #Cliente
    cpf_input = st.text_input("Digite o CPF do cliente (Insira apenas Digitos): ")
    if cpf_input:
        cursor.execute("SELECT id_cliente, nome_cliente FROM clientes WHERE cpf_cliente = %s", (cpf_input,))
        cliente = cursor.fetchone()
        if cliente:
            st.success(f"Cliente encontrado: {cliente[1]}")
            cliente = cliente[0]
        else:
            st.error("Cliente não encontrado.")

    #Data de Emprestimo
    data = st.date_input("Insira a data de hoje:", value = None)

    #Calculo Data de Devolução (2 semanas)
    if data:
        data_devolucao = data + datetime.timedelta(weeks=2)
        st.info(f"A data de devolução será: {data_devolucao.strftime('%d/%m/%Y')}")

    #Adicionar Emprestimo
    if st.button("Adicionar Emprestimo"):
        cursor.close()
        conn.close()
        #Validar 
        #Cliente (Apenas 2 emprestimos por Cliente)
        if not validar_cliente(cliente):
            st.error("O cliente já chegou ao limite de emprestimos por vez")
        #Emprestimo Disponivel
        elif not validar_emprestimo(livro_id):
            st.error("Não existem exemplares disponiveis no momento")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id_exemplar FROM exemplares WHERE id_livro = %s AND disponibilidade = 1", (livro_id,))
                id_exemplar = cursor.fetchall()
                id_exemplar = id_exemplar[0][0]
                cursor.execute("UPDATE livros SET num_copias_disponiveis = num_copias_disponiveis - 1 WHERE id_livro = %s", (livro_id,))
                cursor.execute("""INSERT INTO emprestimos (id_cliente, id_exemplar, status, data_emprestimo, data_devolucao_prevista) 
                               VALUES (%s, %s, %s, %s, %s)""", (cliente, id_exemplar, 'ativo', data, data_devolucao))
                conn.commit()
                st.success("Emprestimo Criado com Sucesso")
            except Exception as e:
                st.error(f"Erro ao Inserir Emprestimo: {e}")
            finally:
                cursor.close()
                conn.close()

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM livros")
livros_existentes = cursor.fetchall()
cursor.close()
conn.close()

if len(livros_existentes) < 1:
    st.warning("Nenhum Livro Adicionado")
else:
    pag_adicionar_eprestimo()