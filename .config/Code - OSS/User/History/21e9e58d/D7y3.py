import requests
from lxml import html
import json

def fetch_river_height():
    url = 'https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            # Use XPath to find the element in the table
            height = tree.xpath('/html/body/div/div/section[2]/section/div[1]/div/div/div[2]/div/div/div/div/table/tbody/tr[1]/td[2]/text()')
            if height:
                return height[0].strip()  # Return the text of the found element
            else:
                return None
        else:
            return None
    except requests.exceptions.RequestException:
        return None

if __name__ == "__main__":
    height = fetch_river_height()
    if height is not None:
        # Print the height in a JSON format suitable for Waybar
        result = {f"{height} metros"}
        print(result)
    else:
        # Print an empty JSON to clear the output in Waybar if data is not available
        print(json.dumps({}))
