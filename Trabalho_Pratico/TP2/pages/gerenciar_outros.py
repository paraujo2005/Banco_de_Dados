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

def get_info(tabela):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {tabela}"
    cursor.execute(query)
    autores = cursor.fetchall()
    cursor.close()
    conn.close()
    return autores

def apresenta_autor():
    st.title("Gerenciar Autores")
    autores = get_info('autores')
    
    if autores:
        # Criando DataFrame com nomes de colunas explicítos
        df = pd.DataFrame(autores, columns=['id_autor', 'nome_autor', 'nacionalidade_autor', 'data_nasc_autor'])

        # Tratando valores nulos
        df['nacionalidade_autor'] = df['nacionalidade_autor'].fillna('Null')
        df['data_nasc_autor'] = df['data_nasc_autor'].fillna('Null')

        # Renomeando as colunas para exibição
        df = df.rename(columns={
            'nome_autor': 'Nome',
            'nacionalidade_autor': 'Nacionalidade',
            'data_nasc_autor': 'Data de Nascimento'
        })

        # Removendo coluna 'id_autor', pois não é necessária para exibição
        df_sem_id = df.drop(columns=['id_autor'])

        # Filtros para a tabela
        with st.sidebar:
            st.header("Filtros de Pesquisa")
            filtro_nome = st.text_input("Nome")
            filtro_nacionalide = st.text_input("Nacionalidade")
            filtro_data = st.date_input("Data de Nascimento", value=None)

        # Aplicando os filtros
        if filtro_nome:
            df_sem_id = df_sem_id[df_sem_id['Nome'].str.contains(filtro_nome, case=False, na=False)]
        if filtro_nacionalide:
            df_sem_id = df_sem_id[df_sem_id['Nacionalidade'].str.contains(filtro_nacionalide, case=False, na=False)]
        if filtro_data:
            # Convertendo a coluna de datas para o mesmo formato do filtro
            df_sem_id['Data de Nascimento'] = pd.to_datetime(df_sem_id['Data de Nascimento'], errors='coerce')
            filtro_data = pd.to_datetime(filtro_data)

            # Filtrando diretamente pela data
            df_sem_id = df_sem_id[df_sem_id['Data de Nascimento'] == filtro_data]

        # Renderizando a tabela
        if not df_sem_id.empty:
            st.dataframe(df_sem_id, use_container_width=True)
        else:
            st.warning("Nenhum autor encontrado com os critérios fornecidos.")
    else:
        st.warning("Não foram encontrados autores no banco de dados.")

def apresenta_tradutor():
    st.title("Gerenciar Tradutores")
    tradutores = get_info('tradutores')
    
    if tradutores:
        # Criando DataFrame com nomes de colunas explicítos
        df = pd.DataFrame(tradutores, columns=['id_tradutor', 'nome_tradutor', 'nacionalidade_tradutor', 'data_nasc_tradutor'])

        # Tratando valores nulos
        df['nacionalidade_tradutor'] = df['nacionalidade_tradutor'].fillna('Null')
        df['data_nasc_tradutor'] = df['data_nasc_tradutor'].fillna('Null')

        # Renomeando as colunas para exibição
        df = df.rename(columns={
            'nome_tradutor': 'Nome',
            'nacionalidade_tradutor': 'Nacionalidade',
            'data_nasc_tradutor': 'Data de Nascimento'
        })

        # Removendo coluna 'id_tradutor', pois não é necessária para exibição
        df_sem_id = df.drop(columns=['id_tradutor'])

        # Filtros para a tabela
        with st.sidebar:
            st.header("Filtros de Pesquisa")
            filtro_nome = st.text_input("Nome")
            filtro_nacionalide = st.text_input("Nacionalidade")
            filtro_data = st.date_input("Data de Nascimento", value=None)

        # Aplicando os filtros
        if filtro_nome:
            df_sem_id = df_sem_id[df_sem_id['Nome'].str.contains(filtro_nome, case=False, na=False)]
        if filtro_nacionalide:
            df_sem_id = df_sem_id[df_sem_id['Nacionalidade'].str.contains(filtro_nacionalide, case=False, na=False)]
        if filtro_data:
            # Convertendo a coluna de datas para o mesmo formato do filtro
            df_sem_id['Data de Nascimento'] = pd.to_datetime(df_sem_id['Data de Nascimento'], errors='coerce')
            filtro_data = pd.to_datetime(filtro_data)

            # Filtrando diretamente pela data
            df_sem_id = df_sem_id[df_sem_id['Data de Nascimento'] == filtro_data]

        # Renderizando a tabela
        if not df_sem_id.empty:
            st.dataframe(df_sem_id, use_container_width=True)
        else:
            st.warning("Nenhum tradutor encontrado com os critérios fornecidos.")
    else:
        st.warning("Não foram encontrados tradutores no banco de dados.")

