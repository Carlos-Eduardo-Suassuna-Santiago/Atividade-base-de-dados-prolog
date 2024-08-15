# Importações necessárias para a aplicação
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, font as tkFont
from PIL import Image, ImageTk
from swiplserver import PrologMQI, PrologThread

# Classe que lida com a base de conhecimento Prolog
class BaseConhecimentoProlog:
    def __init__(self, prolog_file):
        '''
    Construtor da classe, recebe o caminho do arquivo Prolog e inicializa uma nova thread Prolog.
    prolog_file: Caminho para o arquivo Prolog que contém a base de conhecimento.
    prolog_thread: Thread de execução Prolog usada para enviar consultas à base de conhecimento.
    query("consult(...)): Carrega o arquivo Prolog para uso dentro da aplicação.
    '''
        # Inicializa a classe com o caminho do arquivo Prolog
        self.prolog_file = prolog_file
        # Cria uma nova thread Prolog para enviar consultas
        self.prolog_thread = PrologThread(PrologMQI())
        # Carrega o arquivo Prolog na thread
        self.prolog_thread.query(f"consult('{self.prolog_file}')")

    def consultar(self, entrada):
        '''
        Função que recebe uma string de entrada, constrói e executa consultas Prolog, e retorna uma lista de resultados.
        entrada: A consulta do usuário convertida para minúsculas para facilitar a análise.
        resultados: Lista onde os resultados da consulta serão armazenados.
        '''
        # Converte a entrada do usuário para minúsculas
        entrada = entrada.lower()
        # Inicializa uma lista para armazenar os resultados
        resultados = []

        '''
        pokemon_name: Extrai o nome do Pokémon da entrada do usuário.
        consulta: Cria a consulta Prolog para obter a informação desejada do Pokémon e se ele é lendário.
        query: Executa a consulta Prolog.
        resultados.append(...): Adiciona o resultado formatado à lista de resultados.
        '''
        # Verifica se a entrada contém "tipo do" e realiza a consulta apropriada
        if 'tipo do' in entrada:
            pokemon_name = entrada.split('tipo do ')[-1].strip()
            consulta = f"pokemon('{pokemon_name}', Tipo1, Tipo2, _, _, _, _, Lendario)"
            for sol in self.prolog_thread.query(consulta):
                tipo2 = sol.get("Tipo2", "nenhum")
                lendario = "Sim" if sol.get("Lendario", "false").lower() == "true" else "Não"
                resultados.append(f"{pokemon_name.capitalize()} é do tipo: {sol['Tipo1']}, {tipo2} (Lendário: {lendario})".strip())
        
        # Verifica se a entrada contém "pokemons do tipo" ou "pokemons de tipo"
        elif 'pokemons do tipo' in entrada or 'pokemons de tipo' in entrada:
            tipo_especifico = entrada.split('pokemons do tipo ')[-1].strip() if 'pokemons do tipo' in entrada else entrada.split('pokemons de tipo ')[-1].strip()
            consulta = f"pokemon(Nome, '{tipo_especifico}', _, _, _, _, _, Lendario) ; pokemon(Nome, _, '{tipo_especifico}', _, _, _, _, Lendario)"
            for sol in self.prolog_thread.query(consulta):
                lendario = "Sim" if sol.get("Lendario", "false").lower() == "true" else "Não"
                resultados.append(f"{sol['Nome'].capitalize()} (Lendário: {lendario})")
            # Ordena a lista de resultados em ordem alfabética
            resultados.sort()

        # Verifica se a entrada contém "pokemons lendarios" ou "pokemons lendários"
        elif 'pokemons lendarios' in entrada or 'pokemons lendários' in entrada:
            consulta = "pokemon(Nome, _, _, _, _, _, _, true)"
            for sol in self.prolog_thread.query(consulta):
                resultados.append(sol['Nome'].capitalize())
            # Ordena a lista de resultados em ordem alfabética
            resultados.sort()

        # Verifica se a entrada contém "velocidade do"
        elif 'velocidade do' in entrada:
            pokemon_name = entrada.split('velocidade do ')[-1].strip()
            consulta = f"pokemon('{pokemon_name}', _, _, _, _, _, Velocidade, _)"
            for sol in self.prolog_thread.query(consulta):
                resultados.append(f"{pokemon_name.capitalize()} tem {sol.get('Velocidade', 'não disponível')} Pts de velocidade.")
        
        # Verifica se a entrada contém "ataque do"
        elif 'ataque do' in entrada:
            pokemon_name = entrada.split('ataque do ')[-1].strip()
            consulta = f"pokemon('{pokemon_name}', _, _, _, Ataque, _, _, _)"
            for sol in self.prolog_thread.query(consulta):
                resultados.append(f"{pokemon_name.capitalize()} tem {sol.get('Ataque', 'não disponível')} Pts de ataque.")
        
        # Verifica se a entrada contém "defesa do"
        elif 'defesa do' in entrada:
            pokemon_name = entrada.split('defesa do ')[-1].strip()
            consulta = f"pokemon('{pokemon_name}', _, _, _, _, Defesa, _, _)"
            for sol in self.prolog_thread.query(consulta):
                resultados.append(f"{pokemon_name.capitalize()} tem {sol.get('Defesa', 'não disponível')} Pts de defesa.")
        
        # Verifica se a entrada contém "hp do"
        elif 'hp do' in entrada:
            pokemon_name = entrada.split('hp do ')[-1].strip()
            consulta = f"pokemon('{pokemon_name}', _, _, HP, _, _, _, _)"
            for sol in self.prolog_thread.query(consulta):
                resultados.append(f"{pokemon_name.capitalize()} tem {sol.get('HP', 'não disponível')} Pts de HP.")
        
        # Verifica se a entrada contém "pokemon" e realiza a consulta completa
        elif 'pokemon' in entrada:
            pokemon_name = entrada.split('pokemon ')[-1].strip()
            consulta = f"pokemon('{pokemon_name}', Tipo1, Tipo2, HP, Ataque, Defesa, Velocidade, Lendario)"
            for sol in self.prolog_thread.query(consulta):
                tipo2 = sol.get("Tipo2", "nenhum")
                lendario = "Sim" if sol.get("Lendario", "false").lower() == "true" else "Não"
                resultados.append(
                    f"{pokemon_name.capitalize()}\n"
                    f"HP: {sol.get('HP', 'não disponível')}\n"
                    f"Ataque: {sol.get('Ataque', 'não disponível')}\n"
                    f"Defesa: {sol.get('Defesa', 'não disponível')}\n"
                    f"Velocidade: {sol.get('Velocidade', 'não disponível')}\n"
                    f"Tipo(s): {sol['Tipo1']}, {tipo2}\n"
                    f"Lendário: {lendario}".strip()
                )
        
        # Caso a entrada não corresponda a nenhum dos casos acima
        else:
            consulta = f"pokemon('{entrada}', _, _, _, _, _, _, _)"
            for sol in self.prolog_thread.query(consulta):
                resultados.append(entrada.capitalize())
        
        # Retorna os resultados da consulta
        return resultados

