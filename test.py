from typing import List

def pair_sum_sorted(nums: List[int], target: int) -> List[int]:
    print(len(nums))
    for i in range(len(nums)):
        for j in range(len(nums)):
            if target == nums[i] + nums[j]:
                return [i,j]
    return -1
print(pair_sum_sorted([-5, -2, 3, 4, 6], 7))