#Bibliotecas utilizadas 
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from tkinter import messagebox


# Tratamento dos arquivo CSV - transformando o arquivo em "dataframe"
current_directory = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo_origem = os.path.join(current_directory, 'OK_Anexo_Arquivo_Dados_Projeto.csv')
dataframe = pd.read_csv(caminho_arquivo_origem)

# Leitura do arquivo CVS no terminal
print(dataframe)

def normalizar_dados_csv(caminho_arquivo_origem):
    # Carregar os dados climáticos do arquivo
    dataframe = pd.read_csv(caminho_arquivo_origem, delimiter=';')

    for coluna in dataframe.columns:
        if dataframe[coluna].dtype == 'O':
            dataframe[coluna] = pd.to_datetime(dataframe[coluna], format='%d/%m/%Y')
        else:
            dataframe[coluna] = dataframe[coluna].apply(lambda x: float(x) if isinstance(x, str) else x)

    # Filtrar os dados inválidos (precipitação negativa)
    dataframe = dataframe[dataframe['precip'] >= 0]

    return dataframe


def ler_arquivo_csv(caminho_arquivo):
    # Ler o arquivo CSV utilizando pandas
    dataframe = pd.read_csv(caminho_arquivo, delimiter=';')

    return dataframe


def filtrar_dados(dataframe):
    # Filtrar os dados inválidos (precipitação negativa)
    dataframe_filtrado = dataframe[dataframe['precip'] >= 0]

    return dataframe_filtrado


def filtrar_dados_por_data(dataframe, start_month, start_year, end_month, end_year):
    dataframe['data'] = pd.to_datetime(dataframe['data'], format='%d/%m/%Y')
    
    start_date = pd.to_datetime(f"{start_year}-{start_month}-01")
    end_date = pd.to_datetime(f"{end_year}-{end_month}-01") + pd.offsets.MonthEnd(1)

    dataframe_selecionado = dataframe[(dataframe['data'] >= start_date) & (dataframe['data'] <= end_date)]

    return dataframe_selecionado


def open_select_dates_window():
    select_dates_window = tk.Toplevel(window)
    select_dates_window.title("Selecionar Datas")
    select_dates_window.geometry("300x250")

    start_month_label = tk.Label(select_dates_window, text="Mês de início (01 a 12):")
    start_month_label.pack()
    start_month_entry = tk.Entry(select_dates_window)
    start_month_entry.pack()

    start_year_label = tk.Label(select_dates_window, text="Ano de início (1961 a 2016):")
    start_year_label.pack()
    start_year_entry = tk.Entry(select_dates_window)
    start_year_entry.pack()

    end_month_label = tk.Label(select_dates_window, text="Mês de término (01 a 12):")
    end_month_label.pack()
    end_month_entry = tk.Entry(select_dates_window)
    end_month_entry.pack()

    end_year_label = tk.Label(select_dates_window, text="Ano de término (1961 a 2016):")
    end_year_label.pack()
    end_year_entry = tk.Entry(select_dates_window)
    end_year_entry.pack()

    show_data_button = tk.Button(select_dates_window, text="Mostrar dados", command=lambda: show_data(start_month_entry.get(), start_year_entry.get(), end_month_entry.get(), end_year_entry.get()))
    show_data_button.pack()
    
    back_button = tk.Button(select_dates_window, text="Voltar", command=select_dates_window.destroy)
    back_button.pack()
    
def validate_date_range(start_month, start_year, end_month, end_year):
    # Validar se os valores estão dentro do intervalo permitido
    start_month = int(start_month)
    start_year = int(start_year)
    end_month = int(end_month)
    end_year = int(end_year)

    if not (1 <= start_month <= 12) or not (1 <= end_month <= 12):
        return False

    if not (1961 <= start_year <= 2016) or not (1961 <= end_year <= 2016):
        return False

    return True

