import random

class Cella:
	def __init__(self, lettera):
		self.lettera = lettera
		self.chiavePosizioneOrizzontale = None
		self.occupataOrizzontale = False
		self.chiavePosizioneVerticale = None
		self.occupataVerticale = False
	
	def impostaChiavePosizione(self, chiavePosizione):
		orientamento = chiavePosizione[0]
		if orientamento == 0: self.chiavePosizioneOrizzontale = chiavePosizione
		else: self.chiavePosizioneVerticale = chiavePosizione
	
	def chiavePosizione(self, orientamento):
		if orientamento == 0: return self.chiavePosizioneOrizzontale
		return self.chiavePosizioneVerticale
	
	def impostaOccupata(self, occupazione, orientamento):
		if orientamento == 0: self.occupataOrizzontale = occupazione
		else: self.occupataVerticale = occupazione
	
	def occupata(self, orientamento):
		if orientamento == 0: return self.occupataOrizzontale
		return self.occupataVerticale
	
	def __repr__(self):
		return self.lettera

class Posizione:
	def __init__(self, coordinate, orientamento, lunghezza):
		self.coordinate = coordinate
		self.orientamento = orientamento
		self.lunghezza = lunghezza
		self.occupata = False
		self.incastri = 0
	
	def __repr__(self): 
		return "(coordinate: %s, orientamento: %d, lunghezza: %d, incastri: %d)" % (self.coordinate, 
			self.orientamento, self.lunghezza, self.incastri)

