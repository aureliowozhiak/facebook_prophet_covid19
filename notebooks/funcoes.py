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

#função para processamento de dados
def processamento_dados():
  #lendo csv e atribuindo a um dataframe (formato do dataset do pandas)
  df_casos_full = pd.read_csv('https://github.com/aureliowozhiak/facebook_prophet_covid19/raw/main/datasets/caso_full.csv.gz') 

  #removendo linhas com valores Null ou NaN do dataframe
  df_casos_full = df_casos_full.dropna()

  #formatando dados de data
  df_casos_full['date'] = pd.to_datetime(df_casos_full['date'],format='%Y-%m-%d')

  #reduzindo dataframe para colunas especificas
  df_casos_full_reduced = df_casos_full[['city', 'state', 'date', 'estimated_population', 'new_confirmed', 'last_available_confirmed', 'new_deaths', 'last_available_deaths']]

  #criando média móvel
  df_casos_full_reduced['moving_average_confirmed'] = df_casos_full_reduced['last_available_confirmed'].rolling(window=7, center=False).mean()
  df_casos_full_reduced['moving_average_deaths'] = df_casos_full_reduced['last_available_deaths'].rolling(window=7, center=False).mean()

  df_casos_full_reduced['moving_average_new_confirmed'] = df_casos_full_reduced['new_confirmed'].rolling(window=7, center=False).mean()
  df_casos_full_reduced['moving_average_new_deaths'] = df_casos_full_reduced['new_deaths'].rolling(window=7, center=False).mean()

  #isolando um dataframe com casos dos estados do sul
  df_casos_sul = df_casos_full_reduced.query('state == "PR" or state == "SC" or state == "RS"')

  #isolando um dataframe com casos do estado do Paraná
  df_casos_parana = df_casos_full_reduced.query('state == "PR"')

  #pegando apenas as cidades referentes a região metropolitana de Curitiba
  df_casos_rmc =  df_casos_parana.query('city == "Curitiba" or city == "Adrianópolis" or city == "Agudos do Sul" or city == "Almirante Tamandaré" or city == "Araucária" or city == "Balsa Nova" or city == "Bocaiúva do Sul" or city == "Campina Grande do Sul" or city == "Campo do Tenente" or city == "Campo Largo" or city == "Campo Magro" or city == "Cerro Azul" or city == "Colombo" or city == "Contenda" or city == "Doutor city == Ulysses" or city == "Fazenda Rio Grande" or city == "Itaperuçu" or city == "Lapa" or city == "Manditiruba" or city == "Piên" or city == "Pinhais" or city == "Piraquara" or city == "Quatro Barras" or city == "Quitandinha" or city == "Rio Branco do Sul" or city == "Rio Negro" or city == "São José dos Pinhais" or city == "Tijucas do Sul" or city == "Tunas do Paraná"')
  df_casos_cwb =  df_casos_rmc.query('city == "Curitiba"')

  #encontrando top cidades da região metropolitana de curitiba
  rmc_top_cities = df_casos_rmc[['city', 'last_available_deaths', 'date']].query('date == "2021-06-15 00:00:00"').sort_values(by='last_available_deaths', ascending=False)[:3]['city'].to_list()
  df_rmc_top_cities = df_casos_rmc.query('city == @rmc_top_cities')

  return df_casos_full, df_casos_full_reduced, df_casos_sul, df_casos_parana, df_casos_rmc, df_casos_cwb, rmc_top_cities, df_rmc_top_cities

df_casos_full, df_casos_full_reduced, df_casos_sul, df_casos_parana, df_casos_rmc, df_casos_cwb, rmc_top_cities, df_rmc_top_cities = processamento_dados()