def apresenta_genero():
    st.title("Gerenciar Gêneros")
    generos = get_info('generos')

    if generos:
        # Criando DataFrame com nomes de colunas explicítos
        df = pd.DataFrame(generos, columns=['id_genero', 'nome_genero', 'desc_genero'])

        # Tratando valores nulos
        df['desc_genero'] = df['desc_genero'].fillna('Null')

        # Renomeando as colunas para exibição
        df = df.rename(columns={
            'nome_genero': 'Gênero',
            'desc_genero': 'Descrição'
        })

        # Removendo coluna 'id_genero', pois não é necessária para exibição
        df_sem_id = df.drop(columns=['id_genero'])

        # Filtros para a tabela
        with st.sidebar:
            st.header("Filtros de Pesquisa")
            filtro_nome = st.text_input("Gênero")

        # Aplicando os filtros
        if filtro_nome:
            df_sem_id = df_sem_id[df_sem_id['Gênero'].str.contains(filtro_nome, case=False, na=False)]

        # Renderizando a tabela
        if not df_sem_id.empty:
            st.dataframe(df_sem_id, use_container_width=True)
        else:
            st.warning("Nenhum gênero encontrado com os critérios fornecidos.")
    else:
        st.warning("Não foram encontrados gêneros no banco de dados.")

def apresenta_editora():
    st.title("Gerenciar Editoras")
    editoras = get_info('editora')

    if editoras:
        # Criando DataFrame com nomes de colunas explicítos
        df = pd.DataFrame(editoras, columns=['id_editora', 'nome_editora', 'telefone_editora', 'email_editora'])

        # Tratando valores nulos
        df['telefone_editora'] = df['telefone_editora'].fillna('Null')
        df['email_editora'] = df['email_editora'].fillna('Null')

        # Renomeando as colunas para exibição
        df = df.rename(columns={
            'nome_editora': 'Editora',
            'telefone_editora': 'Telefone',
            'email_editora': 'Email'
        })

        # Removendo coluna 'id_editora', pois não é necessária para exibição
        df_sem_id = df.drop(columns=['id_editora'])

        # Filtros para a tabela
        with st.sidebar:
            st.header("Filtros de Pesquisa")
            filtro_nome = st.text_input("Editora")
            filtro_telefone = st.text_input("Telefone")
            filtro_email = st.text_input("Email")

        # Aplicando os filtros
        if filtro_nome:
            df_sem_id = df_sem_id[df_sem_id['Editora'].str.contains(filtro_nome, case=False, na=False)]
        if filtro_telefone:
            df_sem_id = df_sem_id[df_sem_id['Telefone'].str.contains(filtro_telefone, case=False, na=False)]
        if filtro_email:
            df_sem_id = df_sem_id[df_sem_id['Email'].str.contains(filtro_email, case=False, na=False)]

        # Renderizando a tabela
        if not df_sem_id.empty:
            st.dataframe(df_sem_id, use_container_width=True)
        else:
            st.warning("Nenhuma editora encontrado com os critérios fornecidos.")
    else:
        st.warning("Não foram encontrados editoras no banco de dados.")

