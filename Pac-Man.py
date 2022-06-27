import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ])
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  
carteGum = []
carteGhost =[]
score = 0
tempsSuperGum = 0
PacManColor = "yellow"
# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM
            
GUM = PlacementsGUM()   

PacManPos = [5,5]

directions=[(-1,0),(1,0),(0,-1),(0,1)]


Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink",  directions[1] ])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange",directions[2] ])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan",  directions[3] ])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red",   directions[0] ])         



##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    MainLoop()
    Window.after(500,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message,data1,data2):
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = data1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = data2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
   
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

      
def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] != 1 ): L.append((0,-1))
   if ( TBL[x  ][y+1] != 1 ): L.append((0, 1))
   if ( TBL[x+1][y  ] != 1 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] != 1 ): L.append((-1,0))
   return L
   
def EstCouloir(movePossible):
	if len(movePossible)!=2 : return False
	if movePossible[0][0] == movePossible[1][0] or movePossible[0][1] == movePossible[1][1] :
		return True
	return False

def PacManMove(L):
   dic =dict()
   global tempsSuperGum

   if tempsSuperGum > 1:
      for d in L:
         dic[carteGhost [PacManPos[0] + d[0]] [PacManPos[1] + d[1]]] = d
      indmin = min(dic.keys())
      return dic[indmin]

   if carteGhost[PacManPos[0]][PacManPos[1]]>3:
      for d in L:
         dic[carteGum [PacManPos[0] + d[0]] [PacManPos[1] + d[1]]] = d
      indmin = min(dic.keys())
      return dic[indmin]

   else:
      for d in L:
         dic[carteGhost [PacManPos[0] + d[0]] [PacManPos[1] + d[1]]] = d
      indmin = max(dic.keys())
      return dic[indmin]


def GhostMove(ghost,movePossible,couloir):
   if couloir == True : return ghost[3]
   else :
      move=random.randrange(len(movePossible))
      ghost[3]=movePossible[move]
      return movePossible[move]


def IA():
   
   global PacManPos, Ghosts , PAUSE_FLAG, PacManColor,tempsSuperGum
   CarteDesDistancesGum()
   CarteDesDistancesGhost()

   #deplacement Pacman
   L = PacManPossibleMove()
   choix = PacManMove(L)
   tempsSuperGum -= 1

   PacManPos[0] += choix[0]
   PacManPos[1] += choix[1]
   Colision()
   if PAUSE_FLAG : return
   
   MangePacGums()

   #deplacement Fantome
   for F in Ghosts:
      L = GhostsPossibleMove(F[0],F[1])
      choix = GhostMove(F,L,EstCouloir(L))
      F[0] += choix[0]
      F[1] += choix[1]
   Colision()
   if PAUSE_FLAG : return

   if tempsSuperGum > 1 : PacManColor = "Red"
   else : PacManColor = "yellow"

   CarteDesDistancesGum()
   CarteDesDistancesGhost()


def Colision():
   global PAUSE_FLAG, score, Ghosts
   for F in Ghosts:
      if F[0] == PacManPos[0] and F[1] == PacManPos[1]:
         if tempsSuperGum > 0:
            score += 2000
            Ghosts[Ghosts.index(F)][0] = 9
            Ghosts[Ghosts.index(F)][1] = 5
         else : PAUSE_FLAG = True

def MangePacGums():
   global score,tempsSuperGum,PacManColor

   x = PacManPos[0]
   y = PacManPos[1]
   if (GUM[x,y] == 1):
      GUM[x,y] = 0
      score +=100
      if ([x,y] == [1,1] or [x,y] == [1,9] or [x,y] == [18,1] or [x,y] == [18,9] ):
         tempsSuperGum = 16


def CarteDesDistancesGhost():
   global carteGhost
   global Ghosts
   carteGhost = [[200 for i in range(LARGEUR)] for i in range(HAUTEUR)]
   for x in range(HAUTEUR):
      for y in range(LARGEUR):
         if TBL[y][x] == 1 or TBL[y][x] == 2 :
            carteGhost[x][y] = 1000
         for G in Ghosts:
            if x == G[1] and y == G[0]:
               carteGhost[x][y] = 0
       
   # calcul des distances
   fini=False
   while not fini:
      fini = True
      for i in range(1,10):
         for j in range(1,19):
            if carteGhost[i][j] == 1000 : continue
            if carteGhost[i][j] == 0 : continue 
            else:
               mini = min(carteGhost[i+1][j],carteGhost[i][j+1],carteGhost[i-1][j],carteGhost[i][j-1])
               if not mini+1 == carteGhost[i][j] : 
                  fini = False
                  carteGhost[i][j] = mini+1
   carteGhost=np.transpose(carteGhost)


def CarteDesDistancesGum():
    # Initialisation de la carteGum en fonction des gums restants
    global carteGum
    carteGum = [[200 for i in range(LARGEUR)] for i in range(HAUTEUR)]
    for x in range(HAUTEUR):
        for y in range(LARGEUR):
            if GUM[y][x] == 1:
                carteGum[x][y] = 0
            elif TBL[y][x] == 1 or TBL[y][x] == 2 :
                carteGum[x][y] = 1000
       
    # calcul des distances
    fini=False
    while not fini:
        fini = True
        for i in range(1,10):
            for j in range(1,19):

                if carteGum[i][j] == 1000 : continue
                if carteGum[i][j] == 0 : continue 

                else:
                    mini = min(carteGum[i+1][j],carteGum[i][j+1],carteGum[i-1][j],carteGum[i][j-1])
                    if not mini+1 == carteGum[i][j] : 
                        fini = False
                        carteGum[i][j] = mini+1
    carteGum=np.transpose(carteGum)
 
#  Boucle principale de votre jeu appelée toutes les 500ms

def MainLoop():
  if not PAUSE_FLAG : IA()
  Affiche(PacManColor, message = score, data1=carteGhost, data2=carteGum)  
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()

 
   
   
    
   
   