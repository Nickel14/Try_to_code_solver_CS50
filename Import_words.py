
#### --------------------------------------------------------------------- ####
## Importazione della lista di parole


import openpyxl

# Funzione per leggere i nomi dal foglio "Nomi"
def load_names_from_xlsx(file_path, sheet_name="Nomi"):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]  # Accedi al foglio "Nomi"
    
    names = []
    
    # Leggi i nomi dalla colonna A (modifica il range se necessario)
    for row in sheet.iter_rows(min_row=1, max_row=30, min_col=1, max_col=1):  # Ad esempio da A1 a A30
        for cell in row:
            if cell.value:  # Aggiungi solo se c'è un nome nella cella
                names.append(cell.value)
    
    return names

# Funzione per stampare la lista di nomi
def print_names(names):
    print("Lista dei nomi:")
    for name in names:
        print(name)

# Esempio di utilizzo
file_path = r"C:\Users\Utente\Downloads\CS50 2025.xlsx"  # Inserisci il percorso corretto

# Carica i nomi dal foglio "Nomi"
names = load_names_from_xlsx(file_path)

# Stampa la lista dei nomi
if names:
    print_names(names)
   
