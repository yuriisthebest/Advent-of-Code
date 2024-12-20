# Advent of Code 2023
![Collected starts](https://img.shields.io/static/v1?style=for-the-badge&logo=apachespark&label=stars&message=8/50&color=success&logoColor=yellow)

## Tasks
A list of the tasks of this year with explanations, difficulty judgements,
 thoughts and a quick overview of my solutions.

### Personal Difficulty 
- ![](https://via.placeholder.com/15/00ff00/000000?text=+) Very Easy
- ![](https://via.placeholder.com/15/ccff00/000000?text=+) Easy
- ![](https://via.placeholder.com/15/ff9900/000000?text=+) Medium
- ![](https://via.placeholder.com/15/ff0000/000000?text=+) Hard
- ![](https://via.placeholder.com/15/000000/000000?text=+) Very Hard


### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 1: Trebuchet?! 
* **Question:** From of list of strings, find the first and last digit (both numbers and written out).
* **Solution:** Breaking the string into blocks of digits and letters (using regex) and matching written words within the blocks.
* **Difficulty:** `str.find()` and `str.index()` return the first index with match, which can cause some numbers to be missed. Example, if a final block contained `'ninetwonine'`, the last number found would be 2 instead of 9.
* **Thoughts:** Way to difficult of a first day, but afterwards a good challenge.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 2: Cube Conundrum
* **Question:** Find maximum numbers within a string correlated on the word (color) that comes after.
* **Solution:** Splitting the string to get pairs of numbers and colors and a dictionary to keep track of the maximums. 
* **Thoughts:** Not very difficult; The game is interesting, and it would be fun to see it coming back more difficult.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 3: Gear Ratios 
* **Question:** In a grid of characters; Find number that are next to `*`, and maintain which numbers are next to those stars.
* **Solution:** Create position grid with only numbers and symbols; Merge the digits of numbers so their value and positions are maintained; Using the grid, determine if those positions have non-numeric neighbors / `*`.
* **Thoughts:** The hardest part was to parse the data correctly into the grid system so numbers and their positions were maintained; After that the trickiest thing to avoid was to not make incorrect assumptions such as: "Each number only appears once on each line", "Each number can only be adjacent to one gears" and "Each gear has always to adjacent numbers"; I only made a mistake with the first assumption, the other were easy to anticipate.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 4: Scratchcards 
* **Question:** Determine how many scratchcards are in a pile. Each winning scratchcard creates a copy of the next 'X' scratchcards where 'X' is the number of winning numbers a card has.
* **Solution:** Create a dictionary containing all cards once. If card 'Y' wins 'X' times, add 'Y' copies to the next 'X' dict entries (Can also be done with a list).
* **Thoughts:** I made no mistakes on this question and the code looks quite minimal and readable. Nice little challenge.

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 5: If You Give A Seed A Fertilizer 
* **Question:** Given a series of mappings and initial ranges, after sequentially mapping the ranges through the series, what is the lowest resulting value?
* **Solution:** Go backwards through the mappings with the lowest possible final values one at a time and check if the final number in within the initial range.
* **Thoughts:** I think we are out of the very easy questions. This was the first question where naive algorithms could not work due to runtime issues. Fortunately, the second-slowest option was still reasonable to implement and had a runtime around 4 minutes.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 6: Wait For It 
* **Question:** Calculate how many options there are to hold a button to win a race.
* **Solution:** Loop until you find the first race winning value; Then loop for the back until you find the last race winning value; Calculate the difference, which will be the amount of winning options. 
* **Thoughts:** Surprisingly easy, the wording alluded to it being more difficult.

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 7: Camel Cards 
* **Question:** Sort poker hands with jokers!
* **Solution:** Using insertion sort, compare hands until the to-be-inserted hand is the weakest in the comparison and insert fittingly. Use count and some logic to determine the strength of a hand.
* **Thoughts:** The tricky part was to determine the strength of a hand. It was a nice logic puzzle involving jokers and I missed a case in my code where 4 jokers (and an additional card) would often classify as a four of a kind instead of a five of a kind. Once this missed case was detected it was easy to add an explicit case for it.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 8: Haunted Wasteland 
* **Question:** Follow instructions to leave a maze multiple times simultaneously. Find at which point in time all simultaneous paths are on an exit node.
* **Solution:** Compute for all paths the distance time it takes to find an exit node, use the lcm to calculate a point where they all overlap.
* **Thoughts:** It took me a while to figure out how to find the cycles in the paths to calculate the lcm. Fortunately, the puzzle input was nice so after a bit of checking the first time a node finds the exit it will repeat in that order.

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 9: Mirage Maintenance 
* **Question:** Predict the next value in a sequence by recursively computing the differences between values in the sequence.
* **Solution:** Logic and loops.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 10: Pipe Maze 
* **Question:** Find the number of tiles that are enclosed by a loop of pipes.
* **Solution:** Find the loop first, then follow the loop while keeping track which non-loop values are to the left and the right of the loop. This is done by determining the direction the loop goes and using logic to figure out which neighbor is on which side; Since the loop goes along the edges of the input (assumption), the side that is on the outside will have negative values from neighbors that are on the edge (also the inside will likely contain fewer tiles); Use bfs on the found inside tiles to find tiles that are enclosed but not next to the loop.
* **Thoughts:** It was difficult to figure out a solution that wouldn't consider tiles that are within the loop but not enclosed. I was also dreading a bit that I would need direction logic which I find somewhat clunky and tried finding a smart solution. Eventually I made the direction logic, which worked fine.

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 11: Cosmic Expansion 
* **Question:** Calculate the distances between every pair of galaxies in an expanding universe.
* **Solution:** Use manhattan distance on every galaxy pair, keep track of which rows and column expand in the universe and add the expansion factor to the distance per expanding row/column that the shortest path passes.
* **Thoughts:** The concept of the question is fun but overall not too difficult. The twist was expected, which means that I got the second star within a minute (59 seconds).

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 12: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 13: Point of Incidence 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 14: Parabolic Reflector Dish 
* **Question:** Calculate the load stress of a platform after 1000000000 cycles of rocks moving around.
* **Solution:** Simulate the rocks until a cycle if found. Calculate the period of the cycle (manually) and use it to predict the state of the platform after the required cycles.
* **Thoughts:** If was difficult to figure what to do and how to start to solve each part; But once a solution started forming, it was quite doable. I don't know if this comes from experience with AoC or that I happened to gain some insight in the puzzle.

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 15: Lens Library 
* **Question:** Hash a code to determine the box and lens type to be inserted.
* **Solution:** Just implement the hash algorithm as stated and maintain the order of the lenses in the boxes with their focusing power.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 16: The Floor Will Be Lava 
* **Question:** Find the best initial starting point to bounce a beam of light through mirrors and splitters to turn the mountain in lava.
* **Solution:** A BFS / DFS approach; Maintain a queue of tiles with directions that still have to be processed and remember which tiles have been processed from which direction. Apply the bounce logic and run the simulation until all beams have been processed. Brute-force type method works in 400 sec.
* **Thoughts:** After a busy week I was a bit out of touch with AoC. This day allowed me to ease into it again and hopefully continue a bit further. My solution is a bit slow, but speed is never a limiting factor!

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
