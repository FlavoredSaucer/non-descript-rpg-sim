import random as rng
from re import split
from time import sleep


def eep(tim : float = 0):
	if tim >= 0.05:
		sleep(tim)


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
	iFF = 0
	d20 = Die(20)
	InitiativePlus = 0
	Team = None

	AC = 1
	HP = 1
	Initiative=0
	Opponent = None
	DeathMessage = False
	PlusToHit = 0
	AttackActions = 1
	Attack = "0d0+2"
	AtkDice = []
	AtkPlus = 0

	Phrases = [
		"Test 1",
		"Test 2",
		"Test 3",
	]


	def __init__(self,NameOverride : str = "", NameSuffix : str = "", IFFOverride : int = None):
		self.d20 = Die(20)
		if NameOverride:
			self.Name = NameOverride
		self.Name += NameSuffix
		self.AtkDice = []
		self.IsAlive = True
		self.LastDamage = 0
		self.Opponent = None
		if IFFOverride is not None:
			self.iFF = IFFOverride
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
		Attacks = self.AttackActions
		while Attacks >= 1:
			Attacks -= 1
			if self.Opponent is None:
				print(self.Name+" cannot find a target!")
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
				print("Dealing "+str(self.LastDamage)+" points to "+self.Opponent.Name+". ("+str(self.Opponent.HP)+" HP Left.)"); eep(HitDelay)
			else:
				print(self.Name+" misses "+self.Opponent.Name+" with a "+str(self.d20.Roll+self.PlusToHit)+"..."); eep(MissDelay)


	def Speak(self):
		print(self.Name+" says: "+rng.choice(self.Phrases))
	
	def FindOpponent(self,Silent = True):
		EnemyTeams = []
		if self.iFF == 0:
			for x in Teams:
				if x.IsAlive:
					for t in x.Teammates:
						if t.IsAlive and t is not self:
							EnemyTeams.append(t)
		else:
			for x in Teams:
				if x.IsAlive and x.TeamIFF != self.iFF:
					for t in x.Teammates:
						if t.IsAlive:
							EnemyTeams.append(t)
		
		if len(EnemyTeams) == 0:
			self.Opponent = None
			return
		else:
			self.Opponent = rng.choice(EnemyTeams)
			if not Silent:
				print(self.Name+"'s opponent is "+self.Opponent.Name+"!")
			return



class PlayerArwin(PlayerGeneric):
	Name="Arwin"
	iFF = 1
	AC=16
	HP=34
	InitiativePlus = 1
	PlusToHit=5
	Attack="2d6+3"

class PlayerPrincess(PlayerGeneric):
	Name="Princess Ophelia"
	iFF = 1
	AC=18
	HP=40
	PlusToHit=3
	Attack="1d8+1"

class PlayerPrincess2(PlayerGeneric):
	Name="Princess Ophelia"
	iFF = 1
	AC=18
	HP=76
	AttackActions=2
	PlusToHit=5
	Attack="1d8+1"

class PlayerAjay(PlayerGeneric):
	Name="Ajay Gale"
	iFF = 1
	AC=11
	HP=20
	InitiativePlus=4
	PlusToHit=5
	Attack="3d8"

class PlayerTaz(PlayerGeneric):
	Name="Taaz"
	iFF = 1
	AC=19
	HP=28
	InitiativePlus=1
	PlusToHit=5
	Attack="1d6+3"

class PlayerMartin(PlayerGeneric):
	Name="Martin Magfiel"
	iFF = 1
	AC=15
	HP=35
	InitiativePlus = 2
	PlusToHit=6
	Attack="1d12+4"

class PlayerArwin2(PlayerGeneric):
	Name="Arwin Gepetto"
	iFF = 1
	AC = 19
	HP = 164
	InitiativePlus = 2
	AttackActions = 2
	PlusToHit = 9
	Attack="2d6+6"

class PlayerAjay2(PlayerGeneric):
	Name="Ajay Gale"
	iFF = 1
	AC=19
	HP=50
	InitiativePlus=5
	PlusToHit=7
	Attack="3d8"

class PlayerTaz2(PlayerGeneric):
	Name="Taaz"
	iFF = 1
	AC=21
	HP=95
	InitiativePlus=1
	PlusToHit=7
	Attack="2d8+8"

class PlayerMartin2(PlayerGeneric):
	Name="Martin Magfiel"
	iFF = 1
	AC=18
	HP=97
	InitiativePlus = 2
	PlusToHit=10
	Attack="2d6+7"

class EnemyRatSwarm(PlayerGeneric):
	Name="Rat Swarm"
	iFF = 2
	AC=10
	HP=24
	PlusToHit=2
	Attack="2d6"

class EnemyRatGay(PlayerGeneric):
	Name="1000 Gay Rats"
	iFF = 2
	AC=5
	HP=500
	AttackActions=69
	InitiativePlus=2
	PlusToHit=3
	Attack="1d4"

class EnemyRatGiant(PlayerGeneric):
	Name="Giant Rat"
	iFF = 2
	AC=12
	HP=7
	InitiativePlus=0
	PlusToHit=4
	Attack="1d4+2"

class EnemyBeholder(PlayerGeneric):
	Name="Beholder"
	iFF = 3
	AC=18
	HP=180
	PlusToHit=5
	Attack="4d6"

class RandomRat(PlayerGeneric):
	Name="Wild Rat"
	iFF = 0
	AC = 5
	HP = 12
	PlusToHit = 0
	Attack = "1d4"

