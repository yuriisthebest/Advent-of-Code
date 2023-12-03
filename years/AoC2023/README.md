# Advent of Code 2023
![Collected starts](https://img.shields.io/static/v1?style=for-the-badge&logo=apachespark&label=stars&message=6/50&color=success&logoColor=yellow)

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

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 4: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 5: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 6: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 7: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 8: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 9: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 10: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 11: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 12: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 13: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

### ![](https://via.placeholder.com/15/ffffff/000000?text=+) Day 14: 
* **Question:** 
* **Solution:** 
* **Thoughts:** 

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
