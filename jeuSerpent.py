#-*- encoding: utf-8 -*-


#-------------------------------------------------------------#
#   Projet Python - 2020                                    #
#                                                         #
#   Jeu Serpent sur interface grafique                   #
#                                                        #
#   Auteur : Donatien Dinyad Yeto                         #
#   Version : 1.0                                           #
#--------------------------------------------------------------#



try :
	from Tkinter import *
	import Tkinter as Tk
except :
	from tkinter import *
	import tkinter as Tk
	
import random
from math import fabs
import pickle




class Point:
	"""
	Un point 
	p : le point
	x et y ses coordonnées

	"""
	def __init__(self,p,x,y):
		self.p = p
		self.x = x
		self.y = y
		self.next = None


class Liste:
	"""Liste de points répresentant le serpent"""
	def __init__(self):
		self.tete = None
		self.queu = None
		self.t=0


	def insert(self,c):
		p = m.create_oval(0, 0, 10, 10, fill='yellow')
		#q = m.create_oval(0, 0, 12, 12, fill='maroon')
		if self.t == 0:
			el= Point(p,100,50)
			self.tete=el
			self.queu=el
			self.t=1

		else:
			if c=="r":
				el=Point(p,self.queu.x-10,self.queu.y)
				el.next=self.queu
				self.queu=el
			elif c=="l":
				el=Point(p,self.queu.x+10,self.queu.y)
				el.next=self.queu
				self.queu=el
			elif c=="t":
				el=Point(p,self.queu.x,self.queu.y+10)
				el.next=self.queu
				self.queu=el
			elif c=="b":
				el=Point(p,self.queu.x,self.queu.y-10)
				el.next=self.queu
				self.queu=el

	def aff(self):
		el=self.queu
		while el:
			m.coords(el.p,el.x,el.y,el.x+10,el.y+10)
			el=el.next
		ecran.after(50,self.aff)



		
		

def r():
	global L
	L.tete.x=L.tete.x+10
		
		

def l():
	global L
	L.tete.x=L.tete.x-10


def t():
	global L
	L.tete.y=L.tete.y-10

def b():
	global L
	L.tete.y=L.tete.y+10 

def inserte(c):
	global L
	L.insert(c)
	L.aff()

def cycle():
	global L
	el=L.queu
	while el.next:
		el.x=el.next.x
		el.y=el.next.y
		el=el.next

def type():
	global L
	if L.queu.x == L.queu.next.x and L.queu.y > L.queu.next.y :
		return "t"
	if L.queu.x == L.queu.next.x and L.queu.y < L.queu.next.y :
		return "b"
	if L.queu.y == L.queu.next.y and L.queu.x > L.queu.next.x :
		return "l"
	if L.queu.y == L.queu.next.y and L.queu.x < L.queu.next.x :
		return "r"
	

def get():
	global Aget, L,ax,ay,bx,by,v,score,sc,Bonus
	if (L.tete.x == ax and L.tete.y == ay ) or (fabs(L.tete.x-bx) <= 10 and fabs(L.tete.y -by)<=10) :
		typ=random.randrange(0,10)

		if (L.tete.x == ax and L.tete.y == ay ):
			sc=str(int(sc)+10)
		else:
			sc=str(int(sc)+Bonus)

		# Générer position alétoire du pion
		if typ==9:
			Bonus=1000
			bx=random.randrange(20, 480, 20)
			by=random.randrange(20, 480, 20)
			ax=-20
			ay=-20
		else:
			ax=random.randrange(10, 490, 10)
			ay=random.randrange(10, 490, 10)
			bx=-20
			by=-20

		
		score.config(text="Score : "+sc)
		r=type()
		L.insert(r)
		m.coords(Aget,ax,ay,ax+10,ay+10)
		m.coords(bonus,bx,by,bx+20,by+20)

def egaux():
	global L
	e=L.queu
	while e.next :
		if e.x==L.tete.x and e.y==L.tete.y:
			return True
		e=e.next
	return False

def perdre():
	global L ,continu,per

	if continu and (L.tete.x >= 490 or L.tete.x <= 0 or L.tete.y >= 490 or L.tete.y <= 0 or egaux()):
		continu=False
		per.config(text="Vous avez perdu !!")
		#insertScore()
		#i=getScore()
		#print(i)
		

def deplace():
	global sens,continu,Niveau
	if continu:
		cycle()
		if sens == "r":
			r()
		elif sens == "l":
			l()
		elif sens == "b":
			b()
		elif sens == "t":
			t()
	
		get()
		perdre()
	ecran.after(Niveau,deplace)
def init():
	global L,sens,sc
	sens="r"
	L=Liste()
	L.insert("r")
	L.insert("r")
	sc="00"
	score.config(text="Score : "+sc)
	per.config(text="")
	continu=False
	L.aff()

def replay():
	global v,L,continu,per
	e=L.queu
	while e:
		e.x=-100
		e.y=-100
		e=e.next
	L.aff()
	init()
	
	
	
def start():
	global continu
	continu=True
	sc="00"
def pause():
	global continu
	continu=False

def play():
	global continu
	continu=True
	sc='00'

