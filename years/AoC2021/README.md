# Advent of Code 2021
![Collected starts](https://img.shields.io/static/v1?style=for-the-badge&logo=apachespark&label=stars&message=50/50&color=success&logoColor=yellow)

## Tasks
A list of the tasks of this year with explanations, difficulty judgements,
 thoughts and a quick overview of my solutions.

### Personal Difficulty 
- ![](https://via.placeholder.com/15/00ff00/000000?text=+) Very Easy
- ![](https://via.placeholder.com/15/ccff00/000000?text=+) Easy
- ![](https://via.placeholder.com/15/ff9900/000000?text=+) Medium
- ![](https://via.placeholder.com/15/ff0000/000000?text=+) Hard
- ![](https://via.placeholder.com/15/000000/000000?text=+) Very Hard


### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 1: Sonar Sweep
* **Question:** From an ordered list of numbers, find the amount of times the following number is greater than the current number.
* **Solution:** for-loop
* **Thoughts:** My first real challenge, a fun way to start Advent of Code 2021!

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 2: Dive!
* **Question:** Follow a set of instructions to angle and move the submarine in the ocean
* **Solution:** for-loop oover instructions while maintaining variables for the position and angle of the submarine

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 3: Binary Diagnostic
* **Question:** From a list of binary numbers,
    find numbers with the most/least common digits until only one number is left
* **Solution:** Exercise revealed all logic, find the numbers with the most/least common digit i,
    keep those numbers and repeat for i+1 until one number is left
* **Issues:** Minor misunderstanding of the task (most common digit i for all numbers != most common digit i for the numbers kept in memory)

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 4: Giant Squid
* **Question:** Play bingo with 100 cards, which card wins first, which card wins last
* **Solution:** Create a function to check is a card has won, then go through each card with one extra bingo number at a time, maintain wins until the last card wins.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 5: Hydrothermal Venture 
* **Question:** Consider a list of strait lines on a 2D grid (axis-aligned or 45 degrees).
    Find all points in the grid where 2 or more lines overlap
* **Solution:** Maintain a list of all seen grid points, incrementally add lines to be seen, increment a counter if a point is seen twice.

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 6: Lanternfish
* **Question:** Lanternfish breed exponentially, how many Lanternfish are present after 256 days
* **Initial Solution:** Create a fish object that creates another fish object after a certain amount of days
* **Initial Issues:** Updating and appending 10^12 items in a list is very slow...
* **Final Solution:** Maintain the amount of fish of each breed cycle,
        update cycle numbers for each time step instead of fish.
* **Thoughts:** The first exercise where I had to completely rewrite my program for part 2
        (this became a reoccurring thing later on)

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 7: The Treachery of Whales
* **Question:** Given a list of numbers, find the value with the minimum total distance to the numbers
* **Solution:** Start at the mean of the numbers as a proxy of the correct solution.
        Calculate the distance from this position, move towards the direction that reduces the distance
         (path of least resistance), if the distance becomes greater again,
          then the previous position is the optimal value

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 8: Seven Segment Search
* **Question:** Given the segment signal patterns for 0-9 of a 7 segment display in random order,
    figure out which pattern belongs to which number.
* **Solution:** The digits 1, 4, 7 and 8 have a unique amount of segments in a 7 segment display,
        and can therefore easily be identified. We remember the segments used for 1 (right-top and right-bottom),
        and we remember the segments of 8 that are not present in 4 and 7 (left-bottom and bottom).
        2, 3 and 5 all use 5 segments, and 0, 6, 9 all use 6 segments.
        2,3,5: 3 can be distinguished because it uses both segments from 1.
        2 and 5 can be distinguished from each other because the 2 will use both the left-bottom and bottom,
        while 5 only uses the bottom.
        0,6,9: 9 can be distinguished because it does not use the left-bottom segment (0 and 6 do).
        0 and 6 can be distinguished because the 0 uses both the segments used for 1.
        All digits can be identified using the signal patterns,
         the rest of the challenge is to do this multiple times and sum the results
* **Thoughts:** A very interesting concept with a nice logic to it.
        A fun challenge to try and solve it without creating an entire segment-signal map

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 9: Smoke Basin
* **Question:** Consider a 2D grid with values. Find the basins in this grid.
        A basin is an area surrounded by 9's (the max value)
* **Solution:** Part 1 requires to find all the local minima in the grid.
        Each minima is in 1 basin and each basin has only 1 minima (not always true, but it is in this exercise).
        Use recursion on each low point to find all points in the basin (BFS)

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 10: Syntax Scoring
* **Question:** Given a lot of parentheses, find corrupt ones and fix incomplete ones.
* **Solution:** Recursion
* **Issues:** I don't think I know what I did

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 11: Dumbo Octopus
* **Question:** Synchronise flashing octopuses in a 2D grid, at which timestamp are they synchronized?
* **Solution:** For each timestamp, remember that every octopus must increase their timer.
        One by one, increase their timer. If an octopus flashes,
        remember them and add their neighbors another time to increase timer.
        After all timer increases are finished, set the timers of octopuses that flashed to 0

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 12: Passage Pathing 
* **Question:** Find all paths in a cave system
* **Solution:** Recursively add rooms to the possible paths to count all paths (DFS)

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 13: Transparent Origami
* **Question:** Fold a piece of transparent paper. This overlaps dots until 8 capital letters can be seen
* **Solution:** Maintain the position of all dots. After each fold, check which dots have been folded,
        change their x or y position accordingly. Finally, print the code with the dots.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 14: Extended Polymerization
* **Question:** Do chemistry
* **Initial Solution:** Just do the chemistry
* **Initial Issues:** String operations on strings with 10^12 characters are very slow...
* **Solution:** Maintain counts of element pairs, similarly to day 6.
* **Issues:** All elements will be double counted in each pair, expect for the elements in the first and last positions.
        This was very hard to problem solve because it was unclear what the correct solution was.
        This issue apparently was not actually an issue, so the code ran fine once I removed my 'fixes'

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 15: Chiton
* **Question:** Given a 2D grid with risk levels, find the path from top-left to bottom-right with the least risk
* **Solution:** Dijkstra
* **Issues:** Fairly slow, part 2 takes 25 seconds. A* would probably be an improvement

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 16: Packet Decoder 
* **Question:** Given an hex decoded BITS transmission, what is the number?
* **Solution:** Decode the hex into binary, the binary into BITS packets,
    the BITS packets into operations and the operations into numbers.
* **Issues:** Identifying the packets is difficult, but a large recursive function did the trick
* **Thoughts:** Very fun, but the amount of instructions exceeded my personal organic working memory capacity

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 17: Trick Shot
* **Question:** Launch a probe using a specific velocity to ensure the probe lands in a certain area,
        how many different velocities ensure this?
* **Solution:** Brute-force some velocities to see which work and which do not

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 18: Snailfish
* **Question:** Help snailfish with their math, which is really weird.
        They work with nested pairs of numbers which explode is they are too nested
        and splits if any number is too large.
* **Solution:** Create a tree structure of the snailfish numbers.
        The left branch contains the left value of the pair, the right branch contains the right value.
        Nested pairs are pairs within branches.
        Splitting and exploding can be done using tree functions.
        It is a lot of coding work, but does not require too complex logic
* **Thoughts:** Very fun!

### ![](https://via.placeholder.com/15/000000/000000?text=+) Day 19: Beacon Scanner
* **Question:** Scanners and beacons are put in the water.
        Scanners can see nearby beacons and their relative positions.
        The areas of some scanner might overlap at least 12 common beacons.
        What are the positions of the scanners?
* **Solution:** For each pair of scanners, check if they overlap by testing if they have 12 beacons
        with the exact same relative distances from each other.
        Once we found all overlapping scanner pairs, rotate and transpose each scanner so it
        faces a common direction with a known position.
* **Issues:** Rotating and transposing in 3D sucks. I had to take some code from somewhere
        else that individually wrote down the different rotations.
        All the logic is mine and worked the moment that the correct rotations where put in.
* **Thoughts:** Please no 3D rotations...

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 20: Trench Map 
* **Question:** Use an image enhancement algorithm to enhance an image
* **Solution:** For each enhancement step, pad the image with some 0s or 1s.
        Perform the enhancement algorithm on 3x3 slices of the image.
* **Thoughts:** It was fun to figure out that the padding of the image had to flip every other step
        because of the enhancement algorithm

### ![](https://via.placeholder.com/15/ff0000/000000?text=+) Day 21: Dirac Dice 
* **Question:** Play a game of Dirac Dice, using a quantum dice that splits into 3 different universes
        each time it is thrown. Continue until the winner has 21 points, who wins the most?
* **Solution:** Maintain a dictionary with game states and their amount of occurrences. For all games
        still playing, take a turn splitting into 7 different universes with different probabilities.
        After all games are over, take counts on which universes are won by who.
* **Issues:** This took a while to code.
        It is difficult to create something than can go to 10^12 at a reasonable speed while maintaining info.

### ![](https://via.placeholder.com/15/ff0000/000000?text=+) Day 22: Reactor Reboot
* **Question:** Reboot the reactor using the given instructions, turning on and off cubes in a large 3D cuboid
* **Initial Solution:** Maintain a 3D grid with 0s and 1s for each step
* **Initial Issues:** A cube with 50.000^3 values does not fit in memory...
* **Solution:** Create ranges and when a new instruction overlaps an existing range,
        divide that range into smaller sub-ranges.
* **Issues:** It is very difficult to create code without faults to partition a cube into smaller cubes.
        I don't know what was wrong, but my code was not working.
* **Final Solution** Whenever a new instruction overlaps an existing range, create an additional range.
        This additional range is negative if it overlaps an positive range,
        or positive if it overlaps a negative range.
        This maintains the correct amount of 'on' or 'off' cubes in that range.
        For example, three positive ranges all intersecting a certain area would interact as follows:
        Range 1 would be added and just be there, thus this area has a +1 overall count since it is positive.
        Range 2 would overlap it, thus creating a new negative area there.
        We now have 2 positive ranges and 1 negative, for an overall +1 count.
        The 3rd range would overlap 2 positive ranges, creating 2 negative ranges, and 1 negative range,
        creating 1 positive range. The total is now 4 positive ranges and 3 negative ranges, for a +1 overall.
        If there is now suddenly an 'off' instruction in this area, then the 4 positive ranges create
        4 negative ranges, and the 3 negative ranges create 3 positive ranges.
        The total would be 7 positive and 7 negative ranges, thus the entire area has a count of 0,
        which is correct since it was just turned off.
        Note: my code does cancel out equal positive and negative ranges to reduce computational time

### ![](https://via.placeholder.com/15/ff0000/000000?text=+) Day 23: Amphipod
* **Question:** Do a puzzle where you have to sort the items into their respective containers.
* **Solution:** I did this day fully by hand.
        I did create a warped version of A* to solve the problem. But it is too slow for part 2.
* **Issues:** It is quite a complex puzzle to code, even though it is fairly doable by hand.

### ![](https://via.placeholder.com/15/000000/000000?text=+) Day 24: Arithmetic Logic Unit 
* **Question:** Find the largest and smallest model numbers that are valid according to MONAD
* **Solution:** Perform one chunk of the instructions at a time.
        Maintain the z-values after each chunk with the largest/smallest number than leads to that z-value.
        Report the valid remembered number after the instructions are complete
* **Issues:** It took a long time and 5 attempts before the code worked in a reasonable time.
        The code now almost looks simple!
* **Runs in:** 7s per part

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 25: Sea Cucumber
* **Question:** 
* **Solution:** Maintain a 2D grid with the positions of the cucumbers. For each step until no movement,
        let the east facing cucumbers go east. Then, transpose the grid, move the south facing cucumber east
        and transpose back.
* **Thoughts:** I finished my first year of Advent of Code!!!
