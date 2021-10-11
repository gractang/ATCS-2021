def validPalindrome(s):
	newstring = [x for x in s.lower() if x in "qwertyuiopasdfghjklzxcvbnm"]
	return newstring == newstring[::-1]
