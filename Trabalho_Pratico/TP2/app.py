import streamlit as st
import mysql.connector

# Configuração da página
st.set_page_config(
    page_title="Sistema Biblioteca",
    page_icon="📚",
    layout="centered"
)

# Função para conectar ao MySQL
def conectar_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="user_biblioteca",
            password="IDP@biblioteca1234"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}")
        return None

# Função para criar o banco de dados e tabelas
def criar_banco_e_tabelas(conn):
    cursor = conn.cursor()
    try:
        # Criar banco de dados se não existir
        cursor.execute("CREATE DATABASE IF NOT EXISTS Biblioteca")
        conn.database = "Biblioteca"
        
        # Definir as tabelas e seus DDLs
        tabelas = {
            "editora": """
                CREATE TABLE IF NOT EXISTS editora (
                    id_editora INT PRIMARY KEY AUTO_INCREMENT,
                    nome_editora VARCHAR(150) NOT NULL UNIQUE,
                    telefone_editora VARCHAR(15),
                    email_editora VARCHAR(255)
                )
            """,
            "livros": """
                CREATE TABLE IF NOT EXISTS livros (
                    id_livro INT PRIMARY KEY AUTO_INCREMENT,
                    isbn VARCHAR(13) NOT NULL,
                    titulo VARCHAR(255) NOT NULL,
                    edicao INT,
                    id_editora INT,
                    ano_publicacao INT,
                    local_publicacao VARCHAR(100),
                    num_copias INT NOT NULL,
                    num_copias_disponiveis INT NOT NULL,
                    CONSTRAINT fk_livros_id_editora FOREIGN KEY (id_editora) REFERENCES editora(id_editora)
                )
            """,
            "generos": """
                CREATE TABLE IF NOT EXISTS generos (
                    id_genero INT PRIMARY KEY AUTO_INCREMENT,
                    nome_genero VARCHAR(50) NOT NULL UNIQUE,
                    desc_genero TEXT
                )
            """,
            "livro_genero": """
                CREATE TABLE IF NOT EXISTS livro_genero (
                    id_livro INT,
                    id_genero INT,
                    PRIMARY KEY (id_livro, id_genero),
                    CONSTRAINT fk_livro_genero_id_livro FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
                    CONSTRAINT fk_livro_genero_id_genero FOREIGN KEY (id_genero) REFERENCES generos(id_genero)
                )
            """,
            "autores": """
                CREATE TABLE IF NOT EXISTS autores (
                    id_autor INT PRIMARY KEY AUTO_INCREMENT,
                    nome_autor VARCHAR(150) NOT NULL UNIQUE,
                    nacionalidade_autor VARCHAR(100),
                    data_nasc_autor DATE
                )
            """,
            "livro_autor": """
                CREATE TABLE IF NOT EXISTS livro_autor (
                    id_livro INT,
                    id_autor INT,
                    PRIMARY KEY (id_livro, id_autor),
                    CONSTRAINT fk_livro_autor_id_livro FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
                    CONSTRAINT fk_livro_autor_id_autor FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
                )
            """,
            "tradutores": """
                CREATE TABLE IF NOT EXISTS tradutores (
                    id_tradutor INT PRIMARY KEY AUTO_INCREMENT,
                    nome_tradutor VARCHAR(150) NOT NULL UNIQUE, 
                    nacionalidade_tradutor VARCHAR(100),
                    data_nasc_tradutor DATE
                )
            """,
            "livro_tradutor": """
                CREATE TABLE IF NOT EXISTS livro_tradutor (
                    id_livro INT,
                    id_tradutor INT,
                    PRIMARY KEY (id_livro, id_tradutor),
                    CONSTRAINT fk_livro_tradutor_id_livro FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
                    CONSTRAINT fk_livro_tradutor_id_tradutor FOREIGN KEY (id_tradutor) REFERENCES tradutores(id_tradutor)
                )
            """,
            "exemplares": """
                CREATE TABLE IF NOT EXISTS exemplares (
                    id_exemplar INT PRIMARY KEY AUTO_INCREMENT,
                    id_livro INT,
                    disponibilidade BOOLEAN NOT NULL,
                    local_exemplar VARCHAR(50),
                    CONSTRAINT fk_exemplares_id_livro FOREIGN KEY (id_livro) REFERENCES livros(id_livro)
                )
            """,
            "clientes": """
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
                    nome_cliente VARCHAR(150) NOT NULL,
                    cpf_cliente VARCHAR(11) UNIQUE NOT NULL,
                    email_cliente VARCHAR(255),
                    telefone_cliente VARCHAR(15),
                    data_nasc_cliente DATE,
                    endereco_cliente VARCHAR(255)
                )
            """,
            "emprestimos": """
                CREATE TABLE IF NOT EXISTS emprestimos (
                    id_emprestimo INT PRIMARY KEY AUTO_INCREMENT,
                    id_cliente INT,
                    id_exemplar INT,
                    status ENUM('ativo', 'finalizado', 'atrasado') NOT NULL,
                    data_emprestimo DATE NOT NULL,
                    data_devolucao_prevista DATE NOT NULL,
                    data_devolucao DATE,
                    quantidade_renovacoes INT DEFAULT 0,
                    CONSTRAINT fk_emprestimos_id_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                    CONSTRAINT fk_emprestimos_id_exemplar FOREIGN KEY (id_exemplar) REFERENCES exemplares(id_exemplar)
                )
            """
        }
        
        # Criar as tabelas
        for nome_tabela, ddl in tabelas.items():
            try:
                cursor.execute(ddl)
                conn.commit()
            except mysql.connector.Error as table_err:
                st.error(f"Erro ao criar a tabela {nome_tabela}: {table_err}")

        st.success("Banco de dados e tabelas configurados com sucesso!")

    except mysql.connector.Error as err:
        st.error(f"Erro ao configurar o banco de dados: {err}")
    finally:
        cursor.close()

# Função para autenticar o usuário
def autenticar_usuario(usuario, senha):
    if usuario == "admin" and senha == "admin":
        return True
    return False

# Página de Login
st.title("Login - Sistema Biblioteca")
usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
if st.button("Entrar"):
    conn = conectar_mysql()
    if conn:
        criar_banco_e_tabelas(conn)
        if autenticar_usuario(usuario, senha):
            st.success("Login bem-sucedido! Bem-vindo ao sistema.")
        else:
            st.error("Usuário ou senha incorretos.")
        conn.close()