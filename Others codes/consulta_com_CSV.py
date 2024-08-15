import csv
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END
from tkinter import font as tkFont
from PIL import Image, ImageTk  # Biblioteca para manipulação de imagens


class BaseConhecimento:
    def __init__(self, csv_file):
        self.conhecimento = []
        self.carregar_csv(csv_file)

    def carregar_csv(self, csv_file):
        # Carrega o arquivo CSV como uma lista de dicionários
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.conhecimento.append(row)

    def consultar(self, entrada):
        resultados = []
        entrada = entrada.lower()

        for fato in self.conhecimento:
            nome = fato['Name'].lower()
            tipo1 = fato['Type 1'].lower()
            tipo2 = fato['Type 2'].lower()

            if nome in entrada:
                if 'tipo' in entrada:
                    resultado = f"{fato['Name']} é do tipo {fato['Type 1']}"
                    if fato['Type 2']:
                        resultado += f" e {fato['Type 2']}."
                    else:
                        resultado += "."
                    resultados.append(resultado)
                elif 'velocidade' in entrada:
                    resultados.append(f"{fato['Name']} tem {fato['Speed']} Pts de velocidade.")
                elif 'ataque' in entrada:
                    resultados.append(f"{fato['Name']} tem {fato['Attack']} Pts de ataque.")
                elif 'defesa' in entrada:
                    resultados.append(f"{fato['Name']} tem {fato['Defense']} Pts de defesa.")
                elif 'hp' in entrada:
                    resultados.append(f"{fato['Name']} tem {fato['HP']} Pts de HP.")
                elif 'pokemon' in entrada:
                    resultados.append(f"{fato['Name']}\nHP: {fato['HP']} \nAtaque: {fato['Attack']} \nDefesa: {fato['Defense']} \nVelocidade: {fato['Speed']} \nTipo(s): {fato['Type 1']} \n{fato['Type 2'] if fato['Type 2'] else 'Nenhum'}\n")
            elif entrada == tipo1 or entrada == tipo2:
                resultados.append(f"{fato['Name']} ({fato['Type 1']}, {fato['Type 2']})")

        return resultados


class App:
    def __init__(self, root, base_conhecimento):
        self.base_conhecimento = base_conhecimento
        
        # Configurações da janela principal
        root.title("Consultor de Base de Conhecimento Pokémon")
        root.configure(bg='#282a36')  # Cor de fundo do tema (fundo escuro)
        
        # Configuração da fonte
        fonte_principal = tkFont.Font(family="Helvetica", size=12, weight="bold")
        fonte_titulo = tkFont.Font(family="Helvetica", size=14, weight="bold")
        
        # Carregar a imagem
        self.imagem = Image.open("pokemon.png")  # Substitua pelo caminho da sua imagem
        self.imagem = self.imagem.resize((300, 150), Image.LANCZOS)  # Redimensiona a imagem, se necessário
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        
        # Rótulo para a imagem
        Label(root, image=self.imagem_tk, bg='#282a36').grid(row=0, column=0, columnspan=3, pady=0)
        
        # Rótulo de entrada de pergunta
        Label(root, text="Digite sua pergunta:", font=fonte_titulo, fg='#f8f8f2', bg='#282a36').grid(row=1, column=0, padx=10, pady=10)
        
        # Campo de entrada de pergunta
        self.pergunta_entry = Entry(root, width=25, font=fonte_principal, fg='#f8f8f2', bg='#44475a', insertbackground='#f8f8f2')
        self.pergunta_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Botão de consulta
        Button(root, text="Consultar", command=self.consultar_base, font=fonte_principal, fg='#282a36', bg='#50fa7b', activebackground='#50fa7b').grid(row=1, column=2, padx=10, pady=10)
        
        # Campo de texto para mostrar os resultados
        self.resultados_text = Text(root, height=10, width=60, font=fonte_principal, fg='#f8f8f2', bg='#44475a')
        self.resultados_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        
        # Barra de rolagem
        scrollbar = Scrollbar(root, command=self.resultados_text.yview, bg='#44475a')
        scrollbar.grid(row=2, column=3, sticky='nsew')
        self.resultados_text['yscrollcommand'] = scrollbar.set

    def consultar_base(self):
        entrada = self.pergunta_entry.get()
        resultados = self.base_conhecimento.consultar(entrada)
        self.resultados_text.delete(1.0, END)
        if resultados:
            for resultado in resultados:
                self.resultados_text.insert(END, resultado + "\n")
        else:
            self.resultados_text.insert(END, "Nenhum resultado encontrado.\n")

if __name__ == "__main__":
    # Instanciando a base de conhecimento com o arquivo Pokémon
    file_path = "Pokemon.csv"
    base_conhecimento = BaseConhecimento(file_path)
    root = Tk()
    app = App(root, base_conhecimento)
    root.mainloop()