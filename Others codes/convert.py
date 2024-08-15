import csv

# Caminho do arquivo CSV e do arquivo Prolog
csv_file_path = 'Pokemon.csv'
prolog_file_path = 'pokemon.pl'

# Abrindo o arquivo Prolog para escrita
with open(prolog_file_path, 'w', encoding='utf-8') as prolog_file:
    # Lendo o arquivo CSV
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterando sobre cada linha no CSV
        for row in reader:
            # Extraindo os campos necessários e formatando como fato Prolog
            nome = row['Name'].replace("'", "")  # Remover apóstrofos para evitar conflitos no Prolog
            tipo1 = row['Type 1']
            tipo2 = row['Type 2'] if row['Type 2'] else 'none'  # Substituir valor vazio por 'none'
            hp = row['HP']
            ataque = row['Attack']
            defesa = row['Defense']
            velocidade = row['Speed']
            
            # Escrevendo o fato no arquivo Prolog
            prolog_file.write(f"pokemon('{nome}', '{tipo1}', '{tipo2}', {hp}, {ataque}, {defesa}, {velocidade}).\n")

# Caminho do arquivo Prolog gerado
prolog_file_path