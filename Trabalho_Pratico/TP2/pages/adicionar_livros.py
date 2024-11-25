import streamlit as st
import mysql.connector

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

#Verificadores de Validade
#Verificar Faltantes
def verificar_validade_faltantes(titulo, isbn, edicao, editora, autores, ano_publicacao, local_publicacao, num_copias):
    campos_vazios = []
    # Identificar informações faltantes
    if not titulo:
        campos_vazios.append("Titulo")
    if not isbn:
        campos_vazios.append("ISBN")
    if not edicao:
        campos_vazios.append("Edição")
    if not editora:
        campos_vazios.append("Editora")
    if not autores:
        campos_vazios.append("Autores")
    if not ano_publicacao:
        campos_vazios.append("Ano de Publicação")
    if not local_publicacao:
        campos_vazios.append("Local de Publicação")
    if not num_copias:
        campos_vazios.append("Número de Cópias")

    if campos_vazios != []:
        st.error(f"Por favor, preencha os seguintes campos obrigatórios: {', '.join(campos_vazios)}")
        return False
    else:
        return True

#Verificar ISBN
def verificar_validade_isbn(isbn):
    if not isbn:
        return False

    # Checar tamanho do ISBN
    if len(isbn) not in (10, 13):
        st.error("O ISBN deve ser um valor de 10 ou 13 dígitos")
        return False

    # Checar unicidade do ISBN
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM livros WHERE isbn = %s", (isbn,))
        count = cursor.fetchone()[0]
        if count > 0:  # Se ISBN já existir
            st.error("Um livro com esse ISBN já está registrado")
            return False
        return True
    finally:
        cursor.close()
        conn.close()

def adicionar_livro(titulo, isbn, edicao, editora, autores, tradutores, generos, ano_publicacao, local_publicacao, num_copias):
    if not verificar_validade_isbn(isbn):
        return
        
    try:
        #Conectar ao Banco
        conn = get_connection()
        cursor = conn.cursor()

        #Checar editora
        cursor.execute("INSERT INTO editora (nome_editora) VALUES (%s) ON DUPLICATE KEY UPDATE id_editora = LAST_INSERT_ID(id_editora)", (editora,))
        conn.commit()
        id_editora = cursor.lastrowid

        #Inserir livro
        cursor.execute("""
                    INSERT INTO livros 
                    (isbn, titulo, edicao, id_editora, ano_publicacao, local_publicacao, num_copias, num_copias_disponiveis)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (isbn, titulo, edicao, id_editora, ano_publicacao, local_publicacao, num_copias, num_copias))
        conn.commit()

        #Pegar ID Livro
        cursor.execute("SELECT id_livro FROM livros WHERE isbn = %s", (isbn,))
        id_livro = cursor.fetchone()[0]

        #Adicionar autores
        for autor in autores:
            if autor:
                cursor.execute("INSERT INTO autores (nome_autor) VALUES (%s) ON DUPLICATE KEY UPDATE id_autor = LAST_INSERT_ID(id_autor)", (autor,))
                conn.commit()
                id_autor = cursor.lastrowid

                cursor.execute("INSERT INTO livro_autor (id_livro, id_autor) VALUES (%s, %s)", (id_livro, id_autor))
                conn.commit()

        #Adicionar tradutores
        for tradutor in tradutores:
            if tradutor:
                cursor.execute("INSERT INTO tradutores (nome_tradutor) VALUES (%s) ON DUPLICATE KEY UPDATE id_tradutor = LAST_INSERT_ID(id_tradutor)", (tradutor,))
                conn.commit()
                id_tradutor = cursor.lastrowid

                cursor.execute("INSERT INTO livro_tradutor (id_livro, id_tradutor) VALUES (%s, %s)", (id_livro, id_tradutor))
                conn.commit()

        #Adicionar gêneros
        for genero in generos:
            if genero:
                cursor.execute("INSERT INTO generos (nome_genero) VALUES (%s) ON DUPLICATE KEY UPDATE id_genero = LAST_INSERT_ID(id_genero)", (genero,))
                conn.commit()
                id_genero = cursor.lastrowid

                cursor.execute("INSERT INTO livro_genero (id_livro, id_genero) VALUES (%s, %s)", (id_livro, id_genero))
                conn.commit()

        #Criar exemplares
        for i in range(num_copias):
            cursor.execute("INSERT INTO exemplares (id_livro, disponibilidade) VALUES (%s, %s)", (id_livro, True))
            conn.commit()

        st.success("Livro adicionado com sucesso!")
        
    except mysql.connector.Error as err:
        st.error(f"Erro ao adicionar livro: {err}")
        
    finally:
        #Desligar conexão
        cursor.close()
        conn.close()

def pag_adicionar_livro():
    #Pagina de Adicionar Livro
    st.title("Adicionar Livro")

    #Parte 1 - Info Geral
    titulo = st.text_input("Título do Livro")
    isbn = st.text_input("ISBN")
    verificar_validade_isbn(isbn)
    edicao = st.number_input("Edição", min_value=1, step=1)
    editora = st.text_input("Editora")

    #Parte 2 - Autores
    st.header("Autores")
    num_autores = st.number_input("Número de Autores", min_value=1, step=1)
    # Criação dos campos para autores
    autores = []
    if num_autores > 0:
        for i in range(num_autores):
            autor = st.text_input(f"Autor {i + 1}")
            autores.append(autor)

    #Parte 3 - Tradutores
    st.header("Tradutores")
    num_tradutores = st.number_input("Número de Tradutores", min_value=0, step=1)
    # Criação dos campos para tradutores
    tradutores = []
    if num_tradutores > 0:
        for i in range(num_tradutores):
            tradutor = st.text_input(f"Tradutor {i + 1}")
            tradutores.append(tradutor)

    #Parte 4 - Gêneros
    st.header("Gêneros")
    num_generos = st.number_input("Número de Gêneros", min_value=0, step=1)
    # Criação dos campos para gêneros
    generos = []
    if num_generos > 0:
        for i in range(num_generos):
            genero = st.text_input(f"Gênero {i + 1}")
            generos.append(genero)

    #Parte 5 - Publicações e Cópias
    st.header("Publicação e Cópias")
    ano_publicacao = st.number_input("Ano de Publicação", min_value=1000, max_value=9999, step=1)
    local_publicacao = st.text_input("Local de Publicação")
    num_copias = st.number_input("Número de Cópias", min_value=1, step=1)

    #Botão Enviar
    if st.button("Adicionar Livro"):
        if verificar_validade_faltantes(titulo, isbn, edicao, editora, autores, ano_publicacao, local_publicacao, num_copias):
            adicionar_livro(titulo, isbn, edicao, editora, autores, tradutores, generos, ano_publicacao, local_publicacao, num_copias)

pag_adicionar_livro()