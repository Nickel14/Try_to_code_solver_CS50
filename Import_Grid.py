## Importazione della griglia

import openpyxl

# Funzione per leggere la parte specifica della griglia (23 righe e 21 colonne)
def load_grid_from_xlsx(file_path, sheet_name):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]  # Usa il foglio attivo del file Excel
    
    grid = []
    
    # Definiamo l'intervallo di celle che vogliamo leggere (23 righe e 21 colonne)
    for row in sheet.iter_rows(min_row=1, max_row=23, min_col=1, max_col=21):
        grid_row = []
        for cell in row:
            if cell.value is None or cell.value == "":  # Cella vuota
                grid_row.append(None)  # Casella vuota che può contenere una parola
            else:  # Se la cella contiene una lettera o simbolo (ad esempio '$')
                grid_row.append(cell.value)  # Copia direttamente il valore della cella
        grid.append(grid_row)
    
    return grid

# Funzione per formattare la matrice come un unico stringa
def format_grid(grid):
    result = '"""\n'  # Iniziamo la stringa con """ e un \n per il primo ritorno a capo
    for row in grid:
        formatted_row = []
        for cell in row:
            if cell == "$":
                formatted_row.append("*")  # Sostituisce "$" con "*"
            elif cell is None:
                formatted_row.append("_")  # Sostituisce None con "_"
            else:
                formatted_row.append(str(cell))  # Mantiene il valore originale
        result += "".join(formatted_row) + "\n"  # Unisce la riga e va a capo
    result += '"""'  # Chiude la stringa con """
    return result

# Esempio di utilizzo
file_path = r"C:\Users\Utente\Downloads\CS50 2025.xlsx"  # Inserisci il percorso corretto
sheet_name = "Grif"
grid = load_grid_from_xlsx(file_path, sheet_name)

if grid:
    # Formatta la matrice come stringa e la stampa
    formatted_grid = format_grid(grid)
    print(formatted_grid)




