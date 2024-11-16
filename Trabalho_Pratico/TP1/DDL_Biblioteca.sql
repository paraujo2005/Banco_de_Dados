-- Criação do Database
CREATE DATABASE Biblioteca;
USE Biblioteca;

-- Criação da tabela editora
CREATE TABLE editora (
    id_editora INT PRIMARY KEY,
    nome_editora VARCHAR(150) NOT NULL,
    telefone_editora VARCHAR(15),
    email_editora VARCHAR(255)
);

-- Criação da tabela livros
CREATE TABLE livros (
    id_livro INT PRIMARY KEY,
    isbn VARCHAR(13) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    edicao INT,
    id_editora INT,
    ano_publicacao INT,
    local_publicacao VARCHAR(100),
    num_copias INT NOT NULL,
    num_copias_disponiveis INT NOT NULL,
    CONSTRAINT fk_livros_id_editora FOREIGN KEY (id_editora) REFERENCES editora(id_editora)
);

-- Criação da tabela generos
CREATE TABLE generos (
    id_genero INT PRIMARY KEY,
    nome_genero VARCHAR(50) NOT NULL,
    desc_genero TEXT
);

-- Criação da tabela livro_genero
CREATE TABLE livro_genero (
    id_livro INT,
    id_genero INT,
    PRIMARY KEY (id_livro, id_genero),
    CONSTRAINT fk_livro_genero_id_livro FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
    CONSTRAINT fk_livro_genero_id_genero FOREIGN KEY (id_genero) REFERENCES generos(id_genero)
);

-- Criação da tabela autores
CREATE TABLE autores (
    id_autor INT PRIMARY KEY,
    nome_autor VARCHAR(150) NOT NULL,
    nacionalidade_autor VARCHAR(100),
    data_nasc_autor DATE
);

-- Criação da tabela livro_autor
CREATE TABLE livro_autor (
    id_livro INT,
    id_autor INT,
    PRIMARY KEY (id_livro, id_autor),
    CONSTRAINT fk_livro_autor_id_livro FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
    CONSTRAINT fk_livro_autor_id_autor FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
);

-- Criação da tabela tradutores
CREATE TABLE tradutores (
    id_tradutor INT PRIMARY KEY,
    nome_tradutor VARCHAR(150) NOT NULL,
    nacionalidade_tradutor VARCHAR(100),
    data_nasc_tradutor DATE
);

-- Criação da tabela livro_tradutor
CREATE TABLE livro_tradutor (
    id_livro INT,
    id_tradutor INT,
    PRIMARY KEY (id_livro, id_tradutor),
    CONSTRAINT fk_livro_tradutor_id_livro FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
    CONSTRAINT fk_livro_tradutor_id_tradutor FOREIGN KEY (id_tradutor) REFERENCES tradutores(id_tradutor)
);

-- Criação da tabela exemplares
CREATE TABLE exemplares (
    id_exemplar INT PRIMARY KEY,
    id_livro INT,
    disponibilidade BOOLEAN NOT NULL,
    local_exemplar VARCHAR(50),
    CONSTRAINT fk_exemplares_id_livro FOREIGN KEY (id_livro) REFERENCES livros(id_livro)
);

-- Criação da tabela clientes
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nome_cliente VARCHAR(150) NOT NULL,
    cpf_cliente VARCHAR(11) UNIQUE NOT NULL,
    email_cliente VARCHAR(255),
    telefone_cliente VARCHAR(15),
    data_nasc_cliente DATE,
    endereco_cliente VARCHAR(255)
);

-- Criação da tabela emprestimos
CREATE TABLE emprestimos (
    id_emprestimo INT PRIMARY KEY,
    id_cliente INT,
    id_exemplar INT,
    status ENUM('ativo', 'finalizado', 'atrasado') NOT NULL,
    data_emprestimo DATE NOT NULL,
    data_devolucao_prevista DATE NOT NULL,
    data_devolucao DATE,
    quantidade_renovacoes INT DEFAULT 0,
    CONSTRAINT fk_emprestimos_id_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_emprestimos_id_exemplar FOREIGN KEY (id_exemplar) REFERENCES exemplares(id_exemplar)
);