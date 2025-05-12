# modulo-automata

I made this after I watched a video on modulo arithmetic and wondered if it could be applied to cellular automata. The steps to calculate the current cells next state is:
```
1. sum all of the neighbours cells
2. take sum % (number of stages)
```
This will result in a number between 0 and 7 that can then be used to color it accordingly. The result is something beautiful, an ever changing pattern that somehow manages to loop if it is symmetrical.

## Controls
```
SPACE - pause/play animation
R - reset the grid
E - export the current grid
I - import a grid
UP - increase FPS
DOWN - decrease FPS
RIGHT - step a single time
A - increase hue
D - decrease hue
G - hide/show the grid
LEFT CLICK - increase cell by 1
RIGHT CLICK - decrease cell by 1
```

## Gallery
![image](https://github.com/user-attachments/assets/06c91c98-e17e-4f9b-8db2-312ac0505de7)
![image](https://github.com/user-attachments/assets/1e01c5e2-1b65-40d9-84e3-dedc405675df)
![image](https://github.com/user-attachments/assets/31627b3f-8389-4128-bfcc-ef8100f1d306)
![image](https://github.com/user-attachments/assets/09d1af29-972a-44ca-b80f-72c3ac6c3b3b)
![image](https://github.com/user-attachments/assets/81e5f0a4-1a9b-491c-9026-5d4b2dd57a4c)

