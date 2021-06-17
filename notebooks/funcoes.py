import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from pandas.plotting import autocorrelation_plot
import warnings
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from sklearn.metrics import mean_absolute_error
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics

def processamento_dados():
  #lendo csv e atribuindo a um dataframe (formato do dataset do pandas)
  df_casos_full = pd.read_csv('https://github.com/aureliowozhiak/facebook_prophet_covid19/raw/main/datasets/caso_full.csv.gz') 

  #removendo linhas com valores Null ou NaN do dataframe
  df_casos_full = df_casos_full.dropna()

  #formatando dados de data
  df_casos_full['date'] = pd.to_datetime(df_casos_full['date'],format='%Y-%m-%d')

  #reduzindo dataframe para colunas especificas
  df_casos_full_reduced = df_casos_full[['city', 'state', 'date', 'estimated_population', 'new_confirmed', 'last_available_confirmed', 'new_deaths', 'last_available_deaths']]

  #isolando um dataframe com casos do estado do Paraná
  df_casos_parana = df_casos_full_reduced.query('state == "PR"')

  #pegando apenas as cidades referentes a região metropolitana de Curitiba
  df_casos_rmc =  df_casos_parana.query('city == "Curitiba" or city == "Adrianópolis" or city == "Agudos do Sul" or city == "Almirante Tamandaré" or city == "Araucária" or city == "Balsa Nova" or city == "Bocaiúva do Sul" or city == "Campina Grande do Sul" or city == "Campo do Tenente" or city == "Campo Largo" or city == "Campo Magro" or city == "Cerro Azul" or city == "Colombo" or city == "Contenda" or city == "Doutor city == Ulysses" or city == "Fazenda Rio Grande" or city == "Itaperuçu" or city == "Lapa" or city == "Manditiruba" or city == "Piên" or city == "Pinhais" or city == "Piraquara" or city == "Quatro Barras" or city == "Quitandinha" or city == "Rio Branco do Sul" or city == "Rio Negro" or city == "São José dos Pinhais" or city == "Tijucas do Sul" or city == "Tunas do Paraná"')
  df_casos_cwb =  df_casos_rmc.query('city == "Curitiba"')

  #encontrando top cidades da região metropolitana de curitiba
  rmc_top_cities = df_casos_rmc[['city', 'last_available_deaths', 'date']].query('date == "2021-06-15 00:00:00"').sort_values(by='last_available_deaths', ascending=False)[:3]['city'].to_list()
  df_rmc_top_cities = df_casos_rmc.query('city == @rmc_top_cities')

  return df_casos_full, df_casos_full_reduced, df_casos_parana, df_casos_rmc, df_casos_cwb, rmc_top_cities, df_rmc_top_cities

df_casos_full, df_casos_full_reduced, df_casos_parana, df_casos_rmc, df_casos_cwb, rmc_top_cities, df_rmc_top_cities = processamento_dados()

#função padrão para gerar gráficos de linha
def grafico_linha(titulo = 'Total de mortes por COVID-19',
                  subtitle = 'nas 3 cidades com mais casos no Paraná',
                  titulo_legenda = 'Cidades',
                  y_label = 'Acumulado total',
                  x_label = 'Meses/Ano',
                  df = df_rmc_top_cities,
                  df_x = 'date',
                  df_y = 'last_available_deaths',
                  hue = 'city',
                  palette_color = 'autumn'):

  ax = sns.lineplot(data=df, x=df_x, y=df_y, hue=hue, palette=palette_color)
  plt.legend(title=titulo_legenda)
  plt.ylim(0)
  ax.set_title(subtitle,fontsize=16)
  plt.suptitle(titulo,fontsize=24)
  ax.set_ylabel(y_label)
  ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
  ax.set_xlabel(x_label)
  
  def teste():
    print('testeee')
