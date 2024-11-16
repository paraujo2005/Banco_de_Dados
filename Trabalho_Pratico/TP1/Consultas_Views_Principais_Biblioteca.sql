USE Biblioteca;

-- 1. Consulta: Listar todos os livros com suas editoras e autores
SELECT 
    l.titulo AS Titulo_Livro, 
    e.nome_editora AS Editora,
    a.nome_autor AS Autor
FROM 
    livros l
JOIN 
    editora e ON l.id_editora = e.id_editora
JOIN 
    livro_autor la ON l.id_livro = la.id_livro
JOIN 
    autores a ON la.id_autor = a.id_autor;

-- 2. Consulta: Listar os livros e seus respectivos gêneros
SELECT 
    l.titulo AS Titulo_Livro, 
    g.nome_genero AS Genero
FROM 
    livros l
JOIN 
    livro_genero lg ON l.id_livro = lg.id_livro
JOIN 
    generos g ON lg.id_genero = g.id_genero;

-- 3. Consulta: Exibir livros com mais de uma cópia disponível
SELECT 
    titulo, 
    num_copias_disponiveis
FROM 
    livros
WHERE 
    num_copias_disponiveis > 1;

-- 4. Consulta: Listar livros emprestados e seus clientes
SELECT 
    e.nome_cliente AS Cliente, 
    l.titulo AS Titulo_Livro, 
    emp.status AS Status_Empréstimo, 
    emp.data_emprestimo, 
    emp.data_devolucao_prevista
FROM 
    emprestimos emp
JOIN 
    clientes e ON emp.id_cliente = e.id_cliente
JOIN 
    exemplares ex ON emp.id_exemplar = ex.id_exemplar
JOIN 
    livros l ON ex.id_livro = l.id_livro
WHERE 
    emp.status = 'ativo';

-- 5. Consulta: Listar clientes com livros atrasados
SELECT 
    c.nome_cliente AS Cliente, 
    l.titulo AS Titulo_Livro, 
    emp.data_emprestimo, 
    emp.data_devolucao_prevista, 
    emp.data_devolucao
FROM 
    emprestimos emp
JOIN 
    clientes c ON emp.id_cliente = c.id_cliente
JOIN 
    exemplares ex ON emp.id_exemplar = ex.id_exemplar
JOIN 
    livros l ON ex.id_livro = l.id_livro
WHERE 
    emp.status = 'atrasado';

-- 6. Consulta: Quantidade de exemplares por livro
SELECT 
    l.titulo AS Titulo_Livro, 
    COUNT(ex.id_exemplar) AS Quantidade_Exemplares
FROM 
    exemplares ex
JOIN 
    livros l ON ex.id_livro = l.id_livro
GROUP BY 
    l.titulo;

-- 7. Consulta: Exibir autores e livros que não foram emprestados
SELECT 
    a.nome_autor AS Autor, 
    l.titulo AS Titulo_Livro
FROM 
    autores a
JOIN 
    livro_autor la ON a.id_autor = la.id_autor
JOIN 
    livros l ON la.id_livro = l.id_livro
LEFT JOIN 
    exemplares ex ON l.id_livro = ex.id_livro
LEFT JOIN 
    emprestimos emp ON ex.id_exemplar = emp.id_exemplar
WHERE 
    emp.id_emprestimo IS NULL;

-- 8. Consulta: Relatório de livros por editora
SELECT 
    e.nome_editora AS Editora, 
    COUNT(l.id_livro) AS Quantidade_Livros
FROM 
    editora e
JOIN 
    livros l ON e.id_editora = l.id_editora
GROUP BY 
    e.nome_editora;

-- 9. Consulta: Relatório de livros com seu status de disponibilidade
SELECT 
    l.titulo AS Titulo_Livro, 
    CASE 
        WHEN ex.disponibilidade = TRUE THEN 'Disponível' 
        ELSE 'Indisponível' 
    END AS Status_Disponibilidade
FROM 
    livros l
JOIN 
    exemplares ex ON l.id_livro = ex.id_livro;

-- 10. Consulta: Contagem de livros por gênero
SELECT 
    g.nome_genero AS Genero, 
    COUNT(l.id_livro) AS Quantidade_Livros
FROM 
    generos g
JOIN 
    livro_genero lg ON g.id_genero = lg.id_genero
JOIN 
    livros l ON lg.id_livro = l.id_livro
GROUP BY 
    g.nome_genero;


-- -------------------------------
-- Criação de Views

-- 1. View: Livros Disponíveis
CREATE VIEW livros_disponiveis AS
SELECT 
    l.titulo AS Titulo_Livro, 
    e.nome_editora AS Editora,
    COUNT(ex.id_exemplar) AS Exemplares_Disponiveis
FROM 
    livros l
JOIN 
    editora e ON l.id_editora = e.id_editora
JOIN 
    exemplares ex ON l.id_livro = ex.id_livro
WHERE 
    ex.disponibilidade = TRUE
GROUP BY 
    l.titulo, e.nome_editora;

-- 2. View: Relatório de Empréstimos Ativos
CREATE VIEW emprestimos_ativos AS
SELECT 
    e.nome_cliente AS Cliente, 
    l.titulo AS Titulo_Livro, 
    emp.data_emprestimo, 
    emp.data_devolucao_prevista
FROM 
    emprestimos emp
JOIN 
    clientes e ON emp.id_cliente = e.id_cliente
JOIN 
    exemplares ex ON emp.id_exemplar = ex.id_exemplar
JOIN 
    livros l ON ex.id_livro = l.id_livro
WHERE 
    emp.status = 'ativo';

-- 3. View: Livros Emprestados
CREATE VIEW livros_emprestados AS
SELECT 
    l.titulo AS Titulo_Livro, 
    e.nome_cliente AS Cliente,
    emp.data_emprestimo, 
    emp.data_devolucao_prevista
FROM 
    emprestimos emp
JOIN 
    exemplares ex ON emp.id_exemplar = ex.id_exemplar
JOIN 
    livros l ON ex.id_livro = l.id_livro
JOIN 
    clientes e ON emp.id_cliente = e.id_cliente;
