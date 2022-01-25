# -*- coding: utf-8 -*-

import string
import sys
import os
import math
from tkinter import *
from collections import defaultdict

wd = os.getcwd()

os.chdir(wd)


fra = open("French_train.txt", "r", encoding = "utf-8").read()
spa = open("Spanish_train.txt", "r", encoding = "utf-8").read()
ita = open("Italian_train.txt", "r", encoding = "utf-8").read()
rom = open("Romanian_train.txt", "r", encoding = "utf-8").read()
ger = open("German_train.txt", "r", encoding = "utf-8").read()
eng = open("English_train.txt", "r", encoding = "utf-8").read()
pol = open("Polish_train.txt", "r", encoding = "utf-8").read()

def even_text_split(text,n):
    parts = [text[i:i + n] for i in range(0, len(text), n)]
    return tuple(parts)


fra_set = even_text_split(fra, len(fra)//20)
spa_set = even_text_split(spa, len(spa)//20)
ita_set = even_text_split(ita, len(ita)//20)
rom_set = even_text_split(rom, len(rom)//20)
ger_set = even_text_split(ger, len(ger)//20)
eng_set = even_text_split(eng, len(eng)//20)
pol_set = even_text_split(pol, len(pol)//20)

# langues et corpus associé:
langues = {
           ("Français",fra_set),
           ("Espagnol",spa_set),
           ("Italien",ita_set),
           ("Roumain",rom_set),
           ("Allemand",ger_set),
           ("Anglais",eng_set),
           ("Polonais",pol_set),
           }

#%% 
    
    
def ngrammes(text,n): # renvoie le dictionnaire ngramme:occurrences du texte en argument
  w = text.strip(string.punctuation)
  d = {}
  for i in range(len(w)-n+1):
      try:
          d[w[i:i+n]] += 1
      except KeyError:
          d[w[i:i+n]] = 1
  return d    


def print_dict(d): #Affichage dictionnaire
  for (k,v) in d.items():
    print(k + " " + str(v))
  


def cosimNgrammes(text,corpus_text,n): #Calcule la cosimilarité entre le texte et un corpus (texte, texte du corpus) selon les ngrammes
    dtext = ngrammes(text,n)
    dlang = ngrammes(corpus_text,n)
    c = [k for k in dtext.keys() if k in dlang.keys()]
    top = 0 # v.w
    v = 0 # |v|
    w = 0 # |w|
    for k in c:
        top += dtext[k]*dlang[k]
        v += dtext[k]*dtext[k]
        w += dlang[k]*dlang[k]
    v = math.sqrt(v)
    w = math.sqrt(w)
    try:
        return top/(v*w)
    except:
        return 0
   
#%%

def scoredetect(text): # Affiche le score de chaque langue

    dsim = dict() #dictionnaire[LangueDuTexteDuCorpus] : SimilaritéCosinus
    dres = defaultdict(int) #associe a chaque langue leur score (nb de textes du corpus évalués comme les plus proches du texte à analyser)

    if len(text.split()) < 5:
        coef1g = 30 #poids des 1-grammes
        coef2g = 20 #poids des 2-grammes
        coef3g = 50 #poids des 3-grammes
        
        for i in range(len(fra_set)-1):
            for lang,corpus in langues:
                dsim[lang] = (coef1g*cosimNgrammes(text,corpus[i],1) + coef2g*cosimNgrammes(text,corpus[i],2) + coef3g*cosimNgrammes(text,corpus[i],3))/(coef1g+coef2g+coef3g)
            result = max(dsim, key=(lambda lang:dsim[lang]))
            dres[result] += 1
        
    else : 
        coef1g = 67 
        coef2g = 33 

        for i in range(len(fra_set)-1):
            for lang,corpus in langues:
                dsim[lang] = (coef1g*cosimNgrammes(text,corpus[i],1) + coef2g*cosimNgrammes(text,corpus[i],2))/(coef1g+coef2g)
            result = max(dsim, key=(lambda lang:dsim[lang]))
            dres[result] += 1
            
    return dres

def fiabilite(num):
    if num > 15 :
        return "élevée"
    elif num >= 10 :
        return "correcte"
    else :
        return "faible"
    
def detect(d):
    found = max(d, key=(lambda lang:d[lang]))
    return("Après évaluation, ce texte est problement en " + found + " (Fiabilité : " + fiabilite(d[found]) + ").")


#%%
text = ""
if len(sys.argv) == 1:
    print("Détecteur de langues par Arthur Jean-Joseph :")
    print("Donnez la phrase à évaluer en argument, ou bien utilisez l'option -f pour donner un fichier texte.")
    print("Vous pouvez rajouter l'option -d pour voir le détail de l'évaluation.")
    print("-> exemples : Ldetect.py -f phrase.txt")
    print("              Ldetect.py -d exemple d'execution du programme")
    print("              Ldetect.py -df évaluationDetaillée.txt")
    print(" /!\ Si vous êtes sur bash, la phrase donnée en argument doit être entre guillemets si elle contient des caractères non-acceptés.")
    print(" /!\ Les résultats ne sont pas toujours optimaux pour des énoncés très courts.")
elif sys.argv[1] == "--help":
    print("Détecteur de langues par Mathilde Alcaraz et Arthur Jean-Joseph:")
    print("Donnez la phrase à évaluer en argument, ou bien utilisez l'option -f pour donner un fichier texte.")
    print("Vous pouvez rajouter l'option -d pour voir le détail de l'évaluation.")
    print("-> exemples : Ldetect.py -f phrase.txt")
    print("->            Ldetect.py -d exemple d'execution du programme")
    print("->            Ldetect.py -df évaluationDetaillée.txt")
    print(" /!\ Si vous êtes sur bash, la phrase donnée en argument doit être entre guillemets si elle contient des caractères non-acceptés.")
    print(" /!\ Les résultats ne sont pas toujours optimaux pour des énoncés très courts.")
elif sys.argv[1] == "-f": #evaluation avec un fichier
    print("évaluation en cours...")
    try:
        text = getText(sys.argv[2])
    except IndexError:
        print("Argument manquant !")
    if text != "":
        detect(scoredetect(text))
    else:
        print("Erreur : aucun texte à analyser")
elif sys.argv[1] == "-d": #evaluation detaillee
    print("évaluation en cours...")
    for w in sys.argv[2:]:
        text += w + " "
    if text != "":
        d = scoredetect(text)
        print_dict(d)
        detect(d)
    else:
        print("Erreur : aucun texte à analyser")
elif sys.argv[1] == "-df" or sys.argv[1] == "-fd": #evaluation avec un fichier detaillee
    print("évaluation en cours...")
    try:
        text = getText(sys.argv[2])
    except IndexError:
        print("Argument manquant !")
    if text != "":
        d = scoredetect(text)
        print_dict(d)
        detect(d)
    else:
        print("Erreur : aucun texte à analyser")
else: #evaluation normale
    print("évaluation en cours...")
    for w in sys.argv[1:]:
        text += w + " "
    if text != "":
        detect(scoredetect(text))
    else:
       print("Erreur : aucun texte à analyser")     
