import wave
import math
import tkinter
# https://pythonspot.com/tk-file-dialogs/
# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
# https://stackoverflow.com/questions/2905965/creating-threads-in-python
# http://fsincere.free.fr/isn/python/cours_python_ch9.php
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.ttk import Progressbar
from threading import Thread
from tkinter import *
import binascii

global intxt
def trd_enco():
    #on récupère le texte à encoder
    intxt=(txt.get(1.0,END))
    #créé un nouveau thread pour exécuter la fonction enco
    thread1 = Thread(target = enco, args=())
    thread1.start()
    # enco()
    
def enco():

 #fichier à encoder
 messagebox.showinfo("Select initial file", "Select initial file")
 Mafenetre.filename =  filedialog.askopenfilename(initialdir = "T:/",title = "Select file to encode",filetypes = (("WAV files","*.wav"),("all files","*.*")))
 fichierRD=Mafenetre.filename
 print(fichierRD)
 #fichier encodé
 messagebox.showinfo("Select final file", "Select output file")
 Mafenetre.filename2=filedialog.asksaveasfilename(initialfile='FichierEncodé',initialdir = "T:/",title = "Target for encoded message",defaultextension=".wav",filetypes=(("WAV files","*.wav"),("all files","*.*")))
 fichierRW=Mafenetre.filename2
 print(fichierRW)

 # on reserve un espace memoire et on fixe l'etat du fichier son
 Monson = wave.open(fichierRD,'rb') 
 Mysound = wave.open(fichierRW,'wb')
 
 #txt a enco
 intxt=(txt.get(1.0,END))
 #pour enlever les retours à la ligne .replace("\n"," ")
 
 #chaine de chr binaires a enco dans le fichier son
 bin_finale=""
 #longueur du msg(en chr)
 lenght=int(len(intxt))
 #entete(nbr de chr)
 bin_finale="{0:024b}".format(lenght)
 #message txt vers bin
 for x in range(lenght):
    #valeur decimal du chr
    dec_val=0
    #nbr d'octet(s) pour enco valeur dec du chr en bin
    Info=""
    #obtention valeur dec du chr selectionne
    dec_val=ord(intxt[x])
    #si valeur dec du chr encodable sur 1 oct :
    if dec_val<=255:
        Info='00'
        #"{0:08b}".format(dec_val) permet de rajouter des zeros pour avoir 8 bits
        bin_finale=bin_finale+Info+"{0:08b}".format(dec_val)
    #si valeur dec du chr encodable sur 2 oct :
    if dec_val>255 and dec_val<=65535:
        Info='01'
        #"{0:016b}".format(dec_val) permet de rajouter des zeros pour avoir 16 bits
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
 bin_finale=str("{0:032b}".format(len(bin_finale)))+bin_finale
 #nombre d'encodages nécessaires pour encoder bin_finale, arrondi au supérieur pour ne pas perdre de bit
 nbr_enco=int(math.ceil(len(bin_finale)/2))

 #nombre d'ech du fichier son d'org
 nbEchantillon = Monson.getnframes()
 if nbEchantillon<nbr_enco*2:
    messagebox.showinfo('Alerte', 'Attention texte trop long !!')
    return
    
 nbCanal = 1    # mono
 nbOctet = 1    # taille d'un échantillon : 1 octet = 8 bits
 fech = 44100   # fréquence d'échantillonnage
 
 
 parametres = (nbCanal,nbOctet,fech,nbEchantillon,'NONE','not compressed')
 Mysound.setparams(parametres)    # création de l'en-tête

 for i in range(0,nbr_enco):
     Monson.setpos(i)
     #on lit la valeur de l'échantillon du fichier d'origine 
     temp="{0:08b}".format(int(binascii.hexlify(Monson.readframes(1)),16))
     
     #on écrit cette donnée dans le fichier final(on créé la donnée à écrire dans le fichier final)
     Mysound.writeframes(wave.struct.pack('B',int(temp[:6]+bin_finale[i*2:i*2+2],2)))
     
     bar.step((1/nbEchantillon)*100)

