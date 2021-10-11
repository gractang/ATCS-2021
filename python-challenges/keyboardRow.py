FIRST = {'q','w','e','r','t','y','u','i','o','p','Q','W','E','R','T','Y','U','I','O','P'}
SECOND = {'a','s','d','f','g','h','j','k','l','A','S','D','F','G','H','J','K','L'}
THIRD = {'x','c','v','b','n','m','Z','X','C','V','B','N','M'}

def findWords(words):
	words_that_work = []
	for word in words:
		status = [0,0,0]
		for letter in word:
			if letter in FIRST:
				status[0] = 1
			elif letter in SECOND:
				status[1] = 1
			elif letter in THIRD:
				status[2] = 1
			else:
				break
		if (status[0] and not status[1] and not status[2]) or (not status[0] and status[1] and not status[2]) or (not status[0] and not status[1] and status[2]):
			words_that_work.append(word)
	return words_that_work

print(findWords(["Hello","Alaska","Dad","Peace"]))