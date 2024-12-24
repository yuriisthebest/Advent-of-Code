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

### ![](https://via.placeholder.com/15/ff0000/000000?text=+) Day 12: Garden Groups
* **Question:** Find regions of letters in a grid and find the amount of sides these shapes have
* **Solution:** First find the areas and all their neighbors (counting duplicates). Then merge neighbors together iff they are next to each other, and they originate from the same relative direction to their area origin.
* **Thoughts:** This question was hard for me, but my cognitive state was somewhat impacted by a large Christmas party and the fact that it was late at night. Solving part 2 of this problem two days later was much easier and took little effort (continuing the work from my attempts on the 12th).

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 13: Claw Contraption 
* **Question:** Find x and y such that A*x + B*y = Target (very large number) for two dimensions if x and y exist
* **Solution:** Download a integer linear optimization package (ortools) and rewrite the problem as integer optimization
* **Thoughts:** I don't like adding packages to the advent of code, since I try to keep it pure python. However, transforming the problem to integer optimization is far more effective than solving it by code. There probably is a repetition trick cause by the values of button a and b (there often is such a trick), but I generally don't like to find them if there is an easier method. The problem itself is nice with a nice concept and somewhat hidden optimization problem.
* **Alternative solution (worked only for part one):** Start with maximizing B based on target and setting A to 0. If the current value is above target, remove 1 B. If the value is below, add 1 A. Keep going until a solution is found or B is negative. This takes way too long for part 2, but I found it elegant

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 14: Restroom Redoubt 
* **Question:** Figure out after how many steps the linear walking bots create a figure of a Christmas tree.
* **Solution:** Go step by step (from the back is faster) until there is a situation where 8 bots line up vertically, that is a good indication of when an image is created.
* **Thoughts:** I did not expect that part 2, I (thought that I) optimized part 1 for an extension of the map or for many iterations. I did further improve finding the end locations of the bats for any given steps, and now it runs fairly fast.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 15: Warehouse Woes 
* **Question:** A randomly moving robot is moving boxes by running into them, where do the boxes end up?
* **Solution:** A recursive mess of if-statements and data modifications.
* **Thoughts:** LANTERNFISH are Back! It was a fun problem that looked a lot like day 6. Took not that long to solve.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 16: Reindeer Maze 
* **Question:** Find the optimals paths through a maze
* **Solution:** Dijkstra's algorithm but don't stop when first solution is found
* **Thoughts:** I expected harder questions by now. I did get stuck for a while on trying a double pathfinding solution to check if start -> tile -> end is as fast as start -> end. It was slow and somehow it didn't work. Modiying dijkstra was also faster and easier in the end.

### ![](https://via.placeholder.com/15/ff0000/000000?text=+) Day 17: Chronospatial Computer 
* **Question:** Reverse engineer code instruction to figure out which input number to use
* **Solution:** TDB
* **Thoughts:** -NOT SOLVED YET- I like reverse engineering puzzles, but this is difficult

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 18: RAM Run 
* **Question:** Find out when a path from the top-left to the bottom-right is blocked
* **Solution:** Bruteforce: I searched for a path from start to end for each new byte that had fallen
* **Thoughts:** This was very easy for day 18. Granted I did bruteforce the solution, but with numbers this low it wouldn't make sense to do it more efficiently. A more elegant solution would be to see when a line is formed that spans the entire memory bank, but I'm not sure how much faster of a solution that would be

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 19: Linen Layout 
* **Question:** Figure out in how many ways a design can be made. <- that explanation makes no sense. Ever tried to create words / sentences from the abreviations on the periodic table? That's this day's challenge.
* **Solution:** Recurse from the start of the pattern to see which patterns it matches, remove that start and continue recursing.
* **Thoughts:** I love memoization with recursion.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 20: Race Condition 
* **Question:** Given a path through a maze, how many paths could you cheat through the maze.
* **Solution:** Find the path through the maze. Check for each step to which positions further along it could cheat, count how often that occurs
* **Thoughts:** Wow, I was thinking way too complex, difficult and time-consuming by using a pathfinder to find all possible cheat paths. However, the key is that you can easily find the path that will be taken, which is static besides the cheating. This would be an easy day if it didn't take me ~2 hours to figure this out.

### ![](https://via.placeholder.com/15/ff0000/000000?text=+) Day 21: Keypad Conundrum 
* **Question:** Dictate the movements of a chain of robots. Recursively describe a string by writing it on a numpad.
* **Solution:** Key insight, if you look at a chunk of movements of the next bot, it doesn't matter where the bots further down the line are with their arm. You can take each segment (start and stop on "A") as individual chunks that have to be described, order does not matter. Therefor, keep track of which segments have been seen how many times which needs to be described by another bot in the line.
* **Thoughts:** Beautiful! The amount of code and the runtime of the code are both really low, but it took a long time to find all the insights in the problem and how to use that to solve it, escpecially the insight above took a while, as did the order in which the keys should be pressed to find the optimal path (for part 1). Also, I lost sight of the exact metrics required for my difficulty rating system.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 22: Monkey Market 
* **Question:** Efficiently compute a series of numbers and find a short sequence in the sequences that accumulate the most bananas
* **Solution:** Remember the last four differences in the sequence. For each new number, update the sequence and remember this sequence and the amount of bananas it buys. Combine all sequences in one dict, such that each sequences contains all the bananas it buys across all venders. Check which of these sequences produce the most bananas and return that.
* **Thoughts:** I love these recent problems that are quite simple, but requires a lot of considerations and insights in how it exactly works. After understanding it completely, writing code that efficiently finds the answer is surprisingly short.

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 23: 
* **Question:** Find the max clique given a set of connections
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
