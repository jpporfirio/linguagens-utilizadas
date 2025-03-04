import requests
import base64

class RepoGitHub:

    def __init__(self, path, token):
        self.repo = 'repositório desejado'  # Substitua pelo nome do repositório que você deseja criar/atualizar
        self.path = path
        self.username = 'seu usuário'  # Substitua pelo seu nome de usuário do GitHub
        self.token = token
        self.headers = {'Authorization': 'Bearer ' + self.token,
           'X-GitHub-Api-Version': '2022-11-28'}
        
    def create_repo(self):
        data = {
            'name': self.repo,
            'description': 'Repositorio com as linguagens de programação utilizadas',
            'private': False
        }
        url = f'https://api.github.com/users/{self.username}/repos'

        post = requests.post(url = url, json = data, headers = self.headers)
        return post.status_code


    def update_repo(self):

        with open (self.path, 'rb') as file:
            content = file.read()
        encode = base64.b64encode(content)

        data = {
            'message': 'Adicionando um novo arquivo',
            'content': encode.decode('utf-8')
        }        
        url = f'https://api.github.com/repos/{self.username}/{self.repo}/contents/{self.path}'
        put = requests.put(url = url, json = data, headers = self.headers)

        return put.status_code


# Exemplo de uso
if __name__ == "__main__":
    path = 'spotify.csv'  # Caminho para o arquivo que você deseja enviar
    token = 'seu token'  # Substitua pelo seu token de acesso pessoal do GitHub

    # Crie um objeto da classe RepoGitHub
    repo_github = RepoGitHub(path, token)

    # Teste o método create_repo
    status_code_create = repo_github.create_repo()
    print(f'Status code da criação do repositório: {status_code_create}')
    # Espera-se que o status code seja 201 se o repositório for criado com sucesso

    # Teste o método update_repo
    status_code_update = repo_github.update_repo()
    print(f'Status code da atualização do repositório: {status_code_update}')