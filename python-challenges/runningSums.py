def runningSums(nums):
	sums = [nums[0]]
	for i in range(1,len(nums)):
		sums.append(sums[i-1]+nums[i])
	return sums

print(runningSums([3,1,2,10,1]))