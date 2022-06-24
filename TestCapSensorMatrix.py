import os as uos
import wavePlayer as wa
import wave
from machine import *
from utime import *

#Umschalten zwischen Ebenen
toggleSend=Pin(20, Pin.OUT)
toggleSend.value(1)
toggleReceive=Pin(21, Pin.IN)
toggle=0

#Setup zum Abspielen von .wav Dateien über einen Lautsprecher, Code wurde der wavePlayer Library entnommen
if __name__ == "__main__":

    player = wa.wavePlayer()
    waveFolder= "/edit"
    wavelist = []

    for i in uos.listdir(waveFolder):
        if i.find(".wav")>=0:
            wavelist.append(waveFolder+"/"+i)

send= Pin(14, Pin.OUT) # Stromquelle, die über einen 5,1 Megaohm Widerstand an die jeweiligen Drähte verbunden wird
send.value(0)

sleep(1)

#Methode, um die Verzögerung zwischen von Ausgang und Eingang des Signals zu messen. Der Parameter pinNumber überliefert dabei, welcher Eingang von der Methode untersucht werden soll 

def getState(pinNumber):
    #Erstellen der Variablen
    pX= Pin(pinNumber, Pin.IN)
    start=0
    end=0
    
    #Messen der Zeit zum Startzeitpunkt. Zum Startzeitpunkt wird der Strom über den Pin send gesandt, indem dessen Wert auf eins gesetzt wird.
    start= ticks_us()
    send.value(1)
    #Bis das Signal am Pin pX ankommt, wird gewartet.
    while pX.value()<1:
        pass
    end= ticks_us()
    send.value(0)
    #Bei Eingang des Signals wird der Endzeitpunkt gemessen und der Strom des Pins send abgestellt. Letztlich wird die vergangene Zeit von End- bis Startzeitpunkt in ticks zurückgegeben.
    return(end-start)

#Anlegen einer Matrix bestehend aus allen erfassbaren Buchstaben. Die Formatierung ist passend für spätere Nutzung gewählt. 
alphabetMatrix= [['-', '-', '-', '-', '-', '-'],
                 ['-', 'Q', 'W', 'E', 'R', 'T'],
                 ['-', 'A', 'S', 'D', 'F', 'G'],
                 ['-', 'Z', 'X', 'C', 'V', 'B']]
#Matrix für zweite Ebene                
alphabetMatrixLayer2= 	[['-', '-', '-', '-', '-', '-'],
                         ['-', 'Y', 'U', 'I', 'O', 'P'],
                         ['-', 'H', 'J', 'K', 'L', ''],
                         ['-', 'N', 'M', ',', '.', '/']]

while True:
    #Umschalten zwischen beiden Ebenen
    if toggleReceive.value() == 1:
        toggle= 1-toggle
    #Erstellen einer Liste, welche die in getState() gemessene Zeit zwischen Eingang und Ausgang des Stromsignals führt; bezogen auf "Zeilen" der Tastatur (QWERT, ASDFG, YXCVB)
    stateRows= [getState(2)-20, getState(1), getState(0)]	
    #getState(2) erhält eine Verringerung von 20 ticks, da Signale auf diesem Pin im Schnitt um 20 ticks stärker verzögert waren, als die Signale auf allen anderen Pins
    
    #Erstellen einer Liste, welche die in getState() gemessene Zeit zwischen Eingang und Ausgang des Stromsignals führt; bezogen auf "Spalten" der Tastatur (QAZ, WSX, EDC, RFV, TGB)
    stateClmns= [getState(6), getState(7), getState(8), getState(9), getState(10)]	
    
    #Erstellen einer Matrix, um wahrzunehmen, welche Taste gedrückt wird, bzw welche Reihe und Spalte vom Nutzer gedrückt wird. Die Matrix ist eine Liste bestehend aus vier Listen.
    stateMatrix= [[0,           stateClmns[0],              stateClmns[1],              stateClmns[2],              stateClmns[3],              stateClmns[4]             ],
                 [stateRows[0], stateClmns[0]+stateRows[0], stateClmns[1]+stateRows[0], stateClmns[2]+stateRows[0], stateClmns[3]+stateRows[0], stateClmns[4]+stateRows[0]],
                 [stateRows[1], stateClmns[0]+stateRows[1], stateClmns[1]+stateRows[1], stateClmns[2]+stateRows[1], stateClmns[3]+stateRows[1], stateClmns[4]+stateRows[1]],
                 [stateRows[2], stateClmns[0]+stateRows[2], stateClmns[1]+stateRows[2], stateClmns[2]+stateRows[2], stateClmns[3]+stateRows[2], stateClmns[4]+stateRows[2]]] 
    
    #Bestimmung den höchsten Wertes in der gesamten Matrix. max(stateMatrix) aufzurufen gibt dabei die Liste mit den höchsten Werten zurück.
    #Daraufhin kann man den Befehl ein weiteres Mal anwenden, um den höchsten Wert der gesamten Matrix zu erhalten
    strongestSignal= max(max(stateMatrix)) 
    
    #Zuordnen des höchsten Wertes zum Eintrag in der Matrix. Nachdem die Werte einander zugeordnet wurden, wird der passende Eintrag aus der Buchstabenmatrix überliefert.
    if strongestSignal>115: #115 aus Praxis ergebene Zahl
        for i in range(6):
            for j in range(4):
                if stateMatrix[j][i] == strongestSignal: #Vergleich zwischen jedem Matrixeintrag und strongestSignal
                    if toggle==0:
                        print(alphabetMatrix[j][i]);		 #Ausgabe des zugehörigen Buchstaben
                        path="/edit/"+alphabetMatrix[j][i] + ".wav" #Zusammenstellen des Pfades der zugehörigen Audiodatei
                        player.play(path)
                    elif toggle==1:
                        print(alphabetMatrixLayer2[j][i]);		 #Ausgabe des zugehörigen Buchstaben
                        path="/edit/"+alphabetMatrixLayer2[j][i] + ".wav" #Zusammenstellen des Pfades der zugehörigen Audiodatei
                        player.play(path)
    sleep(0.25)   
 