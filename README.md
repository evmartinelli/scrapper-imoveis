# Scraper Imóveis Caixa

Este projeto é um scraper para o site de imóveis da Caixa Econômica Federal. Ele permite buscar e listar informações detalhadas sobre imóveis disponíveis para leilão, incluindo valores, datas de leilão, endereço, e outras informações relevantes.

Estrutura do Projeto


```
scrapper-imoveis/

├── .gitignore
├── [requirements.txt](http://_vscodecontentref_/0)
├── .vscode/
│   └── [launch.json](http://_vscodecontentref_/1)
├── app/
│   ├── [__init__.py](http://_vscodecontentref_/2)
│   ├── [main.py](http://_vscodecontentref_/3)
│   ├── api/
│   │   └── v1/
│   │       └── [endpoints.py](http://_vscodecontentref_/4)
│   ├── models/
│   │   └── [imovel.py](http://_vscodecontentref_/5)
│   ├── services/
│   │   └── [scraper.py](http://_vscodecontentref_/6)
│   └── utils/
│       └── [parser.py](http://_vscodecontentref_/7)
├── tests/
│   └── [test_scraper.py](http://_vscodecontentref_/8)
```

### Principais Componentes

app/main.py: Configura a aplicação FastAPI e registra as rotas.

app/api/v1/endpoints.py: Define os endpoints da API para listar imóveis.

app/models/imovel.py: Modelo Pydantic que representa os dados de um imóvel.

app/services/scraper.py: Contém a lógica para buscar e parsear os dados do site da Caixa.

app/utils/parser.py: Funções auxiliares para parsear o HTML retornado pelo site.

### Requisitos
Certifique-se de ter o Python 3.10+ instalado. As dependências do projeto estão listadas no arquivo requirements.txt.

### Instalação
Clone o repositório: ```bash git clone https://github.com/seu-usuario/scrapper-imoveis.git cd scrapper-imoveis ```

Crie um ambiente virtual e ative-o: ```bash python -m venv venv source venv/bin/activate # Linux/Mac venv\Scripts\activate # Windows ```

Instale as dependências: ```bash pip install -r requirements.txt ```

### Execução
Inicie o servidor FastAPI com o Uvicorn: ```bash uvicorn app.main:app --reload ```

Acesse a documentação interativa da API em: ``` http://127.0.0.1:8000/docs ```

### Endpoints
GET /v1/imoveis: Lista imóveis disponíveis para leilão.
Parâmetros:
estado (opcional): UF do estado (exemplo: SP).
cidade_id (opcional): Código da cidade (exemplo: 9205 para Campinas).
Testes
Os testes estão localizados na pasta tests/. Para executá-los, use o comando:

```bash pytest ```

### Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

### Licença
Este projeto está licenciado sob a MIT License.
