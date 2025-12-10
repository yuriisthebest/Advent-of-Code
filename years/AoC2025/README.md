# Advent of Code 2025
![Collected starts](https://img.shields.io/static/v1?style=for-the-badge&logo=apachespark&label=stars&message=18/24&color=success&logoColor=yellow)

## Tasks
A list of the tasks of this year with explanations, difficulty judgements,
 thoughts and a quick overview of my solutions.

### Personal Difficulty 
- ![](https://via.placeholder.com/15/00ff00/000000?text=+) Very Easy
- ![](https://via.placeholder.com/15/ccff00/000000?text=+) Easy
- ![](https://via.placeholder.com/15/ff9900/000000?text=+) Medium
- ![](https://via.placeholder.com/15/ff0000/000000?text=+) Hard
- ![](https://via.placeholder.com/15/000000/000000?text=+) Very Hard


### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 1: Secret Entrance
* **Question:** Rotating a safe dial left and right, how often does it pass 0?
* **Solution:** One big mess of modulo operations. The code works for values smaller than 100, so first modulo the rotation value since we are guaranteed to pass 0 with those, then rotate the dial only the tens and ones values.
* **Thoughts:** A fairly easy puzzle, but I kept missing edge-cases causing my to lose some time.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 2: Gift Shop
* **Question:** Find numbers with repeating segments within large number ranges.
* **Solution:** There aren't that many numbers, so iteratively check each number if they contain a set of repeating digits. First chunk the number into same size chunks, then check if the set of these chunks if unique.
* **Thoughts:** Neat and nice puzzle. There were not really any tricks, it was brute-forcible, but a nice little challenge.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 3: Lobby
* **Question:** Given a list of numbers, created the largest number of set size N in order that can be made.
* **Solution:** It is always best to use the largest number first, provided that there are enough digits following it to finish the number. Therefore, create a window with a pointer to the first list value as start and one N digits from the end. Find the largest value in that window, then set the start pointer to the value next to that largest value and increase the stop pointer by one. Do this N times, and you'll find the largest possible number with N digits.
* **Thoughts:** I enjoy puzzles like this where you need to think clearly about your approach. I quickly came to the realization above that greedily getting the largest possible number is always best so that was really nice.

### ![](https://via.placeholder.com/15/00ff00/000000?text=+) Day 4: Printing Department
* **Question:** Check amount of neighbors of cells in a grid that have a special value.
* **Solution:** While loop that keeps track if a cell has changed this loop, then check each cell if it gets modified based on the values of the neighbors.
* **Thoughts:** One of the easiest grid puzzles.

### ![](https://via.placeholder.com/15/ccff00/000000?text=+) Day 5: Cafeteria
* **Question:** Combine overlapping ranges to find all unique values contained in these ranges
* **Solution:** Add each range to a list in sorted order based on the starting value, if the next range is overlapping the larger top value is used as the new top-value. Afterwards combine all ranges again if they have overlap.
* **Thoughts:** I didn't do it in an optimal manner, the first part of my solution can probably be cut out and replaced by a simple sort on the first value (as described in the solution above). It's always tricky to combine overlapping ranges, there are quite a few different cases with larger ranges encompassing multiple smaller ones, but not all of them completely, so that's a nice challenge.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 6: Trash Compactor
* **Question:** Help the cephalopods with some weird math equations. Figure out the column based writing of number to calculate the total score.
* **Thoughts:** I had to rewrite my loading helping functions to not remove all the whitespace around the input, which was a bit annoying for part 2.

### ![](https://via.placeholder.com/15/ff0000/000000?text=+) Day 7: Laboratories
* **Question:** A beam is shot from above and splits a number of times, how many paths are there possible to the bottom?
* **Solution:** Keep for each vertical step track of which beams are present and how many paths are possible to get to that beam.
* **Thoughts:** I fundamentally misunderstood part 1 of this exercise, which makes it really difficult. I believed that a splitter would only count if it actually produced new tachyons, so it would not count if both sides of a splitter were occupied by existing tachyons. That's much more complex to figure out than determining which splitters just get hit by a tachyon, which was the actual question. Once I figured that out it wasn't that difficult. Bonus issue: I knocked over my bottle of water so that caused a slight delay as well.

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 8: Playground
* **Question:** Connect junction boxes sequentially using the smallest non-connected distance between two boxes. Which two boxes are last to connect the entire grid together?
* **Solution:** Create a sorted distance list between any pair of junction boxes. Then sequentially connect them while keeping track of the networks that it generates. If all boxes are in one network return the results.
* **Thoughts:** I tried out my new PriorityQueue class that can take care of sorting, adding and taking the smallest values. It's a little cumbersome to use, but it's nice to use some custom classes.

### ![](https://via.placeholder.com/15/000000/000000?text=+) Day 9: Movie Theater
* **Question:** Find the largest rectangle that fits within an oddly shaped polyhedron.
* **Solution:** Brute-force it baby. I tried many kinds of solutions, eventually settling on keeping track of tiles just next to the shape. Sort the possible rectangles and determine the first one whose edges do not contain any of these outside tiles. Other ideas included: Check if the edge line intersects / crosses a boundary line (the edge case where they intersect at the edge of a segment is very common and for me difficult to deal with); Use my Volumes class to determine overlap and feasibility (unfortunately the class isn't really developed for that yet); Create a 100.000 by 100.000 grid to replicate the data and keep track of which tiles have been seen inside or outside the region (my IDE crashed); Remove all in-between values where no red tiles, corner points, are to reduce the spatial dimentionality cause brute-force methods to be much much faster (the translation is difficult to find the largest rectangle afterwards).
* **Thoughts:** AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH. HOW DO I NOT KNOW HOW TO CALCULATE THE AREA OF A RECTANGLE! **A RECTANGLE!**

### ![](https://via.placeholder.com/15/ff9900/000000?text=+) Day 10: Factory
* **Question:** Find the mimimum amount of buttons to press to get to the specified values for lights and jolts.
* **Solution:** Parse the input to create linear optimization constraints. Then solve it while optimizing for the least presses.

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 11: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 12: 
* **Question:** 
* **Solution:** 
* **Thoughts:**
