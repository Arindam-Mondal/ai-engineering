"""
Candy
Source:  InterviewBit
Pattern: Greedy - two-pass local constraint propagation (patterns.md #6)
Status:  solved (unaided)

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

# Target time complexity:  O(n)   <- achieved: 2 linear passes + 1 sum
# Target space complexity: O(n)   <- achieved: one auxiliary array


class Solution:
    # @param A : tuple of integers
    # @return an integer
    def candy(self, A):
        # ------------------------------------------------------------------
        # WHY TWO PASSES
        # ------------------------------------------------------------------
        # Each child i is bound by three rules:
        #
        #     (a) A[i] > A[i-1]  =>  c[i] > c[i-1]     (out-rank left neighbor)
        #     (b) A[i] > A[i+1]  =>  c[i] > c[i+1]     (out-rank right neighbor)
        #     (c) c[i] >= 1                             (everyone gets one)
        #
        # (a) and (b) LOOK circular - c[i] depends on things to its left and
        # to its right, so no single scan direction settles both. The unlock
        # is that they are actually independent: (a) only ever reads leftward,
        # (b) only ever reads rightward. So satisfy each one separately, in
        # the direction it flows, then merge with max().
        #
        # Why merging with max() is provably right, not just convenient:
        #   - pass 1 gives L[i], the minimum value satisfying (a)
        #   - pass 2 gives R[i], the minimum value satisfying (b)
        #   - a legal c[i] must satisfy both, so c[i] >= max(L[i], R[i])
        #   - taking exactly max(L[i], R[i]) is therefore the smallest legal
        #     choice at every index, and every constraint is of the form
        #     "be STRICTLY GREATER than a lower-rated neighbor" - raising a
        #     value can only ever help such a constraint, never break one.
        #   Minimal at each index + no interference => minimal total.
        # ------------------------------------------------------------------

        n = len(A)

        # Rule (c): the floor. A child with no obligation in either direction
        # (a valley, or an interior member of a flat run) keeps exactly 1,
        # which is what minimality demands.
        #
        # Python note: [1] * n is n references to the same int - safe, since
        # ints are immutable. Do NOT carry this idiom over to mutables:
        # [[]] * n gives you n aliases of ONE list. Java: new int[n] + fill(1).
        candies = [1] * n

        # ------------------------------------------------------------------
        # PASS 1 (left -> right): enforce "out-rank your LEFT neighbor".
        # ------------------------------------------------------------------
        # Start at 1: index 0 has no left neighbor, so (a) is vacuous there.
        # Invariant after step i: candies[0..i] is the minimal assignment
        # satisfying (a) across 0..i.
        for i in range(1, n):
            if A[i] > A[i - 1]:
                # Strictly higher rating => strictly more candy. Cheapest
                # legal value is exactly one more, never +2 (we minimize).
                #
                # candies[i-1] is already final for this pass, which is what
                # makes ONE forward sweep enough: a rising run [1,2,3,4]
                # chains to [1,2,3,4] with no inner loop and no re-scanning.
                candies[i] = candies[i - 1] + 1
            # else, two distinct cases both correctly fall through:
            #   A[i] < A[i-1] -> I owe my left neighbor nothing; the debt runs
            #                    the other way and pass 2 will settle it.
            #   A[i] == A[i-1] -> equal ratings impose NO ordering, so a flat
            #                    run RESETS the chain: [1,2,2,3] -> [1,2,1,2].
            #                    This is the #1 wrong answer on this problem -
            #                    writing >= here quietly inflates the total.

        # ------------------------------------------------------------------
        # PASS 2 (right -> left): enforce "out-rank your RIGHT neighbor".
        # ------------------------------------------------------------------
        # reversed(range(n - 1)) yields n-2, n-3, ..., 1, 0.
        #   range(n-1) is 0..n-2, so index n-1 is skipped - correct, it has no
        #   right neighbor. Reversing walks down to and INCLUDING 0, which
        #   matters: A = [2, 1] needs index 0 bumped to 2.
        #   (Equivalent, uglier: range(n - 2, -1, -1). Java: for (int i = n-2;
        #   i >= 0; i--). reversed() is the more readable Python form.)
        for i in reversed(range(n - 1)):
            if A[i] > A[i + 1]:
                # Mirror of pass 1. candies[i+1] is final for BOTH passes here
                # - pass 1 completed entirely before pass 2 started, and pass 2
                # moves right to left - so candies[i+1] + 1 is a true bound.
                #
                # max() IS the merge step. Plain assignment would clobber pass
                # 1 and break every peak. A = [1, 5, 2, 1]:
                #     after pass 1 : [1, 2, 1, 1]
                #     with max()   : [1, 3, 2, 1] = 7   correct
                #     with assign  : [1, 2, 2, 1] = 6   illegal - the 5 ties
                #                                       with its neighbor 2
                candies[i] = max(candies[i], candies[i + 1] + 1)
            # else: no right-side obligation, keep pass 1's value.
            # Note the asymmetry that makes the whole thing sound: pass 2 only
            # ever RAISES values, so pass 1's guarantees survive untouched.

        # sum() over a list of ints runs at C speed - no manual accumulator
        # loop needed (the reflex a Java background gives you).
        return sum(candies)

        # ------------------------------------------------------------------
        # COMPLEXITY
        # ------------------------------------------------------------------
        # Time:  O(n) - three linear sweeps (2 loops + sum), no nesting, no
        #        sort. Compare the naive "keep re-scanning until nothing
        #        changes" fixpoint: O(n^2) on [1,2,3,...,n], guaranteed TLE
        #        at n = 10^5.
        # Space: O(n) for `candies`. Standard accepted answer. An O(1) variant
        #        exists (count ascending/descending run lengths and add
        #        triangular numbers, with fiddly ownership of the shared peak)
        #        - much easier to get wrong, not worth it unless asked.
        #
        # WORKED TRACE - A = [1, 2, 3, 3, 2, 1] (peak spans a plateau)
        #   init:    [1, 1, 1, 1, 1, 1]
        #   pass 1:  i=1 2>1 -> 2 | i=2 3>2 -> 3 | i=3 3>3 no (plateau RESETS)
        #            i=4 2>3 no  | i=5 1>2 no
        #            => [1, 2, 3, 1, 1, 1]
        #   pass 2:  i=4 2>1 -> max(1,2)=2 | i=3 3>2 -> max(1,3)=3
        #            i=2 3>3 no (stays 3)  | i=1 2>3 no | i=0 1>2 no
        #            => [1, 2, 3, 3, 2, 1]
        #   sum = 12
        #   Index 2 owns the left run's peak, index 3 owns the right run's.
        #   They are allowed to TIE at 3 precisely because their ratings tie.


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


# ---------------------------------------------------------------------- NOTES
# Pattern: greedy two-pass. When an element is constrained by BOTH neighbors,
#   split into one pass per direction and combine with max(). Same shape as
#   trapping-rain-water (left-max / right-max) and product-except-self
#   (prefix / suffix). Recognition cue: "depends on both sides at once".
# Trap 1: compare with > not >=. Equal ratings impose no ordering, so a flat
#   run must RESET the chain: [1,2,2,3] -> [1,2,1,2], total 6 not 8.
# Trap 2: pass 2 must be max(candies[i], candies[i+1] + 1). Plain assignment
#   discards pass 1 and breaks every peak.
# Python: reversed(range(n - 1)) is the clean backward walk that still hits
#   index 0; range(n - 2, -1, -1) is the same thing, harder to read.
#   [1] * n is fine for ints, an aliasing bug for lists.
