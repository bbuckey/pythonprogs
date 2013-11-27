import os, sys, math, glob, decimal


def swapPlayer(team,playera,playerb):
	indexa = team.index(playera)
	indexb = team.index(playerb)
	team[indexa]= playerb
	team[indexb]= playera
	return team

class GAME:
	def __init__(self):
		self.teamodd = TEAM()
		self.teameven = TEAM()
		self.thetime = int(0)
		
	def setOddTeam(self,oddteam):
		self.teamodd = oddteam
	
	def setEvenTeam(self,eventeam):
		self.teameven = eventeam
	
	def setTime(self,_round):
		self.thetime = _round
	
	def getTime(self):
		return self.thetime

	def getOddTeam(self):
		return self.teamodd 
	
	def getEvenTeam(self):
		return self.teameven
	
	def benchPlayer(self,index):
		self.teamodd.removePlayer(index)
		self.teameven.removePlayer(index)
	
	def setTeams(seld,_team):
		lista = _team.getTeam()
		for x in lista:
			p = x
			for y in lista:
				if p.getShotp() > y.getShotp() and p.getName() != y.getName():
					lista = swapPlayer(lista,p,y)
					p = y
				elif p.getShotp() < y.getShotp() and p.getName() != y.getName():
					continue
				else:
					if p.getHight() > y.getHight() and p.getName() != y.getName():
						lista = swapPlayer(lista,p,y)
						p = y
					elif p.getHight() < y.getHight() and p.getName() != y.getName():
						continue
		_team.setTeam(lista)
		return _team
					
class TEAM:
	
	def __init__(self):
		self.team = list()
		self.teamSize = 0
	
	def setTeam(self,_team):
		self.team = _team
	
	def setPlayerAppend(self,_team):
		self.team.append(_team)

	def getTeam(self):
		return self.team
	
	def setTeamSize(self,_size):
		self.teamSize = _size

	def getTeamSize(self):
		return self.teamSize
	
	def removePlayer(self,index):
		self.team.remove(self.team[index])
	
class PLAYER:

	def __init__(self):
		self.name = ""
		self.shotp = 0
		self.hight = 0
		self.draft_number = 0
		self.player_time = 0

	def setPlayer(self,_name,_shotp,_hight):
		self.name = _name
		self.shotp = _shotp
		self.hight = _hight
		
	def setDraftNumber(self,dnum):
		self.draft_number = dnum
		
	def setPlayTime(self,playt):
		self.player_time = playt
		
	def getName(self):
		return self.name
	
	def getShotp(self):
		return self.shotp
	
	def getHight(self):
		return self.hight
	
	def getDraftNumber(self):
		return self.draft_number
	
	def getPlayTime(self):
		return self.player_time
	

if __name__ == "__main__":
	loc = "basketball_game_example_input.txt"
	outf = "basketball_game_results.txt"
	outfile = open (outf,'w')
	infile = open(loc,'r')
	listinput = [ a.rstrip('\n') for a in infile.readlines()]
	rounds = int(listinput[0:1].pop())
	listinput = listinput[1:]
	for a in range(0,rounds):
		teams = listinput[0:1].pop()
		listinput = listinput[1:]
		teamstats = teams.split(' ')
		tplayer = teamstats[0:1].pop()
		teamstats = teamstats[1:]
		game = GAME()
		fullteam = TEAM()
		teamo = TEAM()
		teame = TEAM()
		game.setTime(teamstats[0:1].pop())
		fullteam.setTeamSize(int(tplayer))
		teamstats = teamstats[1:]
		size = teamstats[0:1].pop()
		teamo.setTeamSize(size)
		teame.setTeamSize(size)
		for b in range(0,int(tplayer)):
			theplayer = listinput[0:1].pop()
			theplayer = theplayer.split(' ')
			playerp = PLAYER()
			playerp.setPlayer(theplayer[0:1].pop(), int(theplayer[1:2].pop()), int(theplayer[2:3].pop()))
			playerp.setDraftNumber(b+1)
			fullteam.setPlayerAppend(playerp)
			listinput = listinput[1:]
		for b in range(0,int(tplayer)):	
			fullteam = game.setTeams(fullteam)
		for b in range(0,int(tplayer)):
			if b % 2 == 0:
				teamo.setPlayerAppend(fullteam.getTeam()[b])
			else :
				teame.setPlayerAppend(fullteam.getTeam()[b])
		game.setOddTeam(teamo)
		game.setEvenTeam(teame)
		y=int(game.getTime())
		h = abs(len(game.getOddTeam().getTeam()) - int(size))
		for x in range(0,h):
			z =  (y+(x+1)) % int(len(game.getOddTeam().getTeam()))
			game.getOddTeam().removePlayer(z)
		h = abs(len(game.getEvenTeam().getTeam()) - int(size))
		for x in range(0,h):
			z =  (y+(x+1)) % int(len(game.getEvenTeam().getTeam()))
			game.getEvenTeam().removePlayer(z)
		listfinal = list()
		for n in game.getOddTeam().getTeam():
			listfinal.append(n.getName())
		for n in game.getEvenTeam().getTeam():
			listfinal.append(n.getName())
		listfinal.sort()
		strfinal = "Case #%i: " % (a+1)
		for n in listfinal:
			strfinal += n + " "
		outfile.write(strfinal + "\n")
	outfile.close()
	infile.close()
