# Esquema de Normalização

## 1ª Forma Normal (1FN)

Regras aplicadas:
1. Todas as tabelas têm colunas e linhas organizadas.
2. Cada célula contém apenas um valor (atomicidade).
3. Cada linha é única e identificada por uma chave primária.

### Exemplo aplicado na tabela `clientes`:

Tabela: clientes
| id\_cliente | nome\_cliente  | cpf\_cliente  | telefone\_cliente | email\_cliente   |
|-------------|----------------|---------------|-------------------|------------------|
| 1           | João Silva     | 12345678900   | 999999999         | joao@email.com   |
| 2           | Maria Souza    | 09876543211   | 888888888         | maria@email.com  |

---

## 2ª Forma Normal (2FN)

Regras aplicadas:
1. O banco está na 1FN.
2. Todos os atributos não-chave dependem integralmente da chave primária.

### Exemplo aplicado às tabelas `livros` e `editora`:

Tabela: livros
| id\_livro   | titulo        | edicao | id\_editora | ano\_publicacao |
|-------------|---------------|--------|-------------|-----------------|
| 1           | A Vida        | 1      | 1           | 2020            |
| 2           | O Mundo       | 2      | 2           | 2021            |

Tabela: editora
| id\_editora | nome\_editora | telefone\_editora | email\_editora  |
|-------------|---------------|-------------------|-----------------|
| 1           | Editora X     | 111111111         | editora@x.com   |
| 2           | Editora Y     | 222222222         | editora@y.com   |

---

## 3ª Forma Normal (3FN)

Regras aplicadas:
1. O banco está na 2FN.
2. Não há dependência transitiva entre atributos não-chave.

### Exemplo aplicado às tabelas `clientes` e `emprestimos`:

Tabela: clientes
| id\_cliente | nome\_cliente  | cpf\_cliente  | telefone\_cliente | email\_cliente   |
|-------------|----------------|---------------|-------------------|------------------|
| 1           | João Silva     | 12345678900   | 999999999         | joao@email.com   |
| 2           | Maria Souza    | 09876543211   | 888888888         | maria@email.com  |

Tabela: emprestimos
| id\_emprestimo | id\_cliente | id\_exemplar | status   | data\_emprestimo | data\_devolucao\_prevista | data\_devolucao |
|----------------|------------|--------------|----------|------------------|--------------------------|-----------------|
| 1              | 1          | 2            | ativo    | 2024-10-01       | 2024-10-10               | NULL            |
| 2              | 2          | 3            | finalizado| 2024-09-20       | 2024-09-27               | 2024-09-25      |

---

## Considerações Finais

1. **1FN**: As tabelas possuem dados atômicos, sem valores repetidos em células.
2. **2FN**: Todos os atributos não-chave são dependentes da chave primária.
3. **3FN**: Eliminação de dependências transitivas, garantindo que não existam atributos não-chave dependentes de outros atributos não-chave.

Esses passos garantem que o banco de dados esteja devidamente normalizado, evitando redundâncias e anomalias de atualização.