#função padrão para gerar gráficos de linha
def grafico_linha(titulo = 'Total de mortes por COVID-19',
                  subtitle = 'por data de registro nas 3 cidades com maior número de casos no Paraná',
                  titulo_legenda = 'Cidades',
                  y_label = 'Acumulado total',
                  x_label = 'Meses/Ano',
                  df = df_rmc_top_cities,
                  df_x = 'date',
                  df_y = 'last_available_deaths',
                  hue = 'city',
                  palette_color = 'autumn'):


  #parametros para padronizar gráficos
  mpl.rcParams['font.size'] = 18
  mpl.rcParams['figure.figsize'] = (15,8)

  ax = sns.lineplot(data=df, x=df_x, y=df_y, hue=hue, palette=palette_color)
  plt.legend(title=titulo_legenda)
  plt.ylim(0)
  ax.set_title(subtitle,fontsize=16)
  plt.suptitle(titulo,fontsize=24)
  ax.set_ylabel(y_label)
  ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
  ax.set_xlabel(x_label)


  #funções para forecasting:

def return_modelo_previsao(dataframe = df_casos_cwb, ds = 'date', y = 'last_available_deaths', dados_treino = 400, periodo_previsao = 100, n_changepoints_ = 30, changepoint_prior_scale_ = 1.0, changepoint_range_ = 0.83):
  df = pd.DataFrame()
  df_teste = pd.DataFrame()

  df['ds'] = dataframe[ds][:dados_treino]
  df['y'] = dataframe[y][:dados_treino]

  df_teste['ds'] = dataframe[ds][dados_treino:(dados_treino+periodo_previsao)]
  df_teste['y'] = dataframe[y][dados_treino:(dados_treino+periodo_previsao)]

  modelo = Prophet(n_changepoints = n_changepoints_, changepoint_prior_scale = changepoint_prior_scale_, changepoint_range = changepoint_range_, yearly_seasonality=False, daily_seasonality=False);

  modelo.fit(df);

  previsao = modelo.predict(modelo.make_future_dataframe(periods=periodo_previsao));

  return modelo, previsao, df_teste


def treinar_e_plotar(ds_eixo = 'date', y_eixo = 'last_available_deaths', label_y = 'Acumulado total de mortes', titulo = 'Previsão de mortes totais por COVID-19', n_changepoints_ = 30, changepoint_prior_scale_ = 1.0, changepoint_range_ = 0.89):

  modelo, previsao, df_teste = return_modelo_previsao(dataframe = df_casos_cwb, ds = ds_eixo, y = y_eixo, n_changepoints_= n_changepoints_, changepoint_prior_scale_ = changepoint_prior_scale_, changepoint_range_ = changepoint_range_);

  ax = modelo.plot(previsao,xlabel = 'Mês/Ano', ylabel=label_y, figsize=(15,8));

  plt.title(titulo);
  plt.plot(df_teste['ds'], df_teste['y'],'--r', label='Daddos de teste');

  plt.gca().legend(('Dados de treino','Previsão do modelo', 'Dados comparativos para treino'))


def treinar_e_plotar_changepoints(ds_eixo = 'date', y_eixo = 'last_available_deaths', label_y = 'Acumulado total', titulo = 'Previsão de mortes totais por COVID-19', n_changepoints_ = 30, changepoint_prior_scale_ = 1.0, changepoint_range_ = 0.89):

  modelo, previsao, df_teste = return_modelo_previsao(dataframe = df_casos_cwb, ds = ds_eixo, y = y_eixo, n_changepoints_= n_changepoints_, changepoint_prior_scale_ = changepoint_prior_scale_, changepoint_range_ = changepoint_range_);

  ax = modelo.plot(previsao,xlabel = 'Mês/Ano', ylabel=label_y, figsize=(15,8));

  plt.title(titulo);
  plt.plot(df_teste['ds'], df_teste['y'],'--r', label='Daddos de teste');

  plt.gca().legend(('Dados de treino','Previsão do modelo', 'Dados comparativos para treino'))

  add_changepoints_to_plot(ax.gca(), modelo, previsao);

