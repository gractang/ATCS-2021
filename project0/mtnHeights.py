mountains = {'Mount Everest':8848, 'K2':8611, 'Kangchenjunga':8586, 'Lhotse':8516, 'Makalu':8485}
for mtn_name in mountains:
	print(mtn_name)
print()
for mtn_name in mountains:
	print(mountains[mtn_name])
print()
for mtn_name in mountains:
	print("%s is %i meters tall" % (mtn_name, mountains[mtn_name]))