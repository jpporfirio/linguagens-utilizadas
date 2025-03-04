import requests
import math
import pandas as pd
import os

class ConsumidorApi:

    def __init__(self, owner, token):
        self.owner = owner
        self.token = token
        self.headers = {
            'Authorization': 'Bearer ' + token,
            'X-GitHub-Api-Version': '2022-11-28'
        }
        self.url = f'https://api.github.com/users/{owner}'
        self.repos_list = self.bringing_data()
        self.repos_dt = self.language_repos()

    def bringing_data(self):
        repos_list = []
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        qtd_repos = response.json().get('public_repos', 0)
        qtd_pages = math.ceil(qtd_repos / 30)

        for i in range(1, qtd_pages + 1):         
            url = self.url + f'/repos?page={i}'
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
                repos_list.extend(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição da página {i}: {e}")
                continue  # Continua para a próxima página em caso de erro
                
        return repos_list

    def language_repos(self):
        dt = []
        dados = self.repos_list
        for repos in dados:
            dt.append([repos.get('name', None), repos.get('language', None)])
        dt = pd.DataFrame(dt, columns=['Repository Name', 'Language'])
        return dt
    
    def write_csv(self):
        self.repos_dt.to_csv(os.getcwd() + '/' +  self.owner + '.csv', index=False)

# Exemplo de uso
if __name__ == "__main__":
    # Defina o proprietário e o token de acesso
    owner = 'spotify'
    token = 'seu token'  # Substitua pelo seu token de acesso pessoal

    # Crie um objeto da classe ConsumidorApi
    consumidor = ConsumidorApi(owner, token)

    # Obtenha os dados dos repositórios
    df = consumidor.language_repos()

    # Exiba os dados dos repositórios
    print(df)

    # Grave os dados em um arquivo CSV
    consumidor.write_csv()
    print(f'Dados gravados em {os.path.join(os.getcwd(), f"{owner}.csv")}')