# même chose que le "if" précédant mais sans modifier l'échantillon
#ce "if" ne fait que compléter la fin du fichier
 for i in range(nbr_enco,nbEchantillon): 
     Monson.setpos(i)
     temp=int(binascii.hexlify(Monson.readframes(1)),16)
     Audio = wave.struct.pack('B',temp)
     Mysound.writeframes(Audio)
     #valeur=poids du fichier, permet de connaître l'avancement mais ralentit l'encodage
     #klm="b"+str(i)
     #print(klm)
     bar.step((1/nbEchantillon)*100)

 messagebox.showinfo("Warning", "Encode complete")
 
 Monson.close()
 Mysound.close()


def trd_deco():
    #créé un nouveau thread pour exécuter la fonction deco
    thread2 = Thread(target = deco, args=())
    thread2.start()

    # enco()
def deco():
    #sélection du fichier à décoder
    messagebox.showinfo("Select encoded file", "Select encoded file")
    Mafenetre.filename =  filedialog.askopenfilename(initialdir = "T:/",title = "Select file to decode",filetypes = (("WAV files","*.wav"),("all files","*.*")))
    fichierRD=Mafenetre.filename
    Monson = wave.open(fichierRD,'rb')
    nbr_bits=""
    decoded_b=""

    #decodage header
    for x in range(0,16): #  !!!!!! 32 bits oui MAIS 2 BITS PAR ECHANTILLON !!!!!
        Monson.setpos(x)
        temp="{0:08b}".format(int(binascii.hexlify(Monson.readframes(1)),16))
        nbr_bits=nbr_bits+temp[6:]

    nbr_deco = math.ceil(int(nbr_bits,2)/2)

    #décodage message
    for i in range(16,nbr_deco+16):
        Monson.setpos(i)
        temp="{0:08b}".format(int(binascii.hexlify(Monson.readframes(1)),16))
        decoded_b=decoded_b+temp[6:]
        bar.step((1/nbr_deco+16)*100)

    #conversion binaire+code vers txt
    Monson.close()    
    nbr_chr=int(decoded_b[0:24],2)
    last_bit=24
    txt_fin=""
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
    
    #affiche le message décodé
    txt2.delete(1.0,END)
    txt2.insert(INSERT,txt_fin)

#pour effacer le résultat
def cln():
    txt2.delete(1.0,END)

# Création de la fenêtre principale
Mafenetre = Tk()

Mafenetre.title('Spysound')
Mafenetre.resizable(width=True, height=False)
#champ de texte à encoder
txt = scrolledtext.ScrolledText(Mafenetre,height=8)
txt.pack(side = TOP,fill=X,expand=YES, padx = 5, pady = 5)
txt.insert(INSERT,"Que faut-il encoder ?")

# Création d'un boutton
BoutonEnco = Button(Mafenetre, text ='Lancer l\'encodage', command = trd_enco)
BoutonEnco.pack(side = TOP,expand=YES, padx = 5, pady = 5)

bar = Progressbar(Mafenetre, length=200,mode='determinate', value = 0)
bar.pack(side = TOP,expand=YES, padx = 5, pady = 5)

#boutton de décodage
BoutonDeco = Button(Mafenetre, text ='Lancer un décodage', command = trd_deco)
BoutonDeco.pack(side = TOP,expand=YES,  padx = 5, pady = 15)

#champs de texte pour le résultat
txt2 = scrolledtext.ScrolledText(Mafenetre,height=8)
txt2.pack(side = TOP,fill=X,expand=YES,  padx = 5, pady = 5)
txt2.insert(INSERT,"hello world, waiting for something")

#boutton pour effacer les résultats
BoutonCL = Button(Mafenetre, text ='CLN', command = cln)
BoutonCL.pack(side = TOP,padx = 2, pady = 5)
Mafenetre.mainloop()
