import wave
import math
# https://pythonspot.com/tk-file-dialogs/
from tkinter import filedialog
from tkinter import *
def deco():
    #chaine de chr binaires extraite du fichier son
    decoded_b=value2.get()
    #decodage entete
    nbr_bits=int(decoded_b[0:32],2)
    nbr_chr=int(decoded_b[32:56],2)
    #dernier bit/ rang de travail
    last_bit=56
    temp=0
    #resultat final lisible par user
    txt_fin=''
    #nombre de chr (a decoder)
    print(int(decoded_b[0:32],2))
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
    messagebox.showinfo('Attention Confidentiel', txt_fin)
    result.set(txt_fin)
    print(txt_fin)
def enco():
 root = Tk()
 root.filename =  filedialog.askopenfilename(initialdir = "T:/",title = "Select file",filetypes = (("WAV files","*.wav"),("all files","*.*")))
 fichier=root.filename
 root.destroy()
 Monson = wave.open(fichier,'r') # on reserve un espace memoire et on fixe l'etat du son
 #txt a enco
 intxt=str(value.get())
 #chaine de chr binaires a enco dans le fichier son
 bin_finale=""
 #longueur du msg
 lenght=int(len(intxt))
 print(lenght)
 #entete
 bin_finale="{0:024b}".format(lenght)
 #message
 for x in range(lenght):
    #valeur decimal du chr
    dec_val=0
    #nbr d'octet pour enco valeur dec du chr
    Info=""
    #obtention valeur dec du chr selectionne
    dec_val=ord(intxt[x])
    #si valeur dec du chr encodable sur 1 oct :
    if dec_val<=255:
        Info='00'
        #"{0:08b}".format(dec_val) permet de rajoutter des zeros pour avoir 8 bits
        bin_finale=bin_finale+Info+"{0:08b}".format(dec_val)
    #si valeur dec du chr encodable sur 2 oct :
    if dec_val>255 and dec_val<=65535:
        Info='01'
        #"{0:016b}".format(dec_val) permet de rajoutter des zeros pour avoir 16 bits
        bin_finale=bin_finale+Info+"{0:016b}".format(dec_val)
    #si valeur dec du chr encodable sur 3 oct :
    if dec_val>65535 and dec_val<=16777215:
        Info='10'
        bin_finale=bin_finale+Info+"{0:024b}".format(dec_val)
    #si valeur dec du chr encodable sur 4 oct :
    if dec_val>16777215 and dec_val<=4294967295:
        Info='11'
        bin_finale=bin_finale+Info+"{0:032b}".format(dec_val)
  #ajout nombre de bits à enco
 bin_finale=str("{0:032b}".format(len(bin_finale)+32))+bin_finale
 nbr_bits=int(math.ceil(len(bin_finale)/2))
 print(bin_finale)
 
 Liste = []
 
 if Monson.getnframes()<nbr_bits:
    messagebox.showinfo('Alerte', 'Attention texte trop long !!')
    return
 import binascii
 plage = nbr_bits
 for i in range(0,plage):
     Monson.setpos(i)
     temp="{0:08b}".format(int(binascii.hexlify(Monson.readframes(1)),16))
     Liste.append(str(temp[:6]+bin_finale[i*2:i*2+2]))
 print(Liste)
 Monson.close()
def cln():
    result.set(" ")
#(C) Fabrice Sincère

from tkinter import *
# Création de la fenêtre principale (main window)
Mafenetre = Tk()

Mafenetre.title('Spysound')
#Mafenetre.geometry('')

value = StringVar() 
value.set("Que faut-il encoder ?")
entree = Entry(Mafenetre, textvariable=value ,width=100)
entree.pack(side = TOP, padx = 5, pady = 5)

# Création d'un widget Button (bouton Lancer)
BoutonEnco = Button(Mafenetre, text ='Lancer l\'encodage', command = enco)
# Positionnement du widget avec la méthode pack()
BoutonEnco.pack(side = TOP, padx = 5, pady = 5)

#result1= StringVar()
#result1.set("")
#Label2 = Label(Mafenetre, textvariable = result1)
#Label2.pack(side = TOP, padx = 5, pady = 5)

value2 = StringVar() 
value.set("Que faut-il décoder ?")
entree = Entry(Mafenetre, textvariable=value2 ,width=100)
entree.pack(side = TOP, padx = 5, pady = 5)

BoutonDeco = Button(Mafenetre, text ='Lancer le décodage', command = deco)
BoutonDeco.pack(side = TOP, padx = 5, pady = 15)

result = StringVar()
result.set("")
Label1 = Label(Mafenetre, textvariable = result)
Label1.pack(side = TOP, padx = 5, pady = 5)

BoutonCLN = Button(Mafenetre, text ='CLN', command = cln)
BoutonCLN.pack(side = TOP, padx = 5, pady = 15)
#Texte = StringVar()

## Création d'un widget Label (texte 'Résultat -> x')
#LabelResultat = Label(Mafenetre, textvariable = Texte, fg ='red', bg ='white')
#LabelResultat.pack(side = LEFT, padx = 5, pady = 5)

Mafenetre.mainloop()
