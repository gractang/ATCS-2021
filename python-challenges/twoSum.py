def twoSum(nums, target):
	diffs = set()
	for i in range(len(nums)):
		diffs = target - nums[i]



print(twoSum([2,7,11,15], 9))