def adicionar_info(tipo):
    conn = get_connection()
    cursor = conn.cursor()

    if tipo == "Autor":
        with st.form(key='form_adicionar_autor'):
            nome_autor = st.text_input("Nome do Autor")
            nacionalide_autor = st.text_input("Nacionalidade do Autor")
            data_autor = st.date_input("Data de Nascimento do Autor", value=None)

            submit = st.form_submit_button("Adicionar Autor")
            if submit and nome_autor == "":
                st.error("O nome do Autor não pode estar vazio!")
            elif submit:
                # Verifica se a data foi fornecida
                if data_autor:
                    data_autor_str = f"'{data_autor.strftime('%Y-%m-%d')}'"
                else:
                    data_autor_str = "Null"

                query = f"INSERT INTO autores (nome_autor, nacionalidade_autor, data_nasc_autor) VALUES ('{nome_autor}', '{nacionalide_autor}', {data_autor_str})"
                try:
                    cursor.execute(query)
                    conn.commit()
                    st.success("Autor adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar autor: {e}")
    if tipo == "Tradutor":
        with st.form(key='form_adicionar_tradutor'):
            nome_tradutor = st.text_input("Nome do Tradutor")
            nacionalide_tradutor = st.text_input("Nacionalidade do Tradutor")
            data_tradutor = st.date_input("Data de Nascimento do Tradutor", value=None)

            submit = st.form_submit_button("Adicionar Tradutor")
            if submit and nome_tradutor == "":
                st.error("O nome do Tradutor não pode estar vazio!")
            elif submit:
                # Verifica se a data foi fornecida
                if data_tradutor:
                    data_tradutor_str = f"'{data_tradutor.strftime('%Y-%m-%d')}'"
                else:
                    data_tradutor_str = "Null"

                query = f"INSERT INTO tradutores (nome_tradutor, nacionalidade_tradutor, data_nasc_tradutor) VALUES ('{nome_tradutor}', '{nacionalide_tradutor}', {data_tradutor_str})"
                try:
                    cursor.execute(query)
                    conn.commit()
                    st.success("Tradutor adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar tradutor: {e}")
    if tipo == "Gênero":
        with st.form(key='form_adicionar_genero'):
            genero = st.text_input("Gênero")
            desc = st.text_area("Descrição", height=150)
            
            submit = st.form_submit_button("Adicionar Gênero")
            if submit and genero == "":
                st.error("O Gênero não pode estar vazio!")
            elif submit:
                query = f"INSERT INTO generos (nome_genero, desc_genero) VALUES ('{genero}', '{desc}')"
                try:
                    cursor.execute(query)
                    conn.commit()
                    st.success("Gênero adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar gênero: {e}")
    if tipo == "Editora":
         with st.form(key='form_adicionar_editora'):
            nome = st.text_input("Nome da Editora")
            telefone = st.text_input("Telefone da Editora")
            email = st.text_input("Email da Editora")
            
            submit = st.form_submit_button("Adicionar Editora")
            if submit and nome == "":
                st.error("O nome da Editora não pode estar vazio!")
            elif submit:
                query = f"INSERT INTO editora (nome_editora, telefone_editora, email_editora) VALUES ('{nome}', '{telefone}', '{email}')"
                try:
                    cursor.execute(query)
                    conn.commit()
                    st.success("Editora adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar editora: {e}")

    cursor.close()
    conn.close()


