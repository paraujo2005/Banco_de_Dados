USE Biblioteca;

-- Inserir dados na tabela editora
INSERT INTO editora (id_editora, nome_editora, telefone_editora, email_editora)
VALUES
(1, 'Editora Globo', '21-4002-8922', 'contato@editoraglobo.com.br'),
(2, 'Editora Record', '21-2567-4344', 'atendimento@editorarecord.com.br');

-- Inserir dados na tabela livros
INSERT INTO livros (id_livro, isbn, titulo, edicao, id_editora, ano_publicacao, local_publicacao, num_copias, num_copias_disponiveis)
VALUES
(1, '9788532524146', 'O Primo Basílio', 1, 1, 2002, 'São Paulo', 10, 8),
(2, '9788501061286', 'Dom Casmurro', 2, 2, 1995, 'Rio de Janeiro', 5, 5);

-- Inserir dados na tabela generos
INSERT INTO generos (id_genero, nome_genero, desc_genero)
VALUES
(1, 'Romance', 'Gênero literário narrativo, geralmente longo e com história de amor.'),
(2, 'Drama', 'Gênero literário que explora aspectos emocionais da vida humana.');

-- Inserir dados na tabela livro_genero
INSERT INTO livro_genero (id_livro, id_genero)
VALUES
(1, 1),
(2, 2);

-- Inserir dados na tabela autores
INSERT INTO autores (id_autor, nome_autor, nacionalidade_autor, data_nasc_autor)
VALUES
(1, 'José de Alencar', 'Brasileiro', '1829-05-01'),
(2, 'Machado de Assis', 'Brasileiro', '1839-06-21');

-- Inserir dados na tabela livro_autor
INSERT INTO livro_autor (id_livro, id_autor)
VALUES
(1, 1),
(2, 2);

-- Inserir dados na tabela tradutores
INSERT INTO tradutores (id_tradutor, nome_tradutor, nacionalidade_tradutor, data_nasc_tradutor)
VALUES
(1, 'João da Silva', 'Brasileiro', '1980-09-15');

-- Inserir dados na tabela livro_tradutor
INSERT INTO livro_tradutor (id_livro, id_tradutor)
VALUES
(1, 1);

-- Inserir dados na tabela exemplares
INSERT INTO exemplares (id_exemplar, id_livro, disponibilidade, local_exemplar)
VALUES
(1, 1, TRUE, 'Sala 1'),
(2, 2, TRUE, 'Sala 2');

-- Inserir dados na tabela clientes
INSERT INTO clientes (id_cliente, nome_cliente, cpf_cliente, email_cliente, telefone_cliente, data_nasc_cliente, endereco_cliente)
VALUES
(1, 'Ana Souza', '12345678901', 'ana.souza@email.com', '21-98765-4321', '1990-07-15', 'Rua A, 123'),
(2, 'Carlos Lima', '98765432100', 'carlos.lima@email.com', '21-12345-6789', '1985-02-10', 'Rua B, 456');

-- Inserir dados na tabela emprestimos
INSERT INTO emprestimos (id_emprestimo, id_cliente, id_exemplar, status, data_emprestimo, data_devolucao_prevista, data_devolucao, quantidade_renovacoes)
VALUES
(1, 1, 1, 'ativo', '2024-11-15', '2024-11-22', NULL, 0),
(2, 2, 2, 'finalizado', '2024-11-10', '2024-11-17', '2024-11-17', 1);