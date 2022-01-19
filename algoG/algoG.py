import random
import numpy as np
import matplotlib.pyplot as plt

class combinaison:
    def __init__(self,a=None,b=None,c=None):
        if a==None:
            self.a=round(random.random(),2)
            self.b=random.randint(1, 20)
            self.c=random.randint(1, 20)
        else:
            self.a=a
            self.b=b
            self.c=c

    def __str__(self):
        text=""
        text=str(self.a)+","+str(self.b)+","+str(self.c)
        return(text)

    def fitness(self,x,y):
        self.dist=0
        for i in range(len(x)):
            self.dist=self.dist+abs(y[i]-weierstrass(x[i],self.a,self.b,self.c))
        return self.dist

def weierstrass(i,a,b,c):
    total=0
    for n in range(0,c+1):
        total=total+np.cos(np.pi*float(i)*b**n)*a**n
    return total

def create_rand_pop(count):
    liste=[]
    for i in range(count):
        liste.append(combinaison())
    return liste

def evaluate(pop,x,y):
    return sorted(pop, key=lambda z : z.fitness(x,y))

def selection(pop,hcount,lcount):
    pop2=[]
    for i in range(hcount):
        pop2.append(pop[i])
    for i in range(lcount):
        pop2.append(pop[-i-1])
        # lcount=len(i.val)-lcount
        # if lcount<hcount:
        #     print("Borne mal défini")
        #     lcount,hcount=hcount,lcount
        # mid=i.val[hcount:lcount]
        # mid=random.sample(mid,lcount-hcount)
        # final=i.val[0:hcount]+mid+i.val[lcount:len(i.val)]
        # pop2.append(final)
    return pop2

def croisement(ind1,ind2):
    ind3=combinaison()
    if random.randint(0, 1)*True:
        ind3.a=ind1.a
        ind3.b=ind1.b
        ind3.c=ind2.c
    else:
        ind3.a=ind2.a
        ind3.b=ind1.b
        ind3.c=ind1.c
    return ind3

def mutation(ind):
    value=0.01
    r=random.choice(["a", "b", "c","c"])
    s=random.choice(["plus","moins"])
    if r=="a":
        if s=="plus":
            ind.a=ind.a+value
        else:
            ind.a=ind.a-value
    if r=="b":
        if s=="plus":
            ind.b=ind.b+1
        else:
            ind.b=ind.b-1
    if r=="c":
        if s=="plus":
            ind.c=ind.c+1
        else:
            ind.c=ind.c-1
    return ind

def algoloopSimple(x,y):
    memoire=0
    pop=create_rand_pop(40)
    solutiontrouvee=False
    nbiteration=0
    while not solutiontrouvee:
        #print("iteration:" ,nbiteration)
        nbiteration+=1
        evaluation=evaluate(pop,x,y)
        if evaluation[0].fitness(x,y)!=memoire:
            memoire=evaluation[0].fitness(x,y)
            print(str(round(memoire,2))+":"+str(evaluation[0]))
        #print(evaluation[0].fitness(x,y))
        if evaluation[0].fitness(x,y)<0.17 or nbiteration>99 and evaluation[0].fitness(x,y)<0.2:
            solutiontrouvee=True
        else:
            select=selection(evaluation,9,5)
            croises=[]
            for i in range(len(list(select))-1):
                croises.append(croisement(select[i],select[i+1]))
            mutes=[]
            for i in select:
                mutes.append(i)
            newalea=create_rand_pop(5)
            pop=select[:]+croises[:]+mutes[:]+newalea[:]
    print("\nFitness:",evaluation[0].fitness(x,y))
    print("Nombre Itération:",nbiteration)
    return evaluation[0]

def getconfig(file):
    conf = open(file, "r")
    newligne=conf.readline()
    ligne = ""
    while newligne != "":
        newligne=conf.readline()
        ligne = ligne+newligne
    conf.close()
    return ligne

def convert(text):
    x=[]
    y=[]
    for c in text.split("\n"):
        x.append(c.split(";")[0])
        y.append(float(c.split(";")[1]))
    return x,y

#0<a<1
#1<b<20
#1<c<20

x,y=convert(getconfig(r'C:\Users\alan7\Desktop\temperature_sample_calibrate2.csv'))
# y2=[]
# for i in x:
#     y2.append(weierstrass(float(i),a,b,c))
# plt.plot(x,y)
# plt.plot(x,y2)
# plt.show()
print(algoloopSimple(x,y))
a=0.14
b=19
c=5
print(str(a)+","+str(b)+","+str(c))