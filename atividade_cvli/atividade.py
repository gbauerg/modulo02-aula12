import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
  print(f'Obtendo os dados...')

  ENDERECO_DADOS = (
      'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
  )

  df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='cp1252')

  df_cvli = df_ocorrencias[['aisp', 'cvli']]

  df_cvli = df_cvli.groupby('aisp', as_index=False)['cvli'].sum()

  df_cvli = df_cvli.sort_values(by='cvli', ascending=False)
  
  df_cvli['percentual %'] = (df_cvli['cvli'] / df_cvli['cvli'].sum()) * 100

  print(df_cvli.head(10))
except Exception as e:
  print(f'Erro ao obter dados: {e}')

try:
  print(f'\nCalculando Medidas')

  array_cvli = df_cvli['cvli']

  media_cvli = np.mean(array_cvli)
  mediana_cvli = np.median(array_cvli)
  distancia_cvli = np.abs((media_cvli - mediana_cvli) / mediana_cvli * 100)

except Exception as e:
  print(f'Erro ao calcular medidas: {e}')

try:
  q1 = np.quantile(array_cvli, 0.25)
  q2 = np.quantile(array_cvli, 0.50)
  q3 = np.quantile(array_cvli, 0.75)

  iqr = q3 - q1
  lim_superior = q3 + (1.5 * iqr)
  lim_inferior = q1 - (1.5 * iqr)

  maximo = np.max(array_cvli)
  minimo = np.min(array_cvli)
  amplitude = maximo - minimo

  distancia = abs((media_cvli - mediana_cvli) / mediana_cvli * 100)
  df_cvli_menores = df_cvli[
        df_cvli["cvli"] < q1
    ]
  df_cvli_maiores = df_cvli[
        df_cvli["cvli"] > q3
    ]

except Exception as e:
  print(f'Erro ao calcular quartis: {e}')

try:
  df_cvli_outliers_maiores = df_cvli[df_cvli['cvli'] > lim_superior]

  if len(df_cvli_outliers_maiores) == 0:
    print('Não há outliers maiores.')
  else:
    print('\nAISP com Outliers Maiores:')
    print(df_cvli_outliers_maiores)

  df_cvli_outliers_menores = df_cvli[df_cvli['cvli'] < lim_inferior]

  if len(df_cvli_outliers_menores) == 0:
    print('Não há outliers menores.')
  else:
    print('\nMunicipios com Outliers Menores:')
    print(df_cvli_outliers_menores)

except Exception as e:
  print(f'Erro ao criar outliers: {e}')

try:
  # Variância é a média dos quadrados das diferenças entre cada valor e a media
  variancia = np.var(array_cvli)

  distancia_var_media = variancia / (media_cvli**2) * 100

  desvio_padrao = np.std(array_cvli)

  coef_variação = (desvio_padrao / media_cvli) * 100

except Exception as m:
  print(f'Erro ao calcular a variabilidade do conjunto {m}')

try:
  assimetria = df_cvli['cvli'].skew()
  curtose = df_cvli['cvli'].kurtosis()

except Exception as e:
    print(f"Erro ao calcular a Assimetria dos Dados")


try:
  print(f'\nMedidas:')
  print(f'Media: {media_cvli:.2f}')
  print(f'Mediana: {mediana_cvli}')
  print(f'Distância: {distancia_cvli:.2f}')
  print(f'\nQuartis:')
  print(f'IQR: {iqr}')
  print(f'Q1: {q1}')
  print(f'Q2: {q2}')
  print(f'Q3: {q3}')
  print(f'Limite Superior: {lim_superior}')
  print(f'Limite Inferior: {lim_inferior}')
  print(f'\nMáximo: {maximo}')
  print(f'Mínimo: {minimo}')
  print(f'Amplitude: {amplitude}')
  print(f'Distância da Variância Média: {distancia_var_media:.2f}')
  print(f'Coeficiente de Variação: {coef_variação:.0f}%')
  print(f'\nVariância: {variancia:.2f}')
  print(f'Desvio Padrão: {desvio_padrao:.2f}')
  print(f'Distância: {distancia:.2f}%')
  print(f"\nAssimetria: {assimetria}")
  print(f"Curtose: {curtose}")

except Exception as e:
  print(f'Erro ao expressar medidas: {e}')

try:
  print('\nInformações de Crimes Violentos')
  plt.figure(figsize=(16, 10))

  plt.subplot(2, 2, 1)
  plt.boxplot(
      df_cvli['cvli'], orientation='horizontal', showmeans=False, showfliers=False
  )
  plt.title('Distribuição dos dados (Boxplot)')
  plt.xlabel('CVLI')

  plt.subplot(2, 2, 2)
  plt.title('Resumo Estatístico', fontsize=14)
  plt.text(0.1, 0.95, f'Limite Inferior: {lim_inferior}', fontsize=12)
  plt.text(0.1, 0.90, f'Mínimo: {minimo}', fontsize=12)
  plt.text(0.1, 0.85, f'Q1: {q1}', fontsize=12)
  plt.text(0.1, 0.80, f'Q2 (Mediana): {q2}', fontsize=12)
  plt.text(0.1, 0.75, f'Q3: {q3}', fontsize=12)
  plt.text(0.1, 0.70, f'Limite Superior: {lim_superior}', fontsize=12)
  plt.text(0.1, 0.65, f'Máximo: {maximo}', fontsize=12)

  plt.text(0.5, 0.55, f'Mediana: {mediana_cvli}', fontsize=12)
  plt.text(0.5, 0.50, f'Média: {media_cvli:.2f}', fontsize=12)
  plt.text(0.5, 0.45, f'IQR Intervalo Interquartil: {iqr}', fontsize=12)
  plt.text(0.5, 0.40, f'Amplitude Total: {amplitude}', fontsize=12)
  plt.text(0.5, 0.35, f'Distância: {distancia:.2f}%', fontsize=12)

  plt.text(0.1, 0.30, f'Distância da Variância Média: {distancia_var_media:.2f}')
  plt.text(0.1, 0.25, f'Coeficiente de Variação: {coef_variação:.0f}%')
  plt.text(0.1, 0.20, f'\nVariância: {variancia:.2f}')
  plt.text(0.1, 0.15, f'Desvio Padrão: {desvio_padrao:.2f}')
  plt.text(0.1, 0.10, f'Distância: {distancia:.2f}%')
  plt.text(0.1, 0.05, f"\nAssimetria: {assimetria}")
  plt.text(0.1, 0.00, f"Curtose: {curtose}")
  plt.axis('off')

  plt.subplot(2, 2, 3)

  df_cvli_maiores_10 = (df_cvli_maiores.head(10))
  df_cvli_maiores_10["aisp"] = df_cvli_maiores_10["aisp"].astype(str)

  plt.barh(df_cvli_maiores_10['aisp'], df_cvli_maiores_10['cvli'])
  plt.title("Top 10 - AISP com mais Crimes Violentos")

  plt.subplot(2, 2, 4)

  plt.hist(array_cvli, bins=10, edgecolor="black")
  plt.axvline(media_cvli, color="green", linewidth=1)
  plt.axvline(mediana_cvli, color="orange", linewidth=1)

  contagens, limite = np.histogram(array_cvli, bins=100)
    
  print(f"\nFaixas de Crimes do Histograma")
    
  for i in range(len(contagens)):
    if contagens[i] > 0:
      print(
        f"Faixa {i+1}: "
        f"{limite[i]:.0f} até {limite[i+1]:.0f} Crimes Violentos"
        f"=> {contagens[i]} AISP"
          )

  plt.show()

except Exception as e:
  print(f'Erro ao plotar gráfico: {e}')