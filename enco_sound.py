import wave
# https://pythonspot.com/tk-file-dialogs/
from tkinter import filedialog
from tkinter import *
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "T:/",title = "Select file",filetypes = (("WAV files","*.wav"),("all files","*.*")))
fichier=root.filename
root.destroy()
print (fichier)
print("Création d'un fichier audio au format WAV (PCM 8 bits mono 44100)")
Monson = wave.open('T:\Downloads\Starset2min8bitmono.wav','r') # on reserve un espace memoire et on fixe l'etat du son
nbCanal = 1  # mono 
nbOctect = 1 # echantillon : 8 bits = 1 octet
frech = 44100 # frequence d'echantillonnage
#   creation du fichier son
bin_finale="8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888"
nbr_bits=0
Liste = []
print("nb d'echantillonage :",Monson.getnframes())
import binascii
plage = 50
for i in range(0,plage):
    Monson.setpos(i)
    temp="{0:08b}".format(int(binascii.hexlify(Monson.readframes(1)),16))
    Liste.append(str(temp[:6]+bin_finale[i*2:i*2+2]))
print(Liste)
Monson.close()
