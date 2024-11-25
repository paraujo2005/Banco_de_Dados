import streamlit as st
import mysql.connector
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Sistema Biblioteca",
    page_icon="📚",
    layout="wide"
)

# Função de conexão com o banco de dados
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="user_biblioteca",
        password="IDP@biblioteca1234",
        database="Biblioteca"
    )

# Função para obter os livros com seus dados
def get_livros():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT l.id_livro, l.titulo, l.isbn, l.edicao, e.nome_editora, l.ano_publicacao, l.local_publicacao,   
           COALESCE(GROUP_CONCAT(DISTINCT a.nome_autor SEPARATOR ', '), 'Nenhum') AS autores, 
           COALESCE(GROUP_CONCAT(DISTINCT t.nome_tradutor SEPARATOR ', '), 'Nenhum') AS tradutores,
           COALESCE(GROUP_CONCAT(DISTINCT g.nome_genero SEPARATOR ', '), 'Nenhum') AS generos, 
            l.num_copias, l.num_copias_disponiveis
    FROM livros l
    JOIN editora e ON l.id_editora = e.id_editora
    LEFT JOIN livro_autor la ON l.id_livro = la.id_livro
    LEFT JOIN autores a ON la.id_autor = a.id_autor
    LEFT JOIN livro_tradutor lt ON l.id_livro = lt.id_livro
    LEFT JOIN tradutores t ON lt.id_tradutor = t.id_tradutor
    LEFT JOIN livro_genero lg ON l.id_livro = lg.id_livro
    LEFT JOIN generos g ON lg.id_genero = g.id_genero
    GROUP BY l.id_livro, l.titulo, l.isbn, l.edicao, e.nome_editora, l.ano_publicacao, l.local_publicacao, l.num_copias, l.num_copias_disponiveis
    """
    cursor.execute(query)
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    return livros

#Função para ver unicidade do ISBN
def verificar_unicidade_isbn(isbn):
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

# Função para pegar valores de algo já na tabela para remover
def remover_algo(tabela, tipo, id_livro):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    SELECT a.id_{tipo}, a.nome_{tipo}
    FROM livro_{tipo} la
    JOIN {tabela} a ON la.id_{tipo} = a.id_{tipo}
    WHERE la.id_livro = %s;
    """
    cursor.execute(query, (id_livro,))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    return resultado

# Função para atualizar tabelas
def atualizar_info_livro(local_info, nova_info, id_livro):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Usar f-strings para incluir o nome da coluna diretamente
        query = f"UPDATE livros SET {local_info} = %s WHERE id_livro = %s"
        cursor.execute(query, (nova_info, id_livro))
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao atualizar a informação: {e}")
    finally:
        cursor.close()
        conn.close()

def atualizar_info_outro(id, tabela, nova_info):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verifica se o valor já existe
        cursor.execute(f"INSERT INTO {tabela} (nome_{id}) VALUES (%s) on DUPLICATE KEY UPDATE id_{id} = LAST_INSERT_ID(id_{id})", (nova_info,))
        conn.commit()
        novo = cursor.lastrowid

        return novo
    except Exception as e:
        st.error(f"Erro ao atualizar a {id}: {e}")
    finally:
        cursor.close()
        conn.close()

