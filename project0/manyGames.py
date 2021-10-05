games = ['Minecraft', 'Valorant', 'Genshin Impact']
print("I like the following games: " + str(games))
new_game = input("What's a game you like?")
games.append(new_game)
while new_game != 'no':
	new_game = input("What's another game you like?")
	games.append(new_game)
print("We like the following games: " + str(games))