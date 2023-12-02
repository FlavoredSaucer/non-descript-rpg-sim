import random as rng
from re import split
from time import sleep

class Die:
	def __init__(self, nos):
		self.NumberOfSides = nos
		self.Roll = 1
		self.TimesRolled = 0
		self.PreviousRoll = 0

	def DoRoll(self):
		self.PreviousRoll = self.Roll
		self.TimesRolled += 1
		self.Roll = rng.randrange(self.NumberOfSides)+1
		return self.Roll

class PlayerGeneric:
	IsAlive = False
	LastDamage = 0

	Name = "PlayerGeneric"
	IFF = 0
	d20 = Die(20)
	InitiativePlus = 0
	Team = None

	AC = 1
	HP = 1
	Initiative=0
	Opponent = None

	PlusToHit = 0
	Attack = "0d0+2"
	AtkDice = []
	AtkPlus = 0

	Phrases = [
		"Test 1",
		"Test 2",
		"Test 3",
	]


	def __init__(self, NameSuffix = ""):
		self.d20 = Die(20)
		self.Name += NameSuffix
		self.AtkDice = []
		self.IsAlive = True
		self.LastDamage = 0
		self.Opponent = None
		asd = split('d|\+',self.Attack)
		for i in range(int(asd[0])*2):
			self.AtkDice.append(Die(int(asd[1])))
		if len(asd) > 2:
			self.AtkPlus = int(asd[2])
		else:
			self.AtkPlus = 0

	def RollInitiative(self):
		self.Initiative = self.d20.DoRoll()+self.InitiativePlus
	
	def DoAttack(self, Opponent):
		if self.d20.DoRoll()+self.PlusToHit >= Opponent.AC:
			self.DealDamage(Opponent, self.d20.Roll == 20)

	def RollDamage(self, IsCrit = False):
		Rolls = len(self.AtkDice)
		if not IsCrit:
			Rolls /= 2
		Rolls = int(Rolls)
		Damage = self.AtkPlus		
		for i in range(Rolls):
			Damage += self.AtkDice[i].DoRoll()
		self.LastDamage = Damage
		return Damage

	def DealDamage(self, Opponent, IsCrit = False):
		Damage = self.RollDamage(IsCrit)
		Opponent.TakeDamage(Damage)

	def TakeDamage(self, Damage):
		self.HP -= Damage
		if self.HP <= 0:
			self.IsAlive = False

	def CommentateGenericAttack(self):
		if self.Opponent is None:
			print(self.Name+" cannot find a target!");sleep(slprshort/3)
			return
		if self.Opponent.HP <= 0:
			self.FindOpponent()
			if self.Opponent is None: return
		self.DoAttack(self.Opponent)
		if self.d20.Roll+self.PlusToHit >= self.Opponent.AC:
			if self.d20.Roll == 20:
				print(self.Name+" rolls a "+str(self.d20.Roll+self.PlusToHit)+" (Nat 20) and CRITS! ",end="")
			else:
				print(self.Name+" rolls a "+str(self.d20.Roll+self.PlusToHit)+" and hits! ",end="")
			print("Dealing "+str(self.LastDamage)+" points to "+self.Opponent.Name+". ("+str(self.Opponent.HP)+" HP Left.)"); sleep(slpshort)
		else:
			print(self.Name+" misses "+self.Opponent.Name+" with a "+str(self.d20.Roll+self.PlusToHit)+"..."); sleep(slpshort/2)


	def Speak(self):
		print(self.Name+" says: "+rng.choice(self.Phrases))
	
	def FindOpponent(self,Silent = True):
		EnemyTeams = [x for x in Teams if x != self.Team and x.IsAlive]
		if len(EnemyTeams) == 0:
			self.Opponent = None
			return
		self.Opponent = rng.choice(list(EnemyTeams)).ReturnRandomTeammate()
		if not Silent:
			print(self.Name+"'s opponent is "+self.Opponent.Name+"!")


class PlayerArwin(PlayerGeneric):
	Name="Arwin"
	IFF = 1
	AC=16
	HP=34
	InitiativePlus = 1
	PlusToHit=5
	Attack="2d6+3"

class PlayerPrincess(PlayerGeneric):
	Name="Princess Ophelia"
	IFF = 1
	AC=18
	HP=40
	PlusToHit=3
	Attack="1d8+1"

class PlayerAjay(PlayerGeneric):
	Name="Ajay Gale"
	IFF = 1
	AC=11
	HP=20
	InitiativePlus=4
	PlusToHit=5
	Attack="3d8"

class PlayerTaz(PlayerGeneric):
	Name="Taaz"
	IFF = 1
	AC=19
	HP=28
	InitiativePlus=1
	PlusToHit=5
	Attack="1d6+3"

