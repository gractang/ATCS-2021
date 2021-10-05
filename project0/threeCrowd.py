def crowd_test(names, cutoff):
	if len(names) > cutoff:
		print("you're all gonna get covid")

names = ['Iyanu', 'Charlotte', 'Jhila', 'Mitsuka']

crowd_test(names, 3)

names.remove('Iyanu')
names.remove('Charlotte')

crowd_test(names, 3)