# Classe que define a interface gráfica da aplicação
class App:
    '''
    Obtém a consulta do usuário, chama a função consultar da classe BaseConhecimentoProlog, e exibe os resultados.
    delete: Limpa a área de resultados antes de exibir novos resultados.
    insert: Adiciona cada resultado na área de texto.
    ao_pressionar_enter: Chama a função consultar_base ao pressionar a tecla Enter.
    '''
    def __init__(self, root, base_conhecimento):
        self.base_conhecimento = base_conhecimento
        
        # Configurações da janela principal
        root.title("Consultor de Base de Conhecimento Pokémon")
        root.configure(bg='#282a36')
        
        # Definindo as fontes utilizadas na interface
        fonte_principal = tkFont.Font(family="Helvetica", size=12, weight="bold")
        fonte_titulo = tkFont.Font(family="Helvetica", size=14, weight="bold")
        
        # Carrega e ajusta a imagem do Pokémon
        self.imagem = Image.open("image/pokemon.png")
        self.imagem = self.imagem.resize((300, 150), Image.LANCZOS)
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        
        # Adiciona a imagem e os labels à interface
        Label(root, image=self.imagem_tk, bg='#282a36').grid(row=0, column=0, columnspan=3, pady=10)
        Label(root, text="Digite sua pergunta:", font=fonte_titulo, fg='#f8f8f2', bg='#282a36').grid(row=1, column=0, padx=10, pady=10)
        
        # Campo de entrada de texto para as perguntas do usuário
        self.pergunta_entry = Entry(root, width=25, font=fonte_principal, fg='#f8f8f2', bg='#44475a', insertbackground='#f8f8f2')
        self.pergunta_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Botão para acionar a consulta na base de conhecimento
        Button(root, text="Consultar", command=self.consultar_base, font=fonte_principal, fg='#282a36', bg='#FFFF00').grid(row=1, column=2, padx=10, pady=10)
        
        # Área de texto onde os resultados das consultas serão exibidos
        self.resultados_text = Text(root, height=20, width=60, font=fonte_principal, fg='#f8f8f2', bg='#44475a')
        self.resultados_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        
        # Barra de rolagem para a área de resultados
        scrollbar = Scrollbar(root, command=self.resultados_text.yview, bg='#44475a')
        scrollbar.grid(row=2, column=3, sticky='nsew')
        self.resultados_text['yscrollcommand'] = scrollbar.set
        
        # Vincula a tecla "Enter" para acionar a função de consulta
        root.bind('<Return>', self.ao_pressionar_enter)

    def consultar_base(self):
        # Obtém a entrada do usuário e realiza a consulta na base de conhecimento
        entrada = self.pergunta_entry.get()
        resultados = self.base_conhecimento.consultar(entrada)
        self.resultados_text.delete(1.0, END)
        # Exibe os resultados na área de texto
        if resultados:
            for resultado in resultados:
                self.resultados_text.insert(END, resultado + "\n")
        else:
            self.resultados_text.insert(END, "Nenhum resultado encontrado.\n")
    
    def ao_pressionar_enter(self, event):
        # Aciona a consulta quando a tecla "Enter" é pressionada
        self.consultar_base()

# Código principal que inicializa a aplicação
if __name__ == "__main__":
    # Define o arquivo Prolog a ser utilizado
    prolog_file = "data/base_dados_pokemon.pl"
    # Cria a instância da classe BaseConhecimentoProlog
    base_conhecimento = BaseConhecimentoProlog(prolog_file)
    
    # Cria a janela principal da aplicação
    root = Tk()
    # Cria a instância da aplicação e passa a base de conhecimento
    app = App(root, base_conhecimento)
    # Inicia o loop de eventos da interface gráfica
    root.mainloop()