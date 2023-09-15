#Importiamo pyautogui e yfinance
import pyautogui, datetime, keyboard, time
import yfinance as yf

run = True

def stock():
    def price_research(stock_name):
        #Creiamo 3 variabili di controllo
        controllo = 0
        media = 0
        frequenza = 0

        #apriamo il database
        f = open("prezzi_stock.txt", "r")

        #Controlliamo ogni riga del database per controllare se la nostra stock e presente
        for i in (f.readlines()):
            if stock_name in i:
                list(i)
                for y in i:

                    #Cerchiamo la parentesi nella riga della stock desiterata
                    if y =="(":

                        #Prendiamo la percentuale ed aggiungiamola alla variabile media
                        percentuale = i[controllo+1:controllo+6]
                        controllo = 0
                        media += float(percentuale) 
                        frequenza += 1
                        break
                    else:
                        controllo += 1

        #Calcoliamo la media della stock
        return media/frequenza

    try:
        #Prendere quale stock si vuole sapere se e in salita o discesa
        name = pyautogui.prompt("Inserire il nome della stock").upper()
        stock = yf.Ticker(name)

        #Chiedima a yfinance di darci il prezzo corrente della stock e il suo di chiusura
        prezzo_precedente = stock.info["previousClose"]
        prezzo_correte = stock.info["currentPrice"]

        #Otteniamo la percentuale del cambiamento del prezzo
        cambiamento = ((prezzo_correte - prezzo_precedente)/ prezzo_precedente) * 100

        #Mandiamo i dati a schermo
        pyautogui.alert(f"Nella giornata di ieri {name} a chiuso con {cambiamento}")

        #Salviamo i dati in un data base
        if pyautogui.confirm("Salvare le informazioni attuali?") == "OK":
            f = open("prezzi_stock.txt", "r")
            old = f.read()
            f.close()
            f = open("prezzi_stock.txt", "w")
            f.write(f"{old}\n{name} = {prezzo_correte}({cambiamento}), {datetime.datetime.now()}")
            f.close()

        #Calcoliamo l'andamento di una stock dal database
        if pyautogui.confirm("Controllare il l'andamento medio di una stock?") == "OK":
            x = pyautogui.prompt("Inserire la sigla della stock per vedere la sua media").upper()
            pyautogui.alert(f"La stock media di {x} e di {price_research(x)}")

        #Chiedere se si vuole vedere i dati nel database
        if pyautogui.confirm("Vedere il database?") == "OK":
            f = open("prezzi_stock.txt", "r")
            pyautogui.alert(f.read())
            f.close()
        
    except:
        pyautogui.alert("Qualcosa è andato storto riprovare")

#Main loop che fa decidere all'utente se eseguire il programma e quando fermarlo tramite delle hotkey
while run:
    if keyboard.is_pressed("ctrl") and keyboard.is_pressed("f9"):
        break
    if keyboard.is_pressed("ctrl") and keyboard.is_pressed("f10"):
        stock()