class RandomRat2(PlayerGeneric):
	Name="Wild Rat"
	iFF = 0
	AC = 5
	HP = 2
	AttackActions = 2
	PlusToHit = 0
	Attack = "1d4"

class EnemyDragon(PlayerGeneric):
	Name="dragom"
	iFF=69
	AC=19
	HP=225
	AttackActions=3
	PlusToHit=12
	Attack="2d10+7"

class EnemyWTF(PlayerGeneric):
	Name="Beholder V2"
	iFF = 3
	AC=19
	HP=180
	AttackActions = 23
	Attack="1d4"

	def CommentateGenericAttack(self):
		Attacks = self.AttackActions
		while Attacks >= 1:
			Attacks -= 1
			if self.Opponent is None:
				print(self.Name+" cannot find a target!")
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
				print("Dealing "+str(self.LastDamage)+" points to "+self.Opponent.Name+". ("+str(self.Opponent.HP)+" HP Left.)"); eep(HitDelay)
			else:
				print(self.Name+" misses "+self.Opponent.Name+" with a "+str(self.d20.Roll+self.PlusToHit)+"..."); eep(MissDelay)
				self.FindOpponent()


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

	# def ReturnRandomTeammate(self):
	# 	Teammate = [x for x in self.Teammates if x.IsAlive]
	# 	if len(Teammate) == 0:
	# 		return None
	# 	return Teammate[0]



# slplong = .1
# slpshort = slplong/2
# slprshort = slplong/10

TurnDelay = 1
MissDelay = 0.1
DeadDelay = 0.1
HitDelay = 0.1


# Main Game
Turns = 0 

Players = []
Teams = []


# Players.append(PlayerPrincess2())

Players.append(EnemyDragon())

Players.append(PlayerAjay2())
Players.append(PlayerArwin2())
Players.append(PlayerTaz2())
Players.append(PlayerMartin2())

# for kat in range(20):
# 	Players.append(PlayerPrincess2(str(kat),IFFOverride=0))

# for rat in range(400):
# 	Players.append(RandomRat(" " + str(rat)))

# Players.append(EnemyWTF(IFFOverride=2))



rng.shuffle(Players)

for Plr in Players:
	Plr.RollInitiative()

Players = sorted(Players, key=lambda PlayerGeneric: PlayerGeneric.Initiative, reverse=True)

for plr in Players:
	if plr.iFF not in list(t.TeamIFF for t in Teams):
		Teams.append(TeamGeneric(plr.Name+"'s team",plr.iFF))
	next(x for x in Teams if x.TeamIFF == plr.iFF).AddTeammate(plr)
	

for t in Teams:
	t.Update()

for plr in Players:
	plr.FindOpponent()

while True:
	AlivePlayers = [x for x in Players if x.IsAlive]
	HitDelay = TurnDelay * 3 / sum(x.AttackActions for x in AlivePlayers)
	MissDelay = HitDelay
	DeadDelay = HitDelay
	for t in Teams:
		t.Update()
		for p in t.Teammates:
			if not p.IsAlive:
				p.DeathMessage = True
	AliveTeams = [t for t in Teams if t.IsAlive]
	if len(AliveTeams) == 1:
		TeamTemp = AliveTeams[0]
		if TeamTemp.TeamIFF == 0:
			ZeroTeammates = [x for x in TeamTemp.Teammates if x.IsAlive]
			if len(ZeroTeammates) == 1:
				print(ZeroTeammates[0].Name+" wins!")
				print(ZeroTeammates[0].Name+" has "+str(ZeroTeammates[0].HP)+" HP left")
				break
		else:
			print(TeamTemp.Name+" wins!")
			for t in TeamTemp.Teammates:
				print(t.Name+" has "+str(t.HP)+" HP left")
			break
			
	
	# 		if t.IsAlive and t.TeamIFF == 0:
	# 			if len(list(p.IsAlive for p in t.Teammates)) == 1:
	# 				print("wawa")
	# Alive = []
	# Alive.extend(list(x for x in Teams if x.TeamIFF != 0))
	# Alive.extend(list(x.Teammates for x in Teams if x.TeamIFF == 0))
	# print(Alive)

	Turns += 1

	print("Turn "+str(Turns)+":"); eep (TurnDelay)
	for t in Teams:
		if t.IsAlive:
			print(t.Name+" is still up ",end="")
			numA = 0
			numT = 0
			for p in t.Teammates:
				numT +=1
				if p.IsAlive:
					numA += 1
			print("("+str(numA)+"/"+str(numT)+")")
	print();eep(TurnDelay)

	for plr in Players:
		for t in Teams:
			t.Update()
		if plr.IsAlive:
			plr.CommentateGenericAttack()
		else:
			if not plr.DeathMessage:
				print(plr.Name+" is dead..."); eep(DeadDelay)
				plr.DeathMessage = True
	print();eep(DeadDelay)
	print();eep(TurnDelay)





# while True:
# 	Turns += 1
# 	print("	Round "+str(Turns)+"!")
# 	eep(.25)
# 	Player1.CommentateGenericAttack(Enemy1)
# 	if not Enemy1.IsAlive:
# 		print(Player1.Name+" has defeated "+Enemy1.Name+"!"); eep(5)
# 		break
# 	Enemy1.CommentateGenericAttack(Player1)
# 	print("")
# 	print(Player1.Name+"'s HP is "+str(Player1.HP)); eep(.15)
# 	print(Enemy1.Name+"'s HP is "+str(Enemy1.HP)); eep(.15)
# 	eep(1)
# 	if not Player1.IsAlive:
# 		print(Player1.Name+" has died!"); eep(5)
# 		break
