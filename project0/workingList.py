careers = ['programmer', 'truck driver', 'teacher', 'nurse']
print(careers.index('programmer'))
print('programmer' in careers)
careers.append('lawyer')
careers.insert(0, 'musician')
for career in careers:
	print(career)