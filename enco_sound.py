import wave
print("Création d'un fichier audio au format WAV (PCM 8 bits mono 44100)")
Monson = wave.open('T:\isn\Starset2min8bitmono.wav','r') # on reserve un espace memoire et on fixe l'etat du son  
nbCanal = 1  # mono 
nbOctect = 1 # echantillon : 8 bits = 1 octet
frech = 44100 # frequence d'echantillonnage
#   creation du fichier son
bin_finale=""
Liste = []

print("nb d'echantillonage :",Monson.getnframes())

import binascii
plage = 50
for i in range(0,plage):
    Monson.setpos(i)
    temp="{0:08b}".format(int(binascii.hexlify(Monson.readframes(1)),16))
    print(temp)
    Liste.append(temp)# 
print(Liste)
temp2=Liste[0]

# Liste[0]=str(temp2[:6]+bin_finale[n*2:n*2+2])
Liste[0]=str(temp2[:6]+"98")
print(Liste)

Monson.close()
