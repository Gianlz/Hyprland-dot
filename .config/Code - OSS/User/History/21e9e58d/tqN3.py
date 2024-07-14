import requests
from lxml import html

def fetch_river_height():
    url = 'https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            # Use XPath para encontrar o elemento desejado na tabela
            height = tree.xpath('/html/body/div/div/section[2]/section/div[1]/div/div/div[2]/div/div/div/div/table/tbody/tr[1]/td[2]/text()')
            if height:
                return height[0].strip()  # Retorna o texto do elemento encontrado
            else:
                print("Altura do rio não encontrada")
                return None
        else:
            print(f"Falha ao buscar dados: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        return None

if __name__ == "__main__":
    height = fetch_river_height()
    if height is not None:
        print(f"{height} metros")