class Cruciverba:
	def __init__(self, righe, colonne, statoIniziale):
		self.righe = righe
		self.colonne = colonne
		self.griglia = []
		self.posizioni = {}
		self._inizializzaGriglia(statoIniziale)
		self._inizializzaMappaPosizioni()
		self._inizializzaCelleGriglia()
	
	def _inizializzaGriglia(self, statoIniziale):
		self.griglia = [[Cella('') for _ in range(self.colonne)] 
			for _ in range(self.righe)]
		righeStatoIniziale = statoIniziale[1:-1].split('\n')
		for r in range(self.righe):
			for c in range(self.colonne):
				cella = self.griglia[r][c]
				lettera = righeStatoIniziale[r][c]
				if lettera == '*': cella.lettera = lettera
					
	
	def _inizializzaMappaPosizioni(self):
		posizioni = self._trovaPosizioni()
		for posizione in posizioni:
			chiave = (posizione.orientamento, posizione.coordinate)
			self.posizioni[chiave] = posizione
	
	def _inizializzaCelleGriglia(self):
		posizioni = self.posizioni.values()
		for posizione in posizioni:
			self._inizializzaCellePosizione(posizione)
	
	def _inizializzaCellePosizione(self, posizione):
		chiavePosizione = (posizione.orientamento, posizione.coordinate)
		(riga, colonna) = posizione.coordinate
		for _ in range(posizione.lunghezza):
			cella = self.griglia[riga][colonna]
			cella.impostaChiavePosizione(chiavePosizione)
			if posizione.orientamento == 0: colonna += 1
			else: riga += 1
	
	def _trovaPosizioni(self):
		posizioniOrizzontali = self._trovaPosizioniOrizzontali()
		posizioniVerticali = self._trovaPosizioniVerticali()
		return posizioniOrizzontali + posizioniVerticali
	
	def _trovaPosizioniOrizzontali(self):
		posizioni = []
		for riga in range(self.righe):
			posizioni += self._trovaPosizioniInRiga(riga)
		return posizioni
	
	def _trovaPosizioniInRiga(self, riga):
		posizioni = []
		datiPosizioni = Cruciverba.datiPosizioniInCelle(self.prelevaRiga(riga))
		for (colonna, lunghezza) in datiPosizioni:
			coordinate = (riga, colonna)
			posizioni.append(Posizione(coordinate, 0, lunghezza))
		return posizioni
	
	def _trovaPosizioniVerticali(self):
		posizioni = []
		for colonna in range(self.colonne):
			posizioni += self._trovaPosizioniInColonna(colonna)
		return posizioni
	
	def _trovaPosizioniInColonna(self, colonna):
		posizioni = []
		datiPosizioni = Cruciverba.datiPosizioniInCelle(
			self.prelevaColonna(colonna))
		for (riga, lunghezza) in datiPosizioni:
			coordinate = (riga, colonna)
			posizioni.append(Posizione(coordinate, 1, lunghezza))
		return posizioni
	
	@staticmethod
	def datiPosizioniInCelle(celle):
		datiPosizioni = []
		indiceInizio = indiceFine = 0
		while indiceInizio < len(celle):
			indiceInizio = Cruciverba.trovaProssimoBlank(indiceFine, celle)
			if indiceInizio < len(celle):
				indiceFine = Cruciverba.trovaProssimoAsterisco(
					indiceInizio, celle)
				lunghezza = indiceFine - indiceInizio
				if lunghezza > 3: 
					datiPosizioni.append((indiceInizio, lunghezza))
		return datiPosizioni
	
	def prossimaPosizioneInserimento(self, posizionePrecedente = None):
		posizioniCandidate = []
		if posizionePrecedente != None:
			posizioniCandidate = self._trovaPosizioniLibereIntersecanti(
				posizionePrecedente)
		if posizioniCandidate == []: 
			posizioniCandidate = [posizione for posizione in 
				self.posizioni.values() if not posizione.occupata]
		return Cruciverba.posizioneMigliore(posizioniCandidate)
	
	def _trovaPosizioniLibereIntersecanti(self, posizionePrecedente):
		posizioni = []
		(riga, colonna) = posizionePrecedente.coordinate
		orientamento = Cruciverba.opposto(posizionePrecedente.orientamento)
		for _ in range(posizionePrecedente.lunghezza):
			cella = self.griglia[riga][colonna]
			if not cella.occupata(orientamento):
				chiavePosizione = cella.chiavePosizione(orientamento)
				if chiavePosizione != None:
					posizioni.append(self.posizioni[chiavePosizione])
			if posizionePrecedente.orientamento == 0: colonna += 1
			else: riga += 1
		return posizioni
		
	def modelloParola(self, posizione):
		modello = []
		(riga, colonna) = posizione.coordinate
		for _ in range(posizione.lunghezza):
			lettera = self.griglia[riga][colonna].lettera
			letteraPrima = self._ottieniLetteraPrima(
				(riga, colonna), posizione.orientamento)
			letteraDopo = self._ottieniLetteraDopo(
				(riga, colonna), posizione.orientamento)
			modello.append((letteraPrima, lettera, letteraDopo))
			if posizione.orientamento == 0: colonna += 1
			else: riga += 1
		return modello
	
	def _ottieniLetteraPrima(self, coordinate, orientamento):
		(riga, colonna) = coordinate
		if orientamento == 0: riga -= 1
		else: colonna -= 1
		if riga >= 0 and colonna >= 0:
			return self.griglia[riga][colonna].lettera
		return '';
	
	def _ottieniLetteraDopo(self, coordinate, orientamento):
		(riga, colonna) = coordinate
		if orientamento == 0: riga += 1
		else: colonna += 1
		if riga < self.righe and colonna < self.colonne:
			return self.griglia[riga][colonna].lettera
		return '';
	
	def inserisciParola(self, parola, posizione):
		if posizione.occupata: raise Exception
		(riga, colonna) = posizione.coordinate
		orientamentoOpposto = Cruciverba.opposto(posizione.orientamento)
		for i in range(posizione.lunghezza):
			cella = self.griglia[riga][colonna]
			if cella.lettera == '':
				cella.lettera = parola[i]
				chiavePosizioneIntersecante = cella.chiavePosizione(
					orientamentoOpposto)
				if chiavePosizioneIntersecante != None:
					self.posizioni[chiavePosizioneIntersecante].incastri += 1
			elif cella.lettera != parola[i]: raise Exception
			cella.impostaOccupata(True, posizione.orientamento)
			if posizione.orientamento == 0: colonna += 1
			else: riga += 1
		posizione.occupata = True
	
	def rimuoviParola(self, posizione):
		if not posizione.occupata: return
		(riga, colonna) = posizione.coordinate
		orientamentoOpposto = Cruciverba.opposto(posizione.orientamento)
		for i in range(posizione.lunghezza):
			cella = self.griglia[riga][colonna]
			if not cella.occupata(orientamentoOpposto):
				cella.lettera = ''
				chiavePosizioneIntersecante = cella.chiavePosizione(
					orientamentoOpposto)
				if chiavePosizioneIntersecante != None:
					self.posizioni[chiavePosizioneIntersecante].incastri -= 1
			cella.impostaOccupata(False, posizione.orientamento)
			if posizione.orientamento == 0: colonna += 1
			else: riga += 1
		posizione.occupata = False
		
	@staticmethod
	def trovaProssimoBlank(indicePartenza, celle):
		return Cruciverba.trovaProssimoCarattere('', indicePartenza, celle)
	
	@staticmethod
	def trovaProssimoAsterisco(indicePartenza, celle):
		return Cruciverba.trovaProssimoCarattere('*', indicePartenza, celle)
	
	@staticmethod
	def trovaProssimoCarattere(carattere, indicePartenza, celle):		
		i = indicePartenza
		while i < len(celle):
			if celle[i].lettera == carattere: return i
			i += 1
		return i
	
	#sbagliata
	@staticmethod
	def posizioneMigliore(posizioni):
		posizioneMigliore = None
		for posizione in posizioni:
			if posizioneMigliore == None: posizioneMigliore = posizione
			elif posizione.incastri > posizioneMigliore.incastri:
				posizioneMigliore = posizione
			elif (posizione.incastri == posizioneMigliore.incastri and
				posizione.lunghezza > posizioneMigliore.lunghezza):
				posizioneMigliore = posizione
		return posizioneMigliore
	
	def prelevaRiga(self, riga):
		return self.griglia[riga]
	
	def prelevaColonna(self, colonna):
		return [self.griglia[i][colonna] for i in range(self.righe)]
	
	@staticmethod
	def opposto(orientamento):
		return (orientamento + 1) % 2
	
	def __repr__(self):
		stringa = ''
		bordo =  '+' + ''.join(['---+' for _ in range(self.colonne)]) + '\n'
		for r in range(self.righe):
			stringa += bordo
			for c in range(self.colonne):
				lettera = self.griglia[r][c].lettera
				if c == 0: stringa += '|'
				stringa += ' ' + (lettera != '' and lettera or ' ') + ' |'
			stringa += '\n'
		stringa += bordo
		return stringa
				

