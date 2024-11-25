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

def verificar_validade_faltantes(nome, cpf, email, telefone, nascimento, endereco):
    campos_vazios = []
    # Identificar informações faltantes
    if not nome:
        campos_vazios.append("Nome do Cliente")
    if not cpf:
        campos_vazios.append("CPF")
    if not email:
        campos_vazios.append("Email")
    if not telefone:
        campos_vazios.append("Telefone")
    if not nascimento:
        campos_vazios.append("Data de Nascimento")
    if not endereco:
        campos_vazios.append("Endereço")

    if campos_vazios != []:
        st.error(f"Por favor, preencha os seguintes campos obrigatórios: {', '.join(campos_vazios)}")
        return False
    else:
        return True

def adicionar_cliente(nome, cpf, email, telefone, nascimento, endereco):
    nascimento = f"{nascimento.strftime('%Y-%m-%d')}"
    
    try:
        #Conectar ao Banco
        conn = get_connection()
        cursor = conn.cursor()

        #Inserir cliente
        cursor.execute("""
                    INSERT INTO clientes 
                    (nome_cliente, cpf_cliente, email_cliente, telefone_cliente, data_nasc_cliente, endereco_cliente)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nome, cpf, email, telefone, nascimento, endereco))
        conn.commit()

        st.success("Cliente adicionado com sucesso!")
        
    except mysql.connector.Error as err:
        st.error(f"Erro ao adicionar cliente: {err}")
        
    finally:
        #Desligar conexão
        cursor.close()
        conn.close()


def pag_adicionar_cliente():
    #Pagina de Adicionar Cliente
    st.title("Adicionar Cliente")
    nome = st.text_input("Nome do Cliente")
    cpf = st.text_input("CPF")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")
    nascimento = st.date_input("Data de Nascimento", value=None)
    endereco = st.text_input("Endereço")

    if st.button("Cadastrar Cliente"):
        if verificar_validade_faltantes(nome, cpf, email, telefone, nascimento, endereco):
            adicionar_cliente(nome, cpf, email, telefone, nascimento, endereco)

pag_adicionar_cliente()