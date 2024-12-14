# Advent of Code 2024
![Collected starts](https://img.shields.io/static/v1?style=for-the-badge&logo=apachespark&label=stars&message=20/50&color=success&logoColor=yellow)

## Tasks
A list of the tasks of this year with explanations, difficulty judgements,
 thoughts and a quick overview of my solutions.

### Personal Difficulty 
- ![](https://via.placeholder.com/15/00ff00/000000?text=+) Very Easy
- ![](https://via.placeholder.com/15/ccff00/000000?text=+) Easy
- ![](https://via.placeholder.com/15/ff9900/000000?text=+) Medium
- ![](https://via.placeholder.com/15/ff0000/000000?text=+) Hard
- ![](https://via.placeholder.com/15/000000/000000?text=+) Very Hard


### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 1: Historian Hysteria
* **Question:** Use one list to search for counts of numbers in another list
* **Solution:** Loop over list 1, count occurrences in list 2; naive method
* **Thoughts:** Okay start, not too difficult, not too easy. Theming seems lower this year, will see in the coming weeks

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 2: Red-Nosed Reports
* **Question:** Check if a report is safe, ignoring one bad number in the sequence
* **Solution:** Loop over the numbers until a bad level is encountered. Remove either the left or right level (one of which is bad) and check again if the report is safe (without removing any more levels).
* **Thoughts:** More difficult than I expected at day 2 early in the morning, got stuck a little on trying to ignore numbers instead of removing and checking again.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 3: Mull It Over 
* **Question:** Find multiplication statements in a random string of characters.
* **Solution:** Use regex!
* **Thoughts:** Always fun to use regex :D

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 4: Ceres Search 
* **Question:** Find the word XMAS and X's of the word MAS in a word seeker
* **Solution:** Check every location of the word seeker if it has an A (or X in part 1). Then try to map all possible associated patterns (XMAS or MAS - MAS) on that location.
* **Thoughts:** It was kind a brute-force but a neat challenge.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 5: Print Queue 
* **Question:** Fix the order of given lists of numbers according to given ordering rules
* **Solution:** Keep a dict with all numbers that must be in-front or behind a number to easily check if a number is in order. Then iteratively add numbers to the front of the list if they are allowed in order.
* **Thoughts:** Not having any big edge-cases is nice and ensures a non-frustrating solve

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 6: Guard Gallivant 
* **Question:** Figure out where to place an obstruction to make the guard walk in loops
* **Solution:** Place an obstruction at every point in the path and check if it creates a loop
* **Thoughts:** I have a very slow solution, but the question was great

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 7: Bridge Repair 
* **Question:** Figure out if a total can be made using given values and some operators
* **Solution:** Recursively compute the total of the values with different operators until the total is found or all options have been checked
* **Thoughts:** It seemed way more complex that it was, since a recursive brute-force method worked splendidly

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 8: Resonant Collinearity 
* **Question:** Find all grid positions that are in line with a set of given beacons
* **Solution:** Calculate all the anti-node positions inside the frame based on the numeric location of the antennas pairs
* **Thoughts:** This seemed a lot like the code I wrote for work

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 9: Disk Fragmenter 
* **Question:** Defragment a file system given a disk map that describes the file system
* **Solution:** Keep an ordered list with the id, size and gap behind the file. Go from the files in the back to the front while checking the gaps from front to back to check if there is space for the file to move. If a space is found, move the file in the ordered list and adjust the gaps of the file, the previous file in front and the new file in front, to maintain the correct gaps.
* **Thoughts:** I forgot to do this day and wanted an easy one before bed... it wasn't that easy and took quite some time

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 10: Hoof It
* **Question:** Find the distinct number of paths from a trailhead to possible tops
* **Solution:** For each trailhead: Figure out which neighbors can be stepped to from current locations, repeat this 9 times until you get to a top. Count how often you have reached the top.
* **Thoughts:** I really liked this challenge. Funny enough I think this is the first time my part two solution was equal to part 1 minus a single line of code (it's skipped when called by part 2).

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 11: Plutonian Pebbles 
* **Question:** Figure out how many multiplying pebbles there are after blinking a lot
* **Solution:** Use recursion with memoization to efficiently calculate the amount of splits a number will do with the remain amount of blinks
* **Thoughts:** Memoization! Use the fact that the same numbers occur many times in the row of pebbles

### ![](https://via.placeholder.com/15/ff0000/000000?text=+) Day 12: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 13: Claw Contraption 
* **Question:** Find x and y such that A*x + B*y = Target (very large number) for two dimensions if x and y exist
* **Solution:** Download a integer linear optimization package (ortools) and rewrite the problem as integer optimization
* **Thoughts:** I don't like adding packages to the advent of code, since I try to keep it pure python. However, transforming the problem to integer optimization is far more effective than solving it by code. There probably is a repetition trick cause by the values of button a and b (there often is such a trick), but I generally don't like to find them if there is an easier method. The problem itself is nice with a nice concept and somewhat hidden optimization problem.
* **Alternative solution (worked only for part one):** Start with maximizing B based on target and setting A to 0. If the current value is above target, remove 1 B. If the value is below, add 1 A. Keep going until a solution is found or B is negative. This takes way too long for part 2, but I found it elegant

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 14: Restroom Redoubt 
* **Question:** Figure out after how many steps the linear walking bots create a figure of a Christmas tree.
* **Solution:** Go step by step (from the back is faster) until there is a situation where 8 bots line up vertically, that is a good indication of when an image is created.
* **Thoughts:** I did not expect that part 2, I (thought that I) optimized part 1 for an extension of the map or for many iterations. I did further improve finding the end locations of the bats for any given steps, and now it runs fairly fast.

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 15: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 16: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 17: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 18: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 19: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 20: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 21: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 22: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 23: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 24: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 25: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 
