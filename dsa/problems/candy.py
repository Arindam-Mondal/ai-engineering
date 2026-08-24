"""
Candy
Source:  InterviewBit
Pattern: (filled in after you solve it)
Status:  not started

PROBLEM
    N children stand in a line, each with a rating A[i]. Give out candies
    so every child has at least 1, and any child rated higher than a
    neighbor gets strictly more candy than that neighbor. Minimize the
    total candies handed out.

CONSTRAINTS
    1 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9
    equal neighboring ratings impose no ordering requirement between them

EXAMPLES
    A = [1, 2]       -> 3    (candies = [1, 2])
    A = [1, 5, 2, 1]  -> 7    (candies = [1, 3, 2, 1])

BEFORE YOU CODE
    1. What complexity are you aiming for, given len(A) can be 10^5?
    2. A child's required candy count depends on comparisons with BOTH
       neighbors at once - how do you avoid needing both answers before
       you can compute either?

Run:  python candy.py
"""

# Target time complexity:  O(n)
# Target space complexity: O(n)


class Solution:
    # @param A : tuple of integers
    # @return an integer
    def candy(self, A):
        n = len(A)
        candies = [1] * n
        for i in range(1,n):
            if A[i] > A[i-1]:
                candies[i] = candies[i-1] + 1

        for i in reversed(range(n-1)):
            if A[i] > A[i+1]:
                candies[i] = max(candies[i],candies[i+1]+1)

        return sum(candies)


# ---------------------------------------------------------------- self-check
# Run this file directly. Silence means everything passed.
# InterviewBit is the real judge; these just catch the obvious breakage first.

if __name__ == "__main__":
    s = Solution()

    # examples from the statement
    assert s.candy([1, 2]) == 3
    assert s.candy([1, 5, 2, 1]) == 7

    # edges
    assert s.candy([1]) == 1                      # single child
    assert s.candy([5]) == 1                      # single child, any rating
    assert s.candy([1, 1]) == 2                   # equal neighbors, no bump
    assert s.candy([1, 1, 1, 1]) == 4              # all identical
    assert s.candy([5, 4, 3, 2, 1]) == 15          # strictly decreasing
    assert s.candy([1, 2, 3, 4, 5]) == 15          # strictly increasing
    assert s.candy([1, 2, 2]) == 4                 # rise then flat
    assert s.candy([2, 2, 1]) == 4                 # flat then fall
    assert s.candy([1, 3, 2, 2, 1]) == 7           # peak, then a flat descent
    assert s.candy([1, 2, 3, 3, 2, 1]) == 12       # peak spans a plateau
    assert s.candy([-1000000000, 0, 1000000000]) == 6  # min/max legal values

    print("all checks passed")
