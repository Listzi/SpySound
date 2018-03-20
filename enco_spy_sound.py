# SpySound
#txt a enco
intxt= input("txt_utf-8 :")
#chaine de chr binaires a enco dans le fichier son
bin_finale=""
#longueur du msg
lenght=len(intxt)
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
nbr_bits=len(bin_finale)
#ajout nombre de bits à enco
bin_finale=str("{0:032b}".format(len(bin_finale)+32))+bin_finale
print(bin_finale)
