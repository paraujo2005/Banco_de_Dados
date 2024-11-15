# Sistema de Gerenciamento de Biblioteca

## Resumo sobre o Negócio Escolhido
O sistema foi desenvolvido para gerenciar as operações de uma **biblioteca**. Esse tipo de estabelecimento atua no ramo de **cultura e educação**, oferecendo acesso a livros, materiais informativos e outros recursos literários para a comunidade. O objetivo principal é facilitar o empréstimo e a devolução de exemplares, bem como a catalogação de livros, autores, tradutores, editoras e gêneros literários.

---

## Ramo de Atuação
A biblioteca atua no setor de **gestão de acervos literários**, abrangendo:
- **Educação**: Apoiar estudos e pesquisas para estudantes, professores e profissionais.
- **Cultura**: Fomentar a leitura e o acesso a conteúdos históricos, artísticos e técnicos.
- **Entretenimento**: Oferecer romances, ficções e outros gêneros populares para o público em geral.

---

## Tipos de Serviços e Produtos Comercializados
Os serviços oferecidos pela biblioteca incluem:
- **Empréstimo de livros**: Permitir que os clientes retirem exemplares por um período determinado.
- **Renovação de empréstimos**: Extensão do prazo de devolução mediante solicitação.
- **Consulta local**: Disponibilização de exemplares para leitura no ambiente da biblioteca.
- **Catálogo digital**: Acesso à listagem completa de livros e seus detalhes.
- **Cadastro de clientes e acervo**: Registro detalhado de usuários e exemplares.

---

## Principais Atores
Os principais atores do sistema incluem:
- **Clientes**: Usuários que utilizam os serviços de empréstimo e consulta da biblioteca.
- **Funcionários**: Responsáveis por gerenciar o acervo, realizar cadastros e monitorar os empréstimos.
- **Administradores**: Gestores do sistema, responsáveis por manter a integridade dos dados e supervisionar os processos.
- **Autores e Tradutores**: Colaboradores literários associados às obras disponíveis no acervo.

---

## Principais Produtos
- **Livros físicos**: Exemplar principal da biblioteca, categorizado por título, gênero, autor, tradutor e editora.
- **Exemplares**: Cópias físicas individuais dos livros disponíveis para empréstimo ou consulta.

---

## Dados Essenciais
- **Livros**: Informações como ISBN, título, edição, ano e editora.
- **Autores e Tradutores**: Nomes, nacionalidade e data de nascimento.
- **Clientes**: Dados pessoais, como CPF, nome, telefone e endereço.
- **Exemplares**: Disponibilidade e localização na biblioteca.
- **Empréstimos**: Registro de status, datas e quantidade de renovações.

---

## Fluxos de Processos Cotidianos
### 1. Cadastro de Clientes
   - O cliente fornece dados pessoais para ser registrado no sistema.
   - O CPF é usado como identificador único.

### 2. Cadastro de Livros
   - Novos livros são registrados com dados como título, ISBN, autor, editora e gênero.
   - Exemplares físicos são adicionados ao sistema.

### 3. Empréstimo de Livros
   - O cliente solicita o empréstimo de um exemplar disponível.
   - O sistema registra a data do empréstimo e a data prevista para devolução.
   - O status do exemplar é atualizado para **indisponível**.

### 4. Devolução de Livros
   - O cliente devolve o exemplar no prazo estabelecido.
   - O status do exemplar é atualizado para **disponível**.
   - Caso o prazo seja ultrapassado, o status muda para **atrasado** e podem ser aplicadas restrições.

### 5. Renovação de Empréstimos
   - O cliente solicita a renovação do empréstimo.
   - O sistema atualiza a data prevista de devolução e incrementa o contador de renovações.

---

## Regras e Restrições do Negócio
1. **Quantidade de Empréstimos**: Cada cliente pode retirar um número limitado de exemplares simultaneamente.
2. **Prazo de Devolução**: A devolução deve ocorrer até a data prevista para evitar restrições.
3. **Renovações Limitadas**: O cliente pode renovar o empréstimo apenas um número definido de vezes.
4. **Exemplares Indisponíveis**: Não é permitido emprestar exemplares que já estão em uso por outro cliente.
5. **Cadastro Único**: CPF e ISBN devem ser únicos para evitar duplicidades.
6. **Status do Empréstimo**: Um empréstimo só pode ser finalizado quando o exemplar for devolvido.

---

Este sistema garante um fluxo organizado e eficiente para o gerenciamento de uma biblioteca, otimizando processos e reduzindo a probabilidade de erros ou inconsistências nos dados.