def show_data(start_month, start_year, end_month, end_year):
    
    # Validar os valores inseridos pelo usuário
    if not validate_date_range(start_month, start_year, end_month, end_year):
        tk.messagebox.showerror("Erro", "Intervalo de datas inválido. Verifique os valores inseridos.")
        return
    # Ler o arquivo CSV e preparar os dados
    dataframe = ler_arquivo_csv(caminho_arquivo_origem)
    dataframe_filtrado = filtrar_dados(dataframe)

    # Filtrar os dados com base nas datas selecionadas pelo usuário
    dataframe_selecionado = filtrar_dados_por_data(dataframe_filtrado, start_month, start_year, end_month, end_year)

    # Exibir as médias separadamente para cada variável em uma nova janela
    result_window = tk.Toplevel(window)
    result_window.title("Resultados")
    result_window.geometry("300x300")

    # Botões para exibir médias para cada variável
    precip_button = tk.Button(result_window, text="Precipitação", command=lambda: exibir_medias(dataframe_selecionado, 'precip'))
    precip_button.pack()

    maxima_button = tk.Button(result_window, text="Máxima", command=lambda: exibir_medias(dataframe_selecionado, 'maxima'))
    maxima_button.pack()

    minima_button = tk.Button(result_window, text="Mínima", command=lambda: exibir_medias(dataframe_selecionado, 'minima'))
    minima_button.pack()

    horas_insol_button = tk.Button(result_window, text="Horas de Insolação", command=lambda: exibir_medias(dataframe_selecionado, 'horas_insol'))
    horas_insol_button.pack()

    temp_media_button = tk.Button(result_window, text="Temperatura Média", command=lambda: exibir_medias(dataframe_selecionado, 'temp_media'))
    temp_media_button.pack()

    um_relativa_button = tk.Button(result_window, text="Umidade Relativa", command=lambda: exibir_medias(dataframe_selecionado, 'um_relativa'))
    um_relativa_button.pack()

    vel_vento_button = tk.Button(result_window, text="Velocidade do Vento", command=lambda: exibir_medias(dataframe_selecionado, 'vel_vento'))
    vel_vento_button.pack()
    
    back_button = tk.Button(result_window, text="Voltar", command=result_window.destroy)
    back_button.pack()


def exibir_medias(dataframe, variable):
    medias_mensais = calcular_medias_mensais(dataframe, variable)
    media_anual = dataframe[variable].mean()
    media_total = medias_mensais[variable].mean()

    # Exibir as médias em uma nova janela
    medias_window = tk.Toplevel(window)
    medias_window.title("Médias")
    medias_window.geometry("300x450")

    medias_label = tk.Label(medias_window, text="Médias Mensais:")
    medias_label.pack()

    medias_text = tk.Text(medias_window)
    medias_text.pack()

    medias_text.insert(tk.END, str(medias_mensais))

    media_anual_label = tk.Label(medias_window, text=f"Média Anual: {media_anual:.2f}")
    media_anual_label.pack()

    media_total_label = tk.Label(medias_window, text=f"Média Total: {media_total:.2f}")
    media_total_label.pack()
    
    back_button = tk.Button(medias_window, text="Voltar", command=medias_window.destroy)
    back_button.pack()


def calcular_medias_mensais(dataframe, variable):
    dataframe['data'] = pd.to_datetime(dataframe['data'], format='%d/%m/%Y')
    dataframe['ano_mes'] = dataframe['data'].dt.strftime('%Y-%m')
    medias_mensais = dataframe.groupby('ano_mes')[variable].mean().reset_index()
    medias_mensais['ano_mes'] = pd.to_datetime(medias_mensais['ano_mes']).dt.strftime('%B de %Y')
    return medias_mensais


def mes_mais_chuvoso():
    
    # Ler o arquivo CSV e preparar os dados
    dataframe = ler_arquivo_csv(caminho_arquivo_origem)
    dataframe['data'] = pd.to_datetime(dataframe['data'], format="%d/%m/%Y")  # Converter a coluna 'data' para o tipo Timestamp
    dataframe_filtrado = filtrar_dados(dataframe)

    # Encontrar o mês mais chuvoso
    mes_chuvoso = dataframe_filtrado.loc[dataframe_filtrado['precip'].idxmax(), 'data'].strftime('%B de %Y')

    # Exibir o resultado em uma nova janela
    result_window = tk.Toplevel(window)
    result_window.title("Mês Mais Chuvoso")
    result_window.geometry("200x100")

    result_label = tk.Label(result_window, text=f"Mês mais chuvoso: {mes_chuvoso}")
    result_label.pack()
    
    back_button = tk.Button(result_window, text="Voltar", command=result_window.destroy)
    back_button.pack()


