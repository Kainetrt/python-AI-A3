#!python

import math
import matplotlib.pyplot as plt

k=3
learning="data.csv"
inconnu="finalTest.csv"
output=r"C:\Users\alan7\Desktop\resultat.txt"
mode=["comparaison","prediction","ktest"][1]

def exportresult(resultat,nomfichier="resultat.txt"):
    f=open(nomfichier,"w")
    for i in resultat:
        f.write(i+"\n")
    f.close()

def getconfig(file):
    conf = open(file, "r")
    newligne=conf.readline()
    ligne = ""
    while newligne != "":
        newligne=conf.readline()
        ligne = ligne+newligne
    conf.close()
    return ligne

def knn(data,point,k):
    liste_distance=[]
    for index, sample in enumerate(data):
        liste_distance.append((distance(sample,point),index))
    liste_distance=sorted(liste_distance)
    liste_indice=[index for distance,index in liste_distance[:k]]
    return liste_indice

def distance(a,b):
    d=0
    for i in range(len(a)):
        d=d+(b[i]-a[i])**2
    return d**(1/2)

def loadconfig(nomfichier:str,typed=""):
    dataset=getconfig(r"C:\Users\alan7\Documents\Cours\IA\knn\{}".format(nomfichier))
    #dataset=dataset+getconfig(r"C:\Users\alan7\Documents\Cours\IA\knn\preTest.csv")
    data=[]
    for c in dataset.split("\n"):
        if c!="" and c!=" ":
            data.append(c)
    label=[]
    label2=[]
    liste_points=[]
    if typed=="learning":
        for c in data:
            d=c.split(",")
            label.append(d[6])
            liste_points.append([float(d[0]),float(d[1]),float(d[2]),float(d[3]),float(d[4]),float(d[5])])
        return label,liste_points
    elif typed=="comparaison":
        for c in data:
            d=c.split(",")
            label2.append(d[6])
            liste_points.append([float(d[0]),float(d[1]),float(d[2]),float(d[3]),float(d[4]),float(d[5])])
        return label2,liste_points
    else:
        for c in data:
            d=c.split(",")
            liste_points.append([float(d[0]),float(d[1]),float(d[2]),float(d[3]),float(d[4]),float(d[5])])
        return liste_points

def percent(resultat,label):
    if len(resultat)!=len(label):
        return print("Mauvaise taille de résultat pour faire une estimation du % de réussite")
    total=len(label)
    cpt=0
    for i in range(total):
        if resultat[i]==label[i]:
            cpt=cpt+1
    return cpt/total

def verif(k):
    if k%2!=1:
        print("k doit être impair")
        print(exit)
        exit()

def calculresultat(data_inconnu,points,k,label):
    resultat=[]
    for data in data_inconnu:
        index_plus_proche=knn(points,data,k)
        print(index_plus_proche)

        maxi=0
        nommax=""
        cpt=0
        for i in label:
            no=i
            if cpt>maxi:
                maxi=cpt
                nommax=no
            cpt=0
            for j in index_plus_proche:
                if i==label[j]:
                    cpt=cpt+1
        resultat.append(nommax)
    print(resultat)
    return resultat

def ktest(k:int):
    label2,data_inconnu=loadconfig(inconnu,"comparaison")
    resultat=calculresultat(data_inconnu,points,k,label)
    exportresult(resultat,output)
    pourcent=percent(resultat,label2)
    return pourcent


label,points=loadconfig(learning,"learning")
verif(k)

if mode=="comparaison":
    label2,data_inconnu=loadconfig(inconnu,"comparaison")
    resultat=calculresultat(data_inconnu,points,k,label)
    exportresult(resultat,output)
    pourcent=percent(resultat,label2)
    print(pourcent)

if mode=="prediction":
    data_inconnu=loadconfig(inconnu)
    resultat=calculresultat(data_inconnu,points,k,label)
    exportresult(resultat,output)

if mode=="ktest":
    display=[]
    for k in range(1,101,2):
        print(k)
        display.append(ktest(k))
    k=[x for x in range(1,101,2)]
    plt.plot(k,display)
    plt.ylabel('précision')
    plt.xlabel('k')
    plt.show()




# for i in index_plus_proche:
#     print(label[i])

# noms={}
# nom=set(noms)
# for i in index_plus_proche:
#     nom.add(label[i])

#print(maxi,nommax)

#Question 1: la distance
#Question 2: Afficher la moyenne des points les plus proches au lieu du label majoritaire


