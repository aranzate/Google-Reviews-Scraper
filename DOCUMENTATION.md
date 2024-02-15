### Scraper de reviews do Google Maps de franquias Arcca

Para utilizar este programa, coloque o link da primeira requisição XHR listugcontent(obtida através da aba network do navegador) da loja que deseja extrair no urls.txt.

O arquivo handler.py, fica responsável em rodar a extração das reviews paralelamente através dos links fornecidos no arquivo urls.txt.

### Funções

create_table(conn, cur)
Funcionalidade: Cria uma tabela no banco de dados PostgreSQL, com uma conexão definida pelas variáveis de ambiente e com o cursor que permite que o python execute comandos SQL.

get_response_data(url)
Funcionalidade: Retorna os dados da requisição GET pro endereço fornecido pela Google, com as informações contidas no listugcontent.


get_next_request(response_data)
Funcionalidade: Recupera do arquivo a parte relevante para carregar as próximas reviews.
Regex: r'(\w+)(\\u003d\\u003d|\\u003d)\"\]\]\]'
Exemplo: "CAESBkVnSUlDZw\u003d\u003d]]]" 



change_request(response_data, url)
Funcionalidade: Realiza a mudança de página com a informação da função get_next_request, e também recupera os dados extraidos na listugcontent com a função get_response_data



get_place_name(response_data)
Funcionalidade: Extrai o nome da loja.
Regex: r'[^"]*","pt"\]\],\[|[^"]*","en"\]\],\['
Exemplo: "Nema Padaria - Leblon | Padaria de Fermentação Natural","pt"]],[



get_names(response_data)
Funcionalidade: Extrai o nome do cliente que publicou a review.
Regex: r'br100","[^"]+","https'
Exemplo: br100","LU NOREPLAY","https



get_profiles(response_data)
Funcionalidade: Extrai o perfil do cliente que publicou a review.
Regex: r'https://www\.google\.com/maps/contrib/[0-9]+/reviews\?hl\\u003dpt-BR|https://www\.google\.com/maps/contrib/[0-9]+/reviews\?hl\\u003den'
Exemplo: https://www.google.com/maps/contrib/106166884279831670785?hl\u003den



get_ratings(response_data)
Funcionalidade: Extrai a quantidade de estrelas que o cliente deu em sua review.
Regex: r'\[\[[1-5]\]\]\,\[n|\[\[[1-5]\]\,n|\[\[[1-5]\]\,\[\"|\[\[[1-5]\]\]\,\[\[\"'
Exemplo: [[5],["


get_reviews(response_data)
Funcionalidade: Extrai o texto/review publicada pelo cliente.
Regex: r'\[\[[1-5]\],\[".*?"|\[\[[1-5]\]\],\[null|\[\[[1-5]\],null|\[\[[1-5]\]\]\,\[\[\"'
Exemplo: [[5],["Sempre com ótimas opções deliciosas. Sempre compro o pão de queijo congelado, o pão de fermentação natural (que eles entregam fatiado) e algum bolo. Tudo Sempre muito bom!"



scrap_data(response_data, place_name, url)
Funcionalidade: Função principal do scraper, utliza as funções anteriores para extrair todos os dados definidos e armazená-los no banco de dados.




### Bibliotecas necessárias para o funcionamento

- urllib3: Utilizada para fazer requisições HTTP. No caso deste scraper, se faz requisições GET para as respostas XHR das requisições do Google Maps, que contém os dados das reviews dos clientes das lojas.
- re: Utilizada para fazer o regex(Expressão Regular) e extrar do arquivo de texto da resposta XHR parte necessária (e.g. nome do cliente)
- psycopg2-binary: Utilizada para fazer o código em Python se comunicar com um banco de dados em PostgreSQL, podendo inclusive realizar consultas SQL durante a execução.
- dotenv: Utilizada para carregar as variáveis de ambiente para a conexão com o banco de dados.
- os: Utilizada em conjunto com o dotenv.
- time (Opcional): Usado para cronometrar o tempo de execução do programa.

Através das seguintes configurações do serverles.yml, é possível instalar todas as dependências necessárias presentes no arquivo requirements.txt (é necessário rodar com o Docker aberto para dockerizar as biliotecas)
"""
plugins:
  - serverless-python-requirements
  
custom:
    pythonRequirements:
        dockerizePip: non-linux
"""