class PlayerMartin(PlayerGeneric):
	Name="Martin Magfiel"
	IFF = 1
	AC=15
	HP=35
	InitiativePlus = 2
	PlusToHit=6
	Attack="1d12+4"

class EnemyRat1(PlayerGeneric):
	Name="Rat Swarm"
	IFF = 2
	AC=10
	HP=24
	PlusToHit=2
	Attack="2d6"

class EnemyRat2(PlayerGeneric):
	Name="1000 Gay Rats"
	IFF = 2
	AC=5
	HP=500
	InitiativePlus=2
	PlusToHit=0
	Attack="3d10"

class EnemyRat3(PlayerGeneric):
	Name="Giant Rat"
	IFF = 2
	AC=12
	HP=7
	InitiativePlus=0
	PlusToHit=4
	Attack="1d4+2"

class EnemyBeholder(PlayerGeneric):
	Name="Beholder"
	IFF = 3
	AC=18
	HP=180
	PlusToHit=5
	Attack="4d6"

class EnemyWTF(PlayerGeneric):
	Name="Beholder"
	IFF = 3
	AC=10
	HP=1
	PlusToHit=5
	Attack="4d6"

class TeamGeneric():
	Name = "Generic Team"
	TeamIFF = 0
	IsAlive = False
	def __init__(self, Name, TeamIFF):
		self.IsAlive = True
		self.Name = Name
		self.TeamIFF = TeamIFF
		self.Teammates = []
	
	def AddTeammate(self,Teammate):
		self.Teammates.append(Teammate)
		Teammate.Team = self
	
	def Update(self):
		self.IsAlive = any(p.IsAlive for p in self.Teammates)
	
	def ReturnRandomTeammate(self):
		Teammate = [x for x in self.Teammates if x.IsAlive]
		if len(Teammate) == 0:
			return None
		return rng.choice(Teammate)


slplong = 1
slpshort = slplong/2
slprshort = slplong/10

# Main Game
Turns = 0 

# Players = [
# 	PlayerArwin(),
# 	PlayerTaz(),
# 	PlayerMartin(),
# 	PlayerAjay(),
	
# 	EnemyBeholder(),
# ]
Players = []
for i in range(6):
	Players.append(PlayerArwin(" "+str(i+1)))
	Players.append(PlayerTaz(" "+str(i+1)))
	Players.append(PlayerMartin(" "+str(i+1)))
	Players.append(PlayerAjay(" "+str(i+1)))

for i in range(80):
	Players.append(EnemyRat3(" Number "+str(i+1)))

	

Teams = []

rng.shuffle(Players)

for Plr in Players:
	Plr.RollInitiative()

Players = sorted(Players, key=lambda PlayerGeneric: PlayerGeneric.Initiative, reverse=True)

for plr in Players:
	if plr.IFF not in list(t.TeamIFF for t in Teams):
		Teams.append(TeamGeneric(plr.Name+"'s team",plr.IFF))
	next(x for x in Teams if x.TeamIFF == plr.IFF).AddTeammate(plr)
	

for t in Teams:
	t.Update()

for plr in Players:
	plr.FindOpponent()


while True:
	for t in Teams:
		t.Update()
	if list(t.IsAlive for t in Teams).count(True) == 1:
		for t in Teams:
			if t.IsAlive:
				print(t.Name+" wins!")
		break

	Turns += 1

	print("Turn "+str(Turns)+":"); sleep (slpshort)
	for t in Teams:
		if t.IsAlive:
			print(t.Name+" is still up ",end=""); sleep(slprshort)
			numA = 0
			numT = 0
			for p in t.Teammates:
				numT +=1
				if p.IsAlive:
					numA += 1
			print("("+str(numA)+"/"+str(numT)+")")
	print();sleep(slplong)

	for plr in Players:
		for t in Teams:
			t.Update()
		if plr.IsAlive:
			plr.CommentateGenericAttack()
		else:
			print(plr.Name+" is dead..."); sleep(slprshort)
	print();sleep(slpshort)
	print();sleep(slplong)





# while True:
# 	Turns += 1
# 	print("	Round "+str(Turns)+"!")
# 	sleep(.25)
# 	Player1.CommentateGenericAttack(Enemy1)
# 	if not Enemy1.IsAlive:
# 		print(Player1.Name+" has defeated "+Enemy1.Name+"!"); sleep(5)
# 		break
# 	Enemy1.CommentateGenericAttack(Player1)
# 	print("")
# 	print(Player1.Name+"'s HP is "+str(Player1.HP)); sleep(.15)
# 	print(Enemy1.Name+"'s HP is "+str(Enemy1.HP)); sleep(.15)
# 	sleep(1)
# 	if not Player1.IsAlive:
# 		print(Player1.Name+" has died!"); sleep(5)
# 		break