def editar_info(tipo):
    conn = get_connection()
    cursor = conn.cursor()

    #Autor
    if tipo == "Autor":
        #Defenir Parametros
        tabela = "autores"
        info = "nome_autor"

        cursor.execute("SELECT nome_autor FROM autores")
        autores = cursor.fetchall()
        autores = [autor[0] for autor in autores]
        info_editar = st.selectbox("Selecione o autor que deseja editar", autores)
        qual_info = st.selectbox("Qual informação deseja editar?", ["Nome", "Nacionalidade", "Data de Nascimento"])

        #Nome do Autor
        if qual_info == "Nome":
            #Definir Parametros
            coluna = "nome_autor"
            nova_info = st.text_input("Insira o novo nome do autor")

        #Nacionalidade do Autor
        elif qual_info == "Nacionalidade":
            #Definir Parametros
            coluna = "nacionalidade_autor"
            nova_info = st.text_input("Insira a novo nacionalidade do autor")

        #Nascimento do Autor
        elif qual_info == "Data de Nascimento":
            #Definir Parametros
            coluna = "data_nasc_autor"
            nova_info = st.date_input("Insira a nova data de nascimento do autor", value=None)
            if nova_info:
                nova_info = f"{nova_info.strftime('%Y-%m-%d')}"
            else:
                nova_info = "Null"

    #Tradutor
    if tipo == "Tradutor":
        #Defenir Parametros
        tabela = "tradutores"
        info = "nome_tradutor"

        cursor.execute("SELECT nome_tradutor FROM tradutores")
        tradutores = cursor.fetchall()
        tradutores = [tradutor[0] for tradutor in tradutores]
        info_editar = st.selectbox("Selecione o tradutor que deseja editar", tradutores)
        qual_info = st.selectbox("Qual informação deseja editar?", ["Nome", "Nacionalidade", "Data de Nascimento"])

        #Nome do Tradutor
        if qual_info == "Nome":
            #Definir Parametros
            coluna = "nome_tradutor"
            nova_info = st.text_input("Insira o novo nome do tradutor")

        #Nacionalidade do Tradutor
        elif qual_info == "Nacionalidade":
            #Definir Parametros
            coluna = "nacionalidade_tradutor"
            nova_info = st.text_input("Insira a novo nacionalidade do tradutor")

        #Nascimento do Tradutor
        elif qual_info == "Data de Nascimento":
            #Definir Parametros
            coluna = "data_nasc_tradutor"
            nova_info = st.date_input("Insira a nova data de nascimento do tradutor", value=None)
            if nova_info:
                nova_info = f"{nova_info.strftime('%Y-%m-%d')}"
            else:
                nova_info = "Null"

    #Generos
    if tipo == "Gênero":
        #Defenir Parametros
        tabela = "generos"
        info = "nome_genero"

        cursor.execute("SELECT nome_genero FROM generos")
        generos = cursor.fetchall()
        generos = [genero[0] for genero in generos]
        info_editar = st.selectbox("Selecione o genero que deseja editar", generos)
        qual_info = st.selectbox("Qual informação deseja editar?", ["Nome", "Descrição"])

        #Nome do Gênero
        if qual_info == "Nome":
            #Definir Parametros
            coluna = "nome_genero"
            nova_info = st.text_input("Insira o novo nome do genero")

        #Descrição do Gênero
        elif qual_info == "Descrição":
            #Definir Parametros
            coluna = "desc_genero"
            nova_info = st.text_area("Insira a novo descrição do genero")

    #Editora
    if tipo == "Editora":
        #Defenir Parametros
        tabela = "editora"
        info = "nome_editora"

        cursor.execute("SELECT nome_editora FROM editora")
        editoras = cursor.fetchall()
        editoras = [editora[0] for editora in editoras]
        info_editar = st.selectbox("Selecione a editora que deseja editar", editoras)
        qual_info = st.selectbox("Qual informação deseja editar?", ["Nome", "Telefone", "Email"])

        #Nome da Editora
        if qual_info == "Nome":
            #Definir Parametros
            coluna = "nome_editora"
            nova_info = st.text_input("Insira o novo nome da editora")

        #Telefone da Editora
        elif qual_info == "Telefone":
            #Definir Parametros
            coluna = "telefone_editora"
            nova_info = st.text_input("Insira o novo telefone da editora")

        #Email da Editora
        elif qual_info == "Email":
            #Definir Parametros
            coluna = "email_editora"
            nova_info = st.text_input("Insira o novo email da editora")

    #Editar info
    if st.button("Editar"):
        try:
            cursor.execute(f"UPDATE {tabela} SET {coluna} = %s WHERE {info} = %s", (nova_info, info_editar))
            conn.commit()
            st.success("Informação alterada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao alterar informação: {e}")
        finally:
            cursor.close()
            conn.close()

