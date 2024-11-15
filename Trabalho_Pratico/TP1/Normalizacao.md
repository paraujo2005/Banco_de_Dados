# Esquema de Normalização

## 1ª Forma Normal (1FN)

Regras aplicadas:
1. Todas as tabelas têm colunas e linhas organizadas.
2. Cada célula contém apenas um valor (atomicidade).
3. Cada linha é única e identificada por uma chave primária.
4. Cada coluna armazene valores do mesmo tipo de dado.

### Como foi aplicado:
- Todas as tabelas foram estruturadas para atender à 1FN, pois:
  - Não há grupos repetitivos ou valores compostos.
  - Cada célula contém apenas um valor.
  - Cada linha é identificada por uma chave primária.

### Exemplo:
Na tabela `clientes`, os dados de contato (telefone e e-mail) são separados, e o `cpf_cliente` é único:

Tabela: clientes
| id\_cliente | nome\_cliente  | cpf\_cliente  | telefone\_cliente | email\_cliente   |
|-------------|----------------|---------------|-------------------|------------------|
| 1           | João Silva     | 12345678900   | 999999999         | joao@email.com   |
| 2           | Maria Souza    | 09876543211   | 888888888         | maria@email.com  |

---

## 2ª Forma Normal (2FN)

Regras aplicadas:
1. O banco está na 1FN.
2. Todos os atributos não-chave dependem integralmente da chave primária (não pode haver dependência parcial).

### Como foi aplicado:
- Não há dependências parciais em tabelas com chaves compostas, como `livro_tradutor`, `livro_autor` e `livro_genero`. Todos os atributos em tabelas associativas dependem exclusivamente da combinação das chaves primárias.
- Campos como `id_editora` em `livros` referenciam a tabela `editora`, garantindo que as informações relacionadas à editora estejam normalizadas em sua própria tabela.

### Exemplo:
A tabela `livros` separa as informações da editora para evitar redundância:

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

## A 3ª Forma Normal (3FN)

Regras aplicadas:
1. O banco deve estar na 2FN.
2. Nenhum atributo não-chave deve depender de outro atributo não-chave (eliminação de dependências transitivas).

### Como foi aplicado:
- Na tabela `clientes`, as informações pessoais (e.g., nome, telefone) dependem apenas de `id_cliente`. Não há dependências transitivas.
- Na tabela `livros`, os dados de `id_editora` apontam para a tabela `editora`. Os dados da editora (como nome e e-mail) não dependem do livro, eliminando dependências transitivas.

### Exemplo:
Dependências transitivas foram eliminadas nas tabelas relacionadas:

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

1. **1FN**: Todos os atributos são atômicos e as tabelas possuem identificadores únicos.
2. **2FN**: Atributos dependem integralmente das chaves primárias.
3. **3FN**: Nenhum atributo depende transitivamente de outro atributo não-chave.

Esses passos garantem que o banco de dados esteja devidamente normalizado, evitando redundâncias e anomalias de atualização.

