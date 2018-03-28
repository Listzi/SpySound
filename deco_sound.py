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
Monson = wave.open(fichier,'r') # on reserve un espace memoire et on fixe l'etat du son
nbCanal = 1  # mono 
nbOctect = 1 # echantillon : 8 bits = 1 octet
frech = 44100 # frequence d'echantillonnage
nbr_bits=0
decoded_b=""
import binascii
for x in range(0,32):
    Monson.setpos(x)
    temp="{0:08b}".format(int(binascii.hexlify(Monson.readframes(1)),16))
    nbr_bits=nbr_bits+temp[6:]
    
nbr_deco=int(nbr_bits,2)

for i in range(nbr_deco):
    Monson.setpos(i)
    temp="{0:08b}".format(int(binascii.hexlify(Monson.readframes(1)),16))
    decoded_b=decoded_b+temp[6:]
    
nbr_chr=int(decoded_b[0:24],2)
last_bit=24
for x in range(nbr_chr):
    #decodage nbr d'oct du chr
    Info=int(decoded_b[last_bit:last_bit+2],2)
    #1 octet
    if Info==0:
        #valeur dec du chr
        temp=int(decoded_b[last_bit+2:last_bit+10],2)
        #valeur "txt" du chr + ajout au txt decode
        txt_fin=txt_fin+chr(temp)
        #mise a jour du rang de travail
        last_bit=last_bit+10
    #2 octets
    if Info==1:
        temp=int(decoded_b[last_bit+2:last_bit+18],2)
        txt_fin=txt_fin+chr(temp)
        last_bit=last_bit+18
    #3 octets
    if Info==2:
        temp=int(decoded_b[last_bit+2:last_bit+26],2)
        txt_fin=txt_fin+chr(temp)
        last_bit=last_bit+26
    #4 octets (max)
    if Info==3:
        temp=int(decoded_b[last_bit+2:last_bit+34],2)
        txt_fin=txt_fin+chr(temp)
        last_bit=last_bit+34
print(txt_fin)
    
print(i)    
print(Liste)
Monson.close()