# Função para editar o livro
def editar_livro(id_livro):
    # Selecionar qual informação editar
    editar_livro = st.selectbox("Qual informação deseja editar?", [
        'Título', 'ISBN', 'Edição', 'Editora', 'Adicionar Autor', 'Remover Autor',
        'Adicionar Tradutor', 'Remover Tradutor', 'Adicionar Gênero', 'Remover Gênero', 'Ano de Publicação',
        'Local de Publicação'
    ])

    # Criar um formulário para edição
    with st.form(key='form_editar_livro'):
        #Título
        if editar_livro == 'Título':
            novo_titulo = st.text_input('Insira o novo Título do Livro')

        #ISBN
        elif editar_livro == "ISBN":
            novo_isbn = st.text_input('Insira o novo ISBN do Livro')

        #Edição
        elif editar_livro == "Edição":
            nova_edicao = st.number_input('Insira a nova Edição do Livro', min_value=1, step=1)

        #Editora
        elif editar_livro == "Editora":
            nova_editora = st.text_input("Insira o nome da nova Editora")

        #Adicionar Autor
        elif editar_livro == "Adicionar Autor":
            novo_autor = st.text_input("Insira o nome do novo Autor")

        #Remover Autor
        elif editar_livro == "Remover Autor":
            autores = remover_algo("autores", "autor", id_livro)
            autores_dict = {f"{autor[1]}": autor[0] for autor in autores}
            autor_remover = st.selectbox("Selecione o Autor para Remover", list(autores_dict.keys()))

        #Adicionar Tradutor
        elif editar_livro == "Adicionar Tradutor":
            novo_tradutor = st.text_input("Insira o nome do novo Tradutor")

        #Remover Tradutor
        elif editar_livro == "Remover Tradutor":
            tradutores = remover_algo("tradutores", "tradutor", id_livro)
            tradutores_dict = {f"{tradutor[1]}": tradutor[0] for tradutor in tradutores}
            tradutor_remover = st.selectbox("Selecione o Tradutor para Remover", list(tradutores_dict.keys()))

        #Adicionar Gênero
        elif editar_livro == "Adicionar Gênero":
            novo_genero = st.text_input("Insira o nome do novo Gênero")

        #Remover Gênero
        elif editar_livro == "Remover Gênero":
            generos = remover_algo("generos", "genero", id_livro)
            generos_dict = {f"{genero[1]}": genero[0] for genero in generos}
            genero_remover = st.selectbox("Selecione o Gênero para Remover", list(generos_dict.keys()))

        #Ano de Publicação
        elif editar_livro == "Ano de Publicação":
            novo_ano= st.number_input('Insira o novo Ano de Publicação do Livro', min_value=1000, step=1)

        #Local de Publicação
        elif editar_livro == "Local de Publicação":
            novo_local = st.text_input('Insira o novo Local de Publicação do Livro')

        # Botão para submeter o formulário
        submit = st.form_submit_button("Atualizar Livro")
        
        if submit:
            # Título
            if editar_livro == 'Título':
                try:
                    atualizar_info_livro("titulo", novo_titulo, id_livro)
                    st.success("Título atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar o título: {e}")
            
            # ISBN
            elif editar_livro == "ISBN":
                # Verificar se o ISBN é único antes de atualizar
                if not verificar_unicidade_isbn(novo_isbn):
                    st.error("Este ISBN já está cadastrado para outro livro. Por favor, insira um ISBN único.")
                else:
                    try:
                        atualizar_info_livro("isbn", novo_isbn, id_livro)
                        st.success("ISBN atualizado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao atualizar o ISBN: {e}")
            
            # Edição
            elif editar_livro == "Edição":
                try:
                    atualizar_info_livro("edicao", nova_edicao, id_livro)
                    st.success("Edição atualizada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar a Edição: {e}")

            # Editora
            elif editar_livro == "Editora":
                try:
                    editora = atualizar_info_outro("editora", "editora", nova_editora)
                    # Atualiza a editora do livro
                    if editora:
                        id_editora = editora[0]
                        atualizar_info_livro("id_editora", id_editora, id_livro)
                        st.success("Editora atualizada com sucesso!")
                    else:
                        st.error("Erro ao obter o ID da editora após a inserção.")
                except Exception as e:
                    st.error(f"Erro ao atualizar a editora: {e}")

            # Adicionar Autor
            elif editar_livro == "Adicionar Autor":
                try:
                    autor = atualizar_info_outro("autor", "autores", novo_autor)
                    # Adiciona autor ao livro
                    if autor:
                        conn = get_connection()
                        cursor = conn.cursor()
                        id_autor = autor[0]
                        cursor.execute(f"INSERT INTO livro_autor (id_livro, id_autor) VALUES ({id_livro}, {id_autor})")
                        conn.commit()
                        st.success("Autor adicionado com sucesso!")
                    else:
                        st.error("Erro ao obter o ID do autor após a inserção.")
                except Exception as e:
                    st.error(f"Erro ao atualizar o autor: {e}")
                finally:
                    cursor.close()
                    conn.close()

            # Remover Autor
            elif editar_livro == "Remover Autor":
                conn = get_connection()
                cursor = conn.cursor()
                id_autor_remover = autores_dict[autor_remover]
                try:
                    # Remover o autor da associação no banco de dados
                    delete_query = "DELETE FROM livro_autor WHERE id_livro = %s AND id_autor = %s;"
                    cursor.execute(delete_query, (id_livro, id_autor_remover))
                    conn.commit()
                    st.success(f"Autor {autor_remover} removido com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao remover o autor: {e}")
                finally:
                    cursor.close()
                    conn.close()

            # Adicionar Tradutor
            elif editar_livro == "Adicionar Tradutor":
                try:
                    tradutor = atualizar_info_outro("tradutor", "tradutores", novo_tradutor)
                    # Adiciona tradutor ao livro
                    if tradutor:
                        conn = get_connection()
                        cursor = conn.cursor()
                        id_tradutor = tradutor[0]
                        cursor.execute(f"INSERT INTO livro_tradutor (id_livro, id_tradutor) VALUES ({id_livro}, {id_tradutor})")
                        conn.commit()
                        st.success("Tradutor adicionado com sucesso!")
                    else:
                        st.error("Erro ao obter o ID do tradutor após a inserção.")
                except Exception as e:
                    st.error(f"Erro ao atualizar o tradutor: {e}")
                finally:
                    cursor.close()
                    conn.close()

            # Remover Tradutor
            elif editar_livro == "Remover Tradutor":
                conn = get_connection()
                cursor = conn.cursor()
                id_tradutor_remover = tradutores_dict[tradutor_remover]
                try:
                    # Remover o tradutor da associação no banco de dados
                    delete_query = "DELETE FROM livro_tradutor WHERE id_livro = %s AND id_tradutor = %s;"
                    cursor.execute(delete_query, (id_livro, id_tradutor_remover))
                    conn.commit()
                    st.success(f"Tradutor {tradutor_remover} removido com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao remover o tradutor: {e}")
                finally:
                    cursor.close()
                    conn.close()

            # Adicionar Gênero
            elif editar_livro == "Adicionar Gênero":
                try:
                    genero = atualizar_info_outro("genero", "generos", novo_genero)
                    # Adiciona genero ao livro
                    if genero:
                        conn = get_connection()
                        cursor = conn.cursor()
                        id_genero = genero[0]
                        cursor.execute(f"INSERT INTO livro_genero (id_livro, id_genero) VALUES ({id_livro}, {id_genero})")
                        conn.commit()
                        st.success("Genero adicionado com sucesso!")
                    else:
                        st.error("Erro ao obter o ID do genero após a inserção.")
                except Exception as e:
                    st.error(f"Erro ao atualizar o genero: {e}")
                finally:
                    cursor.close()
                    conn.close()

            # Remover Gênero
            elif editar_livro == "Remover Gênero":
                conn = get_connection()
                cursor = conn.cursor()
                id_genero_remover = generos_dict[genero_remover]
                try:
                    # Remover o genero da associação no banco de dados
                    delete_query = "DELETE FROM livro_genero WHERE id_livro = %s AND id_genero = %s;"
                    cursor.execute(delete_query, (id_livro, id_genero_remover))
                    conn.commit()
                    st.success(f"Genero {genero_remover} removido com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao remover o genero: {e}")
                finally:
                    cursor.close()
                    conn.close()

            # Ano de Publicação
            elif editar_livro == "Ano de Publicação":
                try:
                    atualizar_info_livro("ano_publicacao", novo_ano, id_livro)
                    st.success("Ano de Publicação atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar o Ano de Publicação: {e}")

            # Local de Publicação
            elif editar_livro == "Local de Publicação":
                try:
                    atualizar_info_livro("local_publicacao", novo_local, id_livro)
                    st.success("Local de Publicação atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar o Local de Publicação: {e}")

