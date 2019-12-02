
class User:

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def createUser(self):
        name = input("Digite o nome a ser exibido: ")
        username = input("Digite um nome de usuário (Deve ser único e sem caracteres espciais): ")
        email = input("Digite um endereço de e-mail: ")
        password = input("Digite uma senha: ")

        newUser = User(name, username, email, password)
        if(newUser):
            print("Perfil criado com sucesso")
            return True
        else:
            print("Ocorreu um erro, tente novamente")
            return False


