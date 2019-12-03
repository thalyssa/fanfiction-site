# Site de Fanfics

O objetivo do projeto é a construção de um site para leitura e publicação de fanfics¹. O site deve permitir o cadastro de usuários, que podem ou não publicar suas próprias histórias, e exibir um painel específico para os administradores, que possibilita a adição de novas categorias e o banimento de contas.

As histórias publicadas no site possuem nome, ID (Gerado automaticamente), classificação, gêneros (Escolhidos numa lista pré-definida), categoria, sinopse, estado (Concluída ou em andamento) e capítulos. 

## Funcionalidades

**Criar perfil:** Compostos por usuário (Único), e-mail e senha. Devem exibir as histórias do usuário, seus favoritos e uma descrição personalizável pelo próprio usuário.

**Editar perfil:** O usuário deve ser capaz de fazer alterações em todos os atributos do seu perfil.

**Pesquisar história:** Dado o nome de uma história, o site deve retornar todas as histórias correspondentes ao parâmetro.

**Criar história:** Recebendo os atributos necessários (nome, classificação, gêneros, categoria e sinopse), o sistema registra a história, automaticamente associando-a ao usuário que a criou e gerando um ID único. Uma história, quando criada, obrigatoriamente deve receber o primeiro capítulo.

**Ler história:** Permite ao usuário visualizar as histórias publicadas no site.

**Adicionar capítulo:** Recebe um título e a descrição do capítulo para postá-lo. O capítulo é obrigatoriamente associado a uma história.

**Excluir capítulo:** Remove os dados associados a um determinado capítulo.

**Excluir história:** Remove os dados associados a uma determinada história e não a exibe mais no perfil do autor.

**Adicionar história à lista de favoritos:** Permite que um usuário adicione uma história à sua lista de favoritos, que é exibida em seu perfil.

**Adicionar autor aos favoritos:** Permite que um usuário adicione outro à sua lista de favoritos, que é exibida em seu perfil.

**Gerenciar usuários:** [Função exclusiva para o administrador do site] Permite que o administrador exclua contas de usuário.  

## Glossário

**¹Fanfic:** História escrita e divulgada por fãs que se utiliza de personagens ou ambientações já existentes na cultura midiática (Livros, animes, mangás, videogames, filmes, etc.)