def apagar_info(tipo):
    conn = get_connection()
    cursor = conn.cursor()

    #Autores
    if tipo == "Autor":
        cursor.execute("SELECT nome_autor FROM autores")
        autores = cursor.fetchall()
        autores = [autor[0] for autor in autores]
        info_apagar = st.selectbox("Seleciona o autor que deseja apagar", autores)
        cursor.execute("SELECT id_autor FROM autores WHERE nome_autor = %s", (info_apagar,))
        id_apagar = cursor.fetchall()
        id_apagar = id_apagar[0][0]
    
    #Tradutores
    elif tipo == "Tradutor":
        cursor.execute("SELECT nome_tradutor FROM tradutores")
        tradutores = cursor.fetchall()
        tradutores = [tradutor[0] for tradutor in tradutores]
        info_apagar = st.selectbox("Seleciona o tradutor que deseja apagar", tradutores)
        cursor.execute("SELECT id_tradutor FROM tradutores WHERE nome_tradutor = %s", (info_apagar,))
        id_apagar = cursor.fetchall()
        id_apagar = id_apagar[0][0]

    #Gêneros
    elif tipo == "Gênero":
        cursor.execute("SELECT nome_genero FROM generos")
        generos = cursor.fetchall()
        generos = [genero[0] for genero in generos]
        info_apagar = st.selectbox("Seleciona o genero que deseja apagar", generos)
        cursor.execute("SELECT id_genero FROM generos WHERE nome_genero = %s", (info_apagar,))
        id_apagar = cursor.fetchall()
        id_apagar = id_apagar[0][0]

    #Editoras
    elif tipo == "Editora":
        cursor.execute("SELECT nome_editora FROM editora")
        editoras = cursor.fetchall()
        editoras = [editor[0] for editor in editoras]
        info_apagar = st.selectbox("Seleciona a editora que deseja apagar", editoras)
        cursor.execute("SELECT id_editora FROM editora WHERE nome_editora = %s", (info_apagar,))
        id_apagar = cursor.fetchall()
        id_apagar = id_apagar[0][0]

    #Clicar Deletar
    if st.button("Deletar"):
        #Autores
        if tipo == "Autor":
            #Verificar validade
            cursor.execute("SELECT id_autor FROM livro_autor WHERE id_autor = %s", (id_apagar,))
            validar_autor = cursor.fetchall()
            if len(validar_autor) > 0:
                st.error("Um autor vincaludo a um livro não pode ser deletado! Primeiramente disvincule aquele autor do livro")
            else:
                cursor.execute("DELETE FROM autores WHERE id_autor = %s", (id_apagar,))
                conn.commit()
                st.success("Autor apagado com sucesso!")
            
        #Tradutores
        elif tipo == "Tradutor":
            cursor.execute("DELETE FROM tradutores WHERE id_tradutor = %s", (id_apagar,))
            conn.commit()
            st.success("Tradutor apagado com sucesso!")

        #Gêneros
        elif tipo == "Gênero":
            cursor.execute("DELETE FROM generos WHERE id_genero = %s", (id_apagar,))
            conn.commit()
            st.success("Gênero apagado com sucesso!")

        #Editoras
        elif tipo == "Editora":
            cursor.execute("DELETE FROM editora WHERE id_editora = %s", (id_apagar,))
            conn.commit()
            st.success("Editora apagado com sucesso!")

    cursor.close()
    conn.close()

def alterar_info(tipo):
    # Lógica para adicionar, editar e apagar info
    if tipo == "Autores":
        tipo = "Autor"
    if tipo == "Tradutores":
        tipo = "Tradutor"
    if tipo == "Gêneros":
        tipo = "Gênero"
    if tipo == "Editoras":
        tipo = "Editora"
    with st.expander(f"Adicionar, Editar e Apagar {tipo}", expanded=True):
        opcoes = st.selectbox("O que deseja fazer?", [f'Adicionar {tipo}', f'Editar {tipo}', f'Apagar {tipo}'])
        if opcoes == f'Adicionar {tipo}':
            adicionar_info(tipo)     
        elif opcoes == f'Editar {tipo}':
            editar_info(tipo)       
        elif opcoes == f'Apagar {tipo}':
            apagar_info(tipo)

def pag_gerenciar_outros():
    tipo_info = st.selectbox("Qual informação deseja gerenciar?", ["Autores", "Tradutores", "Gêneros", "Editoras"])
    if tipo_info == "Autores":
        apresenta_autor()
        alterar_info(tipo_info)   
    elif tipo_info == "Tradutores":
        apresenta_tradutor()
        alterar_info(tipo_info)  
    elif tipo_info == "Gêneros":
        apresenta_genero()
        alterar_info(tipo_info)  
    elif tipo_info == "Editoras":
        apresenta_editora()
        alterar_info(tipo_info)  

pag_gerenciar_outros()