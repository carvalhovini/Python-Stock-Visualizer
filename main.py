import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import logging

class StockVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Visualizer App")

        self.create_widgets()

    def create_widgets(self):
        # Label e Combobox para selecionar o ticker
        label_ticker = ttk.Label(self.root, text="Escolha um ticker:")
        label_ticker.grid(row=0, column=0, padx=10, pady=10)

        self.ticker_var = tk.StringVar()
        ticker_combobox = ttk.Combobox(self.root, textvariable=self.ticker_var)
        ticker_combobox['values'] = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'GOOG', 'NVDA', 'PYPL', 'INTC']
        ticker_combobox.grid(row=0, column=1, padx=10, pady=10)
        ticker_combobox.set('AAPL')  # Valor padrão

        # Labels e entradas para escolher a data de início e fim
        label_start_date = ttk.Label(self.root, text="Data de Início:")
        label_start_date.grid(row=1, column=0, padx=10, pady=5)
        self.start_date_entry = ttk.Entry(self.root)
        self.start_date_entry.grid(row=1, column=1, padx=10, pady=5)

        label_end_date = ttk.Label(self.root, text="Data de Fim:")
        label_end_date.grid(row=2, column=0, padx=10, pady=5)
        self.end_date_entry = ttk.Entry(self.root)
        self.end_date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botão para gerar o gráfico
        button = ttk.Button(self.root, text="Gerar Gráfico", command=self.plot_stock_chart)
        button.grid(row=3, column=0, columnspan=2, pady=10)

        # Área para exibir o gráfico
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, pady=10)

    def obter_dados_acao(self, ticker, start_date, end_date):
        try:
            # Obter dados históricos da ação
            dados = yf.download(ticker, start=start_date, end=end_date)

            # Verificar se os dados não estão vazios
            if not dados.empty:
                dados["Retorno Percentual"] = dados["Close"].pct_change() * 100
                return dados
            else:
                logging.warning(f"Falha ao obter dados para {ticker}")
                return None

        except ValueError as ve:
            logging.error(f"Entrada inválida: {ve}")
            return None
        except Exception as e:
            if "No timezone found" in str(e):
                logging.error(f"O ticker {ticker} pode estar deslistado.")
            else:
                logging.error(f"Erro ao processar {ticker}: {str(e)}")
            return None

    def plot_stock_chart(self):
        ticker = self.ticker_var.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        # Converter as datas para o formato esperado pelo yfinance
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        dados_acao = self.obter_dados_acao(ticker, start_date, end_date)

        if dados_acao is not None:
            self.ax.clear()
            self.ax.plot(dados_acao.index, dados_acao["Retorno Percentual"], label=f"{ticker} - Retorno Percentual")
            self.ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
            self.ax.set_title(f"Variação Percentual Diária - {ticker}")
            self.ax.set_xlabel("Data")
            self.ax.set_ylabel("Retorno Percentual (%)")
            self.ax.xaxis.set_major_locator(mdates.MonthLocator())  # Ajusta o espaçamento no eixo x
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # Formato da data no eixo x
            self.ax.legend()
            self.canvas.draw()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    root = tk.Tk()
    app = StockVisualizerApp(root)
    root.mainloop()
