# Esquema de Normalização

## 1ª Forma Normal (1FN)

Regras aplicadas:
1. Todas as tabelas têm colunas e linhas organizadas.
2. Cada célula contém apenas um valor (atomicidade).
3. Cada linha é única e identificada por uma chave primária.

### Exemplo aplicado na tabela `clientes`:

Tabela: clientes
+-------------+-------------+------------+----------------+------------------+
| id_cliente  | nome_cliente| cpf_cliente| telefone_cliente| email_cliente    |
+-------------+-------------+------------+----------------+------------------+
| 1           | João Silva  | 12345678900| 999999999      | joao@email.com   |
| 2           | Maria Souza | 09876543211| 888888888      | maria@email.com  |
+-------------+-------------+------------+----------------+------------------+

---

## 2ª Forma Normal (2FN)

Regras aplicadas:
1. O banco está na 1FN.
2. Todos os atributos não-chave dependem integralmente da chave primária.

### Exemplo aplicado às tabelas `livros` e `editora`:

Tabela: livros
+----------+-------------+--------+------------+----------------+
| id_livro | titulo      | edicao | id_editora | ano_publicacao |
+----------+-------------+--------+------------+----------------+
| 1        | Livro A     | 1      | 1          | 2020           |
| 2        | Livro B     | 2      | 2          | 2019           |
+----------+-------------+--------+------------+----------------+

Tabela: editora
+-----------+------------------+-----------------+----------------+
| id_editora| nome_editora     | telefone_editora| email_editora  |
+-----------+------------------+-----------------+----------------+
| 1         | Editora Alpha    | 111111111       | alpha@email.com|
| 2         | Editora Beta     | 222222222       | beta@email.com |
+-----------+------------------+-----------------+----------------+

---

## 3ª Forma Normal (3FN)

Regras aplicadas:
1. O banco está na 2FN.
2. Não há dependência transitiva entre atributos não-chave.

### Exemplo aplicado às tabelas `clientes` e `emprestimos`:

Tabela: clientes
+-------------+----------------+------------------+----------------+
| id_cliente  | nome_cliente   | cpf_cliente      | telefone_cliente|
+-------------+----------------+------------------+----------------+
| 1           | João Silva     | 12345678900      | 999999999       |
| 2           | Maria Souza    | 09876543211      | 888888888       |
+-------------+----------------+------------------+----------------+

Tabela: emprestimos
+-------------+-------------+-------------+----------------+
| id_emprestimo| id_cliente | id_exemplar | status         |
+-------------+-------------+-------------+----------------+
| 1           | 1           | 100         | ativo          |
| 2           | 2           | 101         | finalizado     |
+-------------+-------------+-------------+----------------+

---

## Considerações Finais

1. **1FN**: As tabelas possuem dados atômicos, sem valores repetidos em células.
2. **2FN**: Todos os atributos não-chave são dependentes da chave primária.
3. **3FN**: Eliminação de dependências transitivas, garantindo que não existam atributos não-chave dependentes de outros atributos não-chave.

Esses passos garantem que o banco de dados esteja devidamente normalizado, evitando redundâncias e anomalias de atualização.
