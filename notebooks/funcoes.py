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