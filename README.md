# Desafio ABI Academy Hack

Este projeto é referente ao desafio da ABI Academy Hack promovida pela Ambev

## Projeto

Desenvolver um sistema de recomendação para vendas cruzadas

### Proposta

Criar um sistema de recomendação baseada em caracteristicas dos produtos e explorar a possibilidade de um sistema de recomendação hibrido, que leva em consideração as caracteristicas dos produtos (similaridade entre produtos) e caracteristicas do comprador (similaridade comportamental do comprador).

### Análise

A análise foi baseada no dataset oferecido pela Ambev, no entanto o dataset não está disponivel neste repositório, apenas as informações pertinentes à analise exploratória e modelos gerados.

#### Distribuiçao dos arquivos de análise 

* 00-Ideação
* 01-Análise Exploratória
* 02-Scrap
* 03-Enriquecimento
* 04-Agregação do Dataset
* 05-Comportamento do Atacadista
* 06-Modelagem Produto
* 07-Recomendação de Produto Atacadista (breffing)

### API

Foi disponibilizada uma simples API que consome o modelo gerado e retorna as recomendações com base nas caracteristicas observadas durante as análises. 


#### Subindo o projeto

Para executar o projeto é necessário ter o ambiente configurado com Docker e rodar o seguinte comando no diretório `Desafio/api`
```
docker build -t api-recomendacao .
docker run -d --name api-recomendacao -p 5000:5000 api-recomendacao
```

Para executar a request basta fazer uma requisição no seguinte endereço

HTTP POST http://127.0.0.1:5000/api/recomendacao?top=3

payload: 
```json
{
    "TamanhoContainer": 0.55,
    "PercentualAlcoolico": 9.50,
    "Variedade": "Blonde",
    "Descricao": "",
    "Segmento": "SUPER PREMIUM",
    "Harmonizacao": "Arroz, Peixe, Salgados",
    "Ingredientes":"Trigo, Agua, Cevada",
    "Alergico": "Glutten",
    "Temperatura": "0-5",
    "Ibu": 25
}
```

Os dados do payload acima são meramente ilustrativos.

Exemplo do response:
```json
{
    "message": "ok",
    "predict": [
        {
            "Id": 62706,
            "Submarca": NaN,
            "Litros": 0.0,
            "Segmento": NaN,
            "PercentualAlcoolico": 6.600000000000001
        },
        {
            "Id": 62707,
            "Submarca": NaN,
            "Litros": 0.0,
            "Segmento": NaN,
            "PercentualAlcoolico": 6.600000000000001
        },
        {
            "Id": 58277,
            "Submarca": "LEFFE BLONDE",
            "Litros": 0.25,
            "Segmento": "PREMIUM",
            "PercentualAlcoolico": 0.0
        }
    ]
}
```