def riempiCruciverba(cruciverba, parole, posizionePrecedente = None):
	posizione = cruciverba.prossimaPosizioneInserimento(posizionePrecedente)
	"""
	fh = open('outcrux', 'a')
	fh.write(repr(posizione) + '\n' + repr(cruciverba) + '\n')
	fh.close()
	"""
	if posizione == None: return True
	modello = cruciverba.modelloParola(posizione)
	paroleDaTentare = cercaParole(modello, parole)
	posizioneSuccessiva = None
	lettereEscluse = ''
	indiceIntersezione = -1
	for (parola, _) in paroleDaTentare:
		if indiceIntersezione != -1 and (parola[indiceIntersezione] 
			in lettereEscluse): continue
		cruciverba.inserisciParola(parola, posizione)
		if posizioneSuccessiva == None:
			posizioneSuccessiva = cruciverba.prossimaPosizioneInserimento(posizione)
			indiceIntersezione = calcolaIndiceIntersezione(posizione, posizioneSuccessiva)
		#parole.remove(parola)
		if riempiCruciverba(cruciverba, parole, posizione) == True: return True
		else: lettereEscluse += parola[indiceIntersezione]
		cruciverba.rimuoviParola(posizione)
		#parole.insert(0, parola)
	return False

def calcolaIndiceIntersezione(posizioneX, posizioneY):
	if posizioneY == None: return -1
	if posizioneX.orientamento == 0:
		return posizioneY.coordinate[1] - posizioneX.coordinate[1]
	else: return posizioneY.coordinate[0] - posizioneX.coordinate[0]

def cercaParole(modello, parole):
	risultatoRicerca = []
	for parola in parole:
		punteggio = valutaParola(parola, modello)
		if punteggio != -1: risultatoRicerca.append((parola, punteggio))
	return sorted(risultatoRicerca, reverse = True, 
		key = lambda x: x[1])			## key = lambda (_, punteggio): punteggio)   
## Commento per ALESSANDRO: la riga sopra originalmente era come è difianco commentata, ma la funzione lambda mi dava errori
##							scrivendolo poi cosi, il codice almeno ha girato, anceh se incorrettamente alla fine, come ti ho detto oggi


def valutaParola(parola, modello):
	if len(parola) != len(modello): return -1
	punteggioTotale = 0
	for i in range(len(modello)):
		punteggio = valutaAbbinamento(parola[i], modello[i])
		if punteggio == -1: return -1
		punteggioTotale += punteggio
	return punteggioTotale

def valutaAbbinamento(lettera, modello):
	(letteraPrima, letteraModello, letteraDopo) = modello
	if letteraModello != '' and letteraModello != lettera: return -1
	if letteraModello == lettera: return 0
	punteggio = 0
	if consonante(lettera):
		if letteraDopo == '*': return 0
		if vocale(letteraPrima): punteggio += 1
		if vocale(letteraDopo): punteggio += 1
	elif vocale(lettera):
		if consonante(letteraPrima): punteggio += 1
		if consonante(letteraDopo): punteggio += 1
	return punteggio

def consonante(lettera):
	return lettera in "*bcdfghjklmnpqrstvwxyz"

def vocale(lettera):
	return lettera in "*aeiou"

def ottieniListaParole():
	fh = open('paroleItaliano.txt', 'r')
	return fh.read().split('\n')

statoInizialeCruciverba = """ 
*********************
*****_***************
**_**_**_************
___**_____***********
**____**_************
****_***____*********
****_**_**********_**
****_____*******_*_**
**___**_*******_____*
**_****_**_*****_*_**
**_****_____****_****
**********_*_*_____**
*********____**_*****
************_**_*****
***********_____*____
************_*_***_**
**************_***_**
**************_____**
*************_*_*****
*************___*****
*************_*******
************____*****
*************_*******
"""

### Questo è la griglia data

parole = ottieniListaParole()
cruciverba = Cruciverba(23, 21, statoInizialeCruciverba) ## questa valori, 23x21 li ho modificati, inizialmente non erano cosi
random.shuffle(parole)
print(riempiCruciverba(cruciverba, parole)) ## Anche le parole nel file .txt sono state modificate e sono quelle date
print(cruciverba)

