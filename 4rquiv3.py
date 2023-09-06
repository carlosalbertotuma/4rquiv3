import argparse
import requests
import sys

# Banner de uso
banner = '''
##        ########   #######  ##     ## #### ##     ##  #######  
##    ##  ##     ## ##     ## ##     ## #### ##     ## ##     ## 
##    ##  ##     ## ##     ## ##     ## #### ##     ##        ## 
##    ##  ########  ##     ## ##     ##  ##  ##     ##  #######  
######### ##   ##   ##  ## ## ##     ##       ##   ##         ## 
      ##  ##    ##  ##    ##  ##     ## ####   ## ##   ##     ## 
      ##  ##     ##  ##### ##  #######  ####    ###     #######

By bl4dsc4n - v.0.1

usage: 4rquiv3.py [-h] [--show_date] domain
'''

def search_wayback_machine(domain, show_date=False):
    api_url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original,timestamp"
    response = requests.get(api_url)

    if response.status_code == 200:
        results = response.text.split("\n")
        unique_urls = set()

        if len(results) > 1:
            # Crie uma lista de tuplas (timestamp, url)
            date_url_list = []
            
            for result in results[1:]:
                parts = result.split()
                if len(parts) == 2:
                    url, timestamp = parts
                    if url not in unique_urls:
                        unique_urls.add(url)
                        date_url_list.append((timestamp, url))

            # Organize a lista por data de modificação
            date_url_list.sort()

            for timestamp, url in date_url_list:
                if show_date:
                    print(f"Data de Modificação: {timestamp}")
                    if show_date:
                        print(f"URL: {url}")
                        print(f"Link para o Web Archive: http://web.archive.org/web/{timestamp}/{url}")
                        print()
                else:
                    print(url)
        else:
            print("Nenhuma captura encontrada.")
    else:
        print("Erro ao acessar a Wayback Machine.")

def main():
    parser = argparse.ArgumentParser(description="Pesquise a Wayback Machine para um domínio específico.")
    parser.add_argument("domain", nargs='?', help="O domínio para pesquisa (por exemplo, example.com)")
    parser.add_argument("--show_date", action="store_true", help="Mostrar a data de modificação e o link para o Web Archive")

    if len(sys.argv) == 1:
        print(banner)  # Imprime o banner de uso quando nenhum argumento é passado
        sys.exit(1)

    args = parser.parse_args()

    search_wayback_machine(args.domain, args.show_date)

if __name__ == "__main__":
    main()
