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
