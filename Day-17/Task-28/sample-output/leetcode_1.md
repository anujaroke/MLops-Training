# Two Sum - LeetCode

## 1. Problem Statement
Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.  
You may assume that each input would have exactly one solution, and you may not use the same element twice.  
You can return the answer in any order.

**Example 1:**  
Input: `nums = [2,7,11,15]`, `target = 9`  
Output: `[0,1]`  
Explanation: Because `nums[0] + nums[1] == 9`, we return `[0, 1]`.

**Example 2:**  
Input: `nums = [3,2,4]`, `target = 6`  
Output: `[1,2]`

**Example 3:**  
Input: `nums = [3,3]`, `target = 6`  
Output: `[0,1]`

---

## 2. ELI10 (Explain Like I'm 10)
Imagine you have a list of numbers and a magic number (target). You need to find two numbers in the list that add up to the magic number. Once you find them, tell their positions in the list.

For example:  
List: `[2, 7, 11, 15]`  
Magic number: `9`  
You see that `2 + 7 = 9`, so their positions are `0` and `1`. That's your answer!

---

## 3. Intuition
We need to find two numbers in the array that sum up to the target. Instead of checking every possible pair (which is slow), we can keep track of the numbers we've already seen and check if the current number's complement (target - current number) exists in our "seen" list.

---

## 4. Brute Force Approach
Check every possible pair of numbers in the array and see if they add up to the target.

**Steps:**
1. Loop through each element `nums[i]`.
2. For each `nums[i]`, loop through the rest of the elements `nums[j]` (where `j > i`).
3. If `nums[i] + nums[j] == target`, return `[i, j]`.

**Time Complexity:** O(n²) (because of nested loops)  
**Space Complexity:** O(1) (no extra space used)

---

## 5. Optimal Approach (Hash Map)
Use a hash map (dictionary) to store the numbers we've seen along with their indices. For each number, check if its complement (target - number) exists in the map.

**Steps:**
1. Initialize an empty dictionary `seen`.
2. Loop through the array with index `i` and value `num`.
3. Calculate the complement: `complement = target - num`.
4. If `complement` is in `seen`, return `[seen[complement], i]`.
5. Otherwise, store `num` in `seen` with its index `i`.

**Time Complexity:** O(n) (single pass through the array)  
**Space Complexity:** O(n) (storing values in the hash map)

---

## 6. Time Complexity
- **Brute Force:** O(n²)  
- **Optimal (Hash Map):** O(n)

---

## 7. Space Complexity
- **Brute Force:** O(1)  
- **Optimal (Hash Map):** O(n)

---

## 8. Python Solution
```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []  # In case no solution (though problem states there is one)
```

---

## 9. Dry Run Example
Let's take `nums = [2, 7, 11, 15]` and `target = 9`.

| Iteration | `i` | `num` | `complement = 9 - num` | `seen` before check | Action                     |
|-----------|-----|-------|------------------------|---------------------|----------------------------|
| 1         | 0   | 2     | 7                      | `{}`                | `7` not in `seen`. Store `{2: 0}`. |
| 2         | 1   | 7     | 2                      | `{2: 0}`            | `2` is in `seen`. Return `[0, 1]`. |

**Output:** `[0, 1]` ✅