# Função para apagar o livro
def apagar_livro(id_livro):
    if st.button("Confirmar Deleção"):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Obtendo o título do livro antes de deletar
            cursor.execute("SELECT titulo FROM livros WHERE id_livro = %s", (id_livro,))
            livro = cursor.fetchone()

            if livro:
                titulo_livro = livro[0]
                
                # Apagando registros de tabelas relacionadas
                cursor.execute("DELETE FROM exemplares WHERE id_livro = %s", (id_livro,))
                cursor.execute("DELETE FROM livro_autor WHERE id_livro = %s", (id_livro,))
                cursor.execute("DELETE FROM livro_tradutor WHERE id_livro = %s", (id_livro,))
                cursor.execute("DELETE FROM livro_genero WHERE id_livro = %s", (id_livro,))
                
                # Apagando o livro da tabela principal
                cursor.execute("DELETE FROM livros WHERE id_livro = %s", (id_livro,))
                conn.commit()
                
                st.success(f"Livro '{titulo_livro}' apagado com sucesso de todas as tabelas.")
            else:
                st.error(f"Livro com ID {id_livro} não encontrado.")
            
        except Exception as e:
            st.error(f"Erro ao apagar o livro: {e}")
        finally:
            cursor.close()
            conn.close()

# Função principal para gerenciar livros
def gerenciar_livros():
    st.title("Gerenciar Livros")

    # Exibindo tabela de livros
    livros = get_livros()
    if livros:
        df = pd.DataFrame(livros)

        # Tratando valores nulos
        df['autores'] = df['autores'].fillna('Nenhum autor')
        df['tradutores'] = df['tradutores'].fillna('Nenhum tradutor')
        df['generos'] = df['generos'].fillna('Nenhum gênero')

        # Formatando o ano para XXXX
        df['ano_publicacao'] = df['ano_publicacao'].apply(lambda x: f"{x:04d}")

        # Renomeando as colunas para exibição
        df = df.rename(columns={
            'titulo': 'Título',
            'isbn': 'ISBN',
            'edicao': 'Edição',
            'nome_editora': 'Editora',
            'autores': 'Autores',
            'tradutores': 'Tradutores',
            'generos': 'Gêneros',
            'ano_publicacao': 'Ano de Publicação',
            'local_publicacao': 'Local de Publicação',
            'num_copias': 'Exemplares Totais',
            'num_copias_disponiveis': 'Exemplares Disponíveis'
        })

        # Removendo o ID do livro para não exibi-lo na tabela
        df_sem_id = df.drop(columns=['id_livro'])

        # Filtros para a tabela
        with st.sidebar:
            st.header("Filtros de Pesquisa")
            filtro_titulo = st.text_input("Título")
            filtro_isbn = st.text_input("ISBN")
            filtro_editora = st.text_input("Editora")
            filtro_autor = st.text_input("Autor")
            filtro_tradutor = st.text_input("Tradutor")
            filtro_genero = st.text_input("Gênero")

        # Aplicando os filtros
        if filtro_titulo:
            df_sem_id = df_sem_id[df_sem_id['Título'].str.contains(filtro_titulo, case=False, na=False)]
        if filtro_isbn:
            df_sem_id = df_sem_id[df_sem_id['ISBN'].str.contains(filtro_isbn, case=False, na=False)]
        if filtro_editora:
            df_sem_id = df_sem_id[df_sem_id['Editora'].str.contains(filtro_editora, case=False, na=False)]
        if filtro_autor:
            df_sem_id = df_sem_id[df_sem_id['Autores'].str.contains(filtro_autor, case=False, na=False)]
        if filtro_tradutor:
            df_sem_id = df_sem_id[df_sem_id['Tradutores'].str.contains(filtro_tradutor, case=False, na=False)]
        if filtro_genero:
            df_sem_id = df_sem_id[df_sem_id['Gêneros'].str.contains(filtro_genero, case=False, na=False)]

        # Renderizando a tabela filtrada
        if not df_sem_id.empty:
            st.dataframe(
                df_sem_id,
                use_container_width=True
            )
        else:
            st.warning("Nenhum livro encontrado com os critérios fornecidos.")

        # Lógica para editar e apagar livros
        with st.expander("Editar e Apagar Livros", expanded=True):
            # Escolha entre Título ou ISBN
            busca_por = st.radio("Buscar por", ("Título", "ISBN"))
            if busca_por == "Título":
                livro_selecionado = st.selectbox("Selecione o livro por Título", df['Título'].tolist())
                livro_id = int(df.loc[df['Título'] == livro_selecionado, 'id_livro'].values[0])
            else:
                livro_selecionado = st.selectbox("Selecione o livro por ISBN", df['ISBN'].tolist())
                livro_id = int(df.loc[df['ISBN'] == livro_selecionado, 'id_livro'].values[0])

            editar_ou_apagar = st.selectbox("O que deseja fazer?", ['Editar Livro', 'Apagar Livro'])
            if editar_ou_apagar == "Editar Livro":
                editar_livro(livro_id)
            elif editar_ou_apagar == "Apagar Livro":
                apagar_livro(livro_id)

# Chamando a função para exibir a página
gerenciar_livros()