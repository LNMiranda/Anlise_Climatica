from tkinter import Tk, Label, Entry, Button, Toplevel

# Função para coletar os dados meteorológicos de um mês
def coletar_dados_mes(mes):
    window = Toplevel()
    window.title(f"Dados do mês {mes}")

    Label(window, text=f"Mês {mes}").grid(row=0, column=0, columnspan=2)
    Label(window, text="Temperatura máxima (°C):").grid(row=1, column=0)
    Label(window, text="Temperatura mínima (°C):").grid(row=2, column=0)

    temperatura_maxima_entry = Entry(window)
    temperatura_maxima_entry.grid(row=1, column=1)
    temperatura_minima_entry = Entry(window)
    temperatura_minima_entry.grid(row=2, column=1)

    if mes in dados_meses:
        temperatura_maxima_entry.insert(0, str(dados_meses[mes][0]))
        temperatura_minima_entry.insert(0, str(dados_meses[mes][1]))

    def salvar_dados():
        temperatura_maxima = float(temperatura_maxima_entry.get().replace(',', '.'))
        temperatura_minima = float(temperatura_minima_entry.get().replace(',', '.'))

        if temperatura_minima > temperatura_maxima:
            Label(window, text="Erro: A temperatura mínima não pode ser maior que a temperatura máxima!").grid(row=4, column=0, columnspan=2)
        elif temperatura_maxima < -90 or temperatura_maxima > 60:
            Label(window, text="Erro: A temperatura máxima deve estar entre -90°C e +60°C!").grid(row=4, column=0, columnspan=2)
        elif temperatura_minima < -90 or temperatura_minima > 60:
            Label(window, text="Erro: A temperatura mínima deve estar entre -90°C e +60°C!").grid(row=4, column=0, columnspan=2)
        else:
            dados_meses[mes] = (temperatura_maxima, temperatura_minima)
            window.destroy()

    salvar_button = Button(window, text="Salvar", command=salvar_dados)
    salvar_button.grid(row=3, column=0, columnspan=2)

# Função para abrir a janela de edição do mês selecionado
def abrir_janela_edicao(mes):
    coletar_dados_mes(mes)

# Criar janela principal
window = Tk()
window.title("Dados Meteorológicos")

Label(window, text="Selecione o mês para editar os dados:").grid(row=0, column=0, columnspan=2)

# Criar botões para cada mês
for mes in range(1, 13):
    button = Button(window, text=f"Mês {mes}", command=lambda m=mes: abrir_janela_edicao(m))
    button.grid(row=(mes-1)//2 + 1, column=(mes-1)%2)

# Criar janela para resultados
def exibir_resultados():
    resultados_window = Toplevel()
    resultados_window.title("Resultados")

    Label(resultados_window, text="Meses com as maiores temperaturas:").pack()
    for mes, temperatura in meses_maiores:
        Label(resultados_window, text=f"Mês {mes}: Temperatura máxima = {temperatura[0]}°C, Temperatura mínima = {temperatura[1]}°C").pack()

    Label(resultados_window, text="Meses com as menores temperaturas:").pack()
    for mes, temperatura in meses_menores:
        Label(resultados_window, text=f"Mês {mes}: Temperatura máxima = {temperatura[0]}°C, Temperatura mínima = {temperatura[1]}°C").pack()

    Label(resultados_window, text=f"Média das temperaturas máximas: {media_maximas:.2f}°C").pack()
    Label(resultados_window, text=f"Média das temperaturas mínimas: {media_minimas:.2f}°C").pack()

# Botão para exibir resultados
resultados_button = Button(window, text="Exibir Resultados", command=exibir_resultados)
resultados_button.grid(row=7, column=0, columnspan=2)

# Dicionário para armazenar os dados dos meses
dados_meses = {}

window.mainloop()