def niveau(n):
	global Niveau
	Niveau=n

def incre():
	global temp,Bonus
	if temp < 60:
		temp=temp+1
	ww=(400*temp)/60
	nw=400-ww
	p=(100*nw)/400
	Bonus=(1000*p)/100

	nbar.config(width=nw)
	wbar.config(width=ww)
	bn.config(text="Bonus : "+str(Bonus))
	pg.config(text=str(p)+"%")
	ecran.after(200,incre)

def saveScore(scores):
	with open('scores.txt', 'wb') as fichier:
		mon_pickler = pickle.Pickler(fichier)
		mon_pickler.dump(scores)
def getScore():
	try :
		with open('scores.txt', 'rb') as fichier:
			mon_depickler = pickle.Unpickler(fichier)
			score_recupere = mon_depickler.load()
		return score_recupere
	except:
		return None

def insertScore():
	global sc
	score=getScore()
	if score["J1"] < int(sc):
		score["J5"]=score["J4"]
		score["J4"]=score["J3"]
		score["J3"]=score["J2"]
		score["J2"]=score["J1"]
		score["J1"]=int(sc)

	elif score["J2"] < int(sc):
		score["J5"]=score["J4"]
		score["J4"]=score["J3"]
		score["J3"]=score["J2"]
		score["J2"]=int(sc) 

	elif score["J3"] < int(sc):
		score["J5"]=score["J4"]
		score["J4"]=score["J3"]
		score["J3"]=int(sc)

	elif score["J4"] < int(sc):
		score["J5"]=score["J4"]
		score["J4"]=int(sc)

	elif score["J5"] < int(sc):
		score["J5"]=int(sc) 
	saveScore(score)

def evt(evt):
	global sens
	if evt.keysym == "Right" and sens!= "l":
		#inserte("r")
		sens="r"
	elif evt.keysym == "Left" and sens!="r":
		#inserte("l")
		sens="l"
	elif evt.keysym == "Up" and sens!="b":
		#inserte("t")
		sens="t"
	elif evt.keysym == "Down" and sens!= "t":
		#inserte("b")
		sens="b"
	elif evt.keysym == "p":
		pause()
	elif evt.keysym == "o":
		play()
		
	
	#m.coords(point,x,y,x+10,y+10)

ecran=Tk.Tk()
ecran.title("MAP")
ecran.geometry("500x600")

x,y=0,0
ax=random.randrange(10, 490, 10)
ay=random.randrange(10, 490, 10)
bx=-20
by=-20

sens = "r"
sc = "00"
Niveau =100

continu=False
temp=0
Bonus=1000
d={
	"J1":0,
	"J2":0,
	"J3":0,
	"J4":0,
	"J5":0
}


map1=Frame(ecran)
map1.pack(side=LEFT)

per=Label(map1,text="")
per.pack(side=TOP)
score=Label(map1,text="Score : "+sc)
score.pack(side=TOP)



menubar = Menu(ecran)
ecran.config(menu=menubar)
menubar.add_command(label ="Commencer",command=start)
menubar.add_command(label ="Pause",command=pause)
menubar.add_command(label ="Play",command=play)
menubar.add_command(label ="Rejouer",command=replay)


niv= Menu(menubar, tearoff=0)
niv.add_command(label ="Très facile",command=lambda arg=500 : niveau(arg))
niv.add_command(label ="Facile",command=lambda arg=200 : niveau(arg))
niv.add_separator()
niv.add_command(label ="Moyen",command=lambda arg= 100 : niveau(arg))
niv.add_separator()
niv.add_command(label ="Difficile",command=lambda arg=50 : niveau(arg))
niv.add_command(label ="Très difficile",command=lambda arg= 20: niveau(arg))

menubar.add_cascade(label="Niveau", menu=niv)


m=Canvas(map1,width=500,height=500,bg="blue")
m.pack()
Aget = m.create_oval(ax, ay, ax+10, ay+10, fill='green')
bonus = m.create_oval(bx,by,bx+20,by+20,fill="aqua")
asc=getScore()
if(asc):
	aa="Joueur 1 : "+str(asc["J1"])+"\n"+"Joueur 2 : "+str(asc["J2"])+"\n"+"Joueur 3 : "+str(asc["J3"])+"\n"+"Joueur 4 : "+str(asc["J4"])+"\n"+"Joueur 5 : "+str(asc["J5"])+"\n"
else:
	aa=""
#afsc=Label(map1,text=aa)
#afsc.pack()
#fbar=Frame(map1)
#nbar=Canvas(fbar,width=300,height=10,bg="green")
#wbar=Canvas(fbar,width=100,height=10,bg="black")
#bn=Label(map1,text=str(Bonus))
#pg=Label(map1,text="00%")
#wbar.pack(side=LEFT)
#nbar.pack(side=LEFT)
#fbar.pack(side=	TOP)
#pg.pack(side=TOP)
#bn.pack(side=TOP)


L=Liste()
L.insert("r")
L.insert("r")
deplace()
get()
#incre()

#point = m.create_oval(x, y, x+10, y+10, fill='yellow')

L.aff()
ecran.bind("<Key>",evt)
ecran.mainloop()