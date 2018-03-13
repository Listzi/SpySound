#spysound
#chaine de chr binaires extraite du fichier son
decoded_b= input("deco :")
#decodage entete
nbr_chr=int(decoded_b[0:32],2)
#dernier bit/ rang de travail
last_bit=32
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
print(txt_fin)
