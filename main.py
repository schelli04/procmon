import psutil
import socket
import mysql.connector
import time
from config import *

# Datenbank-Objekt anlegen
try:
    mydb = mysql.connector.connect(
    host=DBHOST,
    port = DBPORT,
    user=DBUSER,
    password=DBPWD,
    database=DB
    )
except:
    print("Datenbankverbindung nicht erfolgreich")
    exit()
    
mycursor = mydb.cursor()

# Computername in Date schreiben
host = socket.gethostname()

# Zu überwachende Prozesse aus Datei einkesen
fobj = open("prozessliste.txt", "r")
prozessListeCheck = [procMon.strip() for procMon in fobj]
fobj.close()

# Liste der laufenden Prozesse erzeugen
prozessliste = [prozess for prozess in psutil.process_iter(['pid','name','username'])]

# Schleife über die zu monitorenden Prozesse
for monProc in prozessListeCheck:
    # Überwachungsvariable ob Prozess läuft wird zunächst auf False gesetzt
    laeuft=False
    #Schleife über laufende Prozesse
    for proc in prozessliste:
        # Vergleich ob der Prozess in einem der Prozesse aufgeführt ist
        # um Fehler durch Rechtschreibugn auszuschließen werden beide String in Kleinbuchstaben umgewandelt
        if monProc.lower() in str(proc.name()).lower():
            # Wenn der Prozess in der Prozessliste vorhanden ist wird ein Datensatz in die DB geschrieben
          
            # Wenn Prozess unter anderem Benutzernamen läuft, wird eine Exception geworfen.
            # Damit das Skript dennoch weiterläuft, wird ein Dummy Username geschrieben
            try:
                uname = proc.username()
            except:
                uname = "_Zugriff verweigert_"
            pname = proc.name()
            print(pname, " is running")
            # SQL Statement um in Datenbank zu schreiben
            sql = "INSERT INTO "+TABLE+" (time, host, username, proc, cputime) VALUES (%s, %s, %s, %s, %s)"
            val = (time.time(),
                host,
                uname,
                pname,
                proc.cpu_times().user
            )
            mycursor.execute(sql, val)
            mydb.commit()
        

