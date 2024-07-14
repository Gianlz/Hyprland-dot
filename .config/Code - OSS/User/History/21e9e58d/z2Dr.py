import requests
from bs4 import BeautifulSoup

def fetch_river_height():
    url = 'https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', attrs={'data-key': '0'})
            if table:
                # Assuming the river height is in the first row, second column (adjust indices as needed)
                cell = table.find_all('td')[1]
                return cell.text.strip()
            else:
                print("Table with data-key='0' not found")
                return None
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    height = fetch_river_height()
    if height is not None:
        print(height)
