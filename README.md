<a href="https://www.linkedin.com/in/aureliowozhiak/">![](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)</a>
<a href="https://github.com/aureliowozhiak">![](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)</a>

<p align="center"><img src="images/prophet_logo.png" /></p>

# Facebook Prophet e os casos de COVID-19

## Análisando a série temporal dos casos de Corona Virus no Brasil e criando previsões<sup>*</sup> com o Facebook Prophet

---
## Visão geral do projeto:

 - Objetivo do projeto
 - Introdução
     - O Brasil em dados libertos
     - A pandêmia do COVID-19
     - O que é o Facebook Prophet?
 - Origem dos dados e informações técnicas
 - Importação de bibliotecas
 - Carregamento e Processamento dos dados
 - Análisando a série temporal dos casos de COVID-19 em Curitiba-PR
 - Criando o modelo de previsão
 - Plotando as previsões com o Prophet<sup>*</sup>
 - Pesquisa complementar
 - Conclusão
 - Referências

 
  <a href="https://nbviewer.jupyter.org/github/aureliowozhiak/facebook_prophet_covid19/blob/main/notebooks/Facebook_Prophet_e_os_casos_de_COVID_19.ipynb">![](https://img.shields.io/badge/open_in_nbviewer-02569B?style=for-the-badge&logo=open&logoColor=white)<a/><br/> 
 
 <a href="https://colab.research.google.com/github/aureliowozhiak/facebook_prophet_covid19/blob/main/notebooks/Facebook_Prophet_e_os_casos_de_COVID_19.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

<sub><sup> *As previsões criadas aqui pelo Prophet não são exatas pois não mostram de fato o cenário futuro do corona virus, pois os dados utilizados apenas nos dão uma visão, com base no que aconteceu no passado, para termos uma noção de qual poderia ser a tendência de crescimento dos casos, porém, como os dados não exprimem o cenário completo e não leva em conta campanhas futuras de vacinação, que já estão acontecendo, não devemos levar essas conclusões como se fossem verdades absolutas.</sup></sub>
---
### 🎯 Objetivo do projeto

A ideia aqui é efetuar algumas analises nos dados referentes ao casos de COVID-19 desde seu primeiro caso aqui no Brasil até o momento e tentar efetuar algumas previsões* utilizando uma ferramenta de open source para forecasting(previsão) do Facebook, o Prophet!

---
### ⭐ Introdução

#### - O Brasil.io

O [brasil.io](https://brasil.io/home/) surgiu com o objetivo de disponibilizar dados públicos de forma mais acessível para qualquer pessoa conseguir acessar e fazer uso desses dados.

<p align="center"><img src="https://raw.githubusercontent.com/aureliowozhiak/facebook_prophet_covid19/main/images/brasil.io.png" /></p>

>Após a criação da Lei de Acesso à Informação, todas as informações produzidas ou custodiadas pelo poder público são públicas e portanto, disponíveis a todos os cidadãos, exceto aquelas que são sigilosas por lei. Contudo, mesmo que a informação esteja disponível não significa que ela está em um formato acessível 

<sub>adaptado: https://brasil.io/manifesto/ - acesso em: 16/06/2021 </sub>

#### - A pandêmia do COVID-19

<p align="center"><img src="https://raw.githubusercontent.com/aureliowozhiak/facebook_prophet_covid19/main/images/SARS-CoV-2_without_background.png" /></p>

>A pandemia de COVID-19, também conhecida como pandemia de coronavírus, é uma pandemia em curso de COVID-19, uma doença respiratória causada pelo coronavírus da síndrome respiratória aguda grave 2 (SARS-CoV-2). O vírus tem origem zoonótica e o primeiro caso conhecido da doença remonta a dezembro de 2019 em Wuhan, na China. Em 20 de janeiro de 2020, a Organização Mundial da Saúde (OMS) classificou o surto como Emergência de Saúde Pública de Âmbito Internacional e, em 11 de março de 2020, como pandemia. Em 16 de junho de 2021, 176 568 410 casos foram confirmados em 192 países e territórios, com 3 819 480 mortes atribuídas à doença, tornando-se uma das pandemias mais mortais da história.

<sub>adaptado: https://pt.wikipedia.org/wiki/Pandemia_de_COVID-19 - acesso em: 16/06/2021 </sub>

#### O que é o Facebook Prophet?

Em fevereiro de 2017 o Facebook Research lançou a ferramenta open source chamada [Facebook Prophet](https://facebook.github.io/prophet/) para previsão de séries temporais, ou seja, esse algortimo "profeta" do Facebook tem por objetivo principal prever uma tendência no comportamento dos dados com apenas poucos meses de histórico.<br/>
Como essa ferramenta, também é possível entender sazonalidades que impactam a série temporal e análisar mudanças bruscas de tendência e outliers

Essa ferramenta está [disponível no GitHub](https://github.com/facebook/prophet) para ser utilizada com Python ou R.

---
#### 📝 Origem dos dados e informações técnicas

Os dados utilizados foram baixados do [brasil.io](https://brasil.io/home) > [COVID-19](https://brasil.io/covid19/) > [Dados completos](https://brasil.io/dataset/covid19/caso_full/)<br />
<sub>link direto para download: [https://data.brasil.io/dataset/covid19/caso_full.csv.gz](https://data.brasil.io/dataset/covid19/caso_full.csv.gz)</sub><br/><br/>



Após acessar e efetuar o download do dataset completo, efetuei uma cópia e salvei no repositório do GitHub em "datasets/caso_full.csv.gz"<br/>
<sub>cópia salva no repositório dia: 16/06/2021: [https://github.com/aureliowozhiak/facebook_prophet_covid19/blob/main/datasets/caso_full.csv.gz](https://github.com/aureliowozhiak/facebook_prophet_covid19/blob/main/datasets/caso_full.csv.gz) </sub>


O dataset original contém várias colunas com os valores: 

> 'city', 'city_ibge_code', 'date', 'epidemiological_week', 'estimated_population', 'estimated_population_2019', 'is_last', 'is_repeated', 'last_available_confirmed', 'last_available_confirmed_per_100k_inhabitants', 'last_available_date', 'last_available_death_rate', 'last_available_deaths', 'order_for_place', 'place_type', 'state', 'new_confirmed', 'new_deaths'

Porém, aqui vamos utilizar apenas os seguintes:

- **city**: nome da cidade
- **state**: nome do estado
- **date**: data do registro
- **estimated_population**: população estimada da cidade
- **new_confirmed**: novos casos confirmados
- **last_available_confirmed**: total acumulado de casos confirmados até a data
- **new_deaths**: novas mortes confirmadas
- **last_available_deaths**: total acumulado de mortes confirmadas até a data

---

#### 👨‍💻 Carregamento e Processamento dos dados

Todo carregamento, processamento e organização dos dados foram feitos no arquivo [funcoes.py](https://github.com/aureliowozhiak/facebook_prophet_covid19/blob/main/notebooks/funcoes.py) 