def media_temperatura_ultimos_11_anos():
    
    # Ler o arquivo CSV e preparar os dados
    dataframe = ler_arquivo_csv(caminho_arquivo_origem)
    dataframe['data'] = pd.to_datetime(dataframe['data'], format="%d/%m/%Y")  # Converter a coluna 'data' para o tipo Timestamp
    dataframe_filtrado = filtrar_dados(dataframe)

    # Filtrar os dados dos últimos 11 anos (2006 a 2016)
    start_date = pd.to_datetime("2006-01-01")
    end_date = pd.to_datetime("2016-12-31")
    dataframe_selecionado = dataframe_filtrado[(dataframe_filtrado['data'] >= start_date) & (dataframe_filtrado['data'] <= end_date)]

    # Calcular a média da temperatura mínima e máxima do determinado período
    average_temperature_minima = dataframe_selecionado['minima'].mean()
    average_temperature_maxima = dataframe_selecionado['maxima'].mean()

    # Exibir o resultado em uma nova janela
    average_window = tk.Toplevel(window)
    average_window.title("Média da Temperatura Mínima e Máxima")
    average_window.geometry("200x150")

    minima_label = tk.Label(average_window, text=f"Média Temperatura Mínima: {average_temperature_minima:.2f}")
    minima_label.pack()

    maxima_label = tk.Label(average_window, text=f"Média Temperatura Máxima: {average_temperature_maxima:.2f}")
    maxima_label.pack()


def generate_bar_chart():
    # Normalizar os dados do arquivo CSV e filtrar os dados inválidos
    dataframe_filtrado = normalizar_dados_csv(caminho_arquivo_origem)

    # Extrair o ano da coluna 'data'
    dataframe_filtrado['ano'] = dataframe_filtrado['data'].dt.year

    # Calcular as temperaturas máximas e mínimas anuais
    temperatura_maxima = dataframe_filtrado.groupby('ano')['temperatura'].max()
    temperatura_minima = dataframe_filtrado.groupby('ano')['temperatura'].min()

    # Gerar gráfico de barras das temperaturas máximas e mínimas anuais
    plt.bar(temperatura_maxima.index, temperatura_maxima, label='Temperatura Máxima')
    plt.bar(temperatura_minima.index, temperatura_minima, label='Temperatura Mínima')

    plt.xlabel('Ano')
    plt.ylabel('Temperatura')
    plt.title('Temperaturas Máximas e Mínimas Anuais')
    plt.legend()
    plt.show()

    back_button = tk.Button(chart_window, text="Voltar", command=chart_window.destroy)
    back_button.pack()


def calculate_average_temperature():
   
    # Normalizar os dados do arquivo CSV e filtrar os dados inválidos
    dataframe_filtrado = normalizar_dados_csv(caminho_arquivo_origem)

    # Calcular a média da temperatura mínima e máxima geral
    average_temperature_min = dataframe_filtrado['minima'].mean()
    average_temperature_max = dataframe_filtrado['maxima'].mean()

    average_window = tk.Toplevel(window)
    average_window.title("Média de Temperaturas Minimas e Máximas dos ultimos 11 anos")
    average_window.geometry("225x100")

    min_label = tk.Label(average_window, text=f"Média de temperatura mínima: {average_temperature_min:.2f}")
    min_label.pack()

    max_label = tk.Label(average_window, text=f"Média de temperatura máxima: {average_temperature_max:.2f}")
    max_label.pack()
    
    back_button = tk.Button(average_window, text="Voltar", command=average_window.destroy)
    back_button.pack()


def quit_program():
    sys.exit()

# Janela principal
window = tk.Tk()
window.title("Análise Climática")
window.geometry("450x150")

select_dates_button = tk.Button(window, text="Selecionar Intervalo de Datas 1961 e 2016", command=open_select_dates_window)
select_dates_button.pack()

generate_chart_button = tk.Button(window, text="Gerar Gráfico de Barras das temperaturas Máximas e Minimas", command=generate_bar_chart)
generate_chart_button.pack()

calculate_average_button = tk.Button(window, text="Calcular Média de Temperaturas Minimas e Máximas dos ultimos 11 anos", command=calculate_average_temperature)
calculate_average_button.pack()

most_rainy_button = tk.Button(window, text="Mês Mais Chuvoso", command=mes_mais_chuvoso)
most_rainy_button.pack()

quit_button = tk.Button(window, text="Sair", command=quit_program)
quit_button.pack()

window.mainloop()