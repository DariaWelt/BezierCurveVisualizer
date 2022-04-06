# Bezier Curve Visualizer

GUI App for bezier curve visualization and rendering animation. The app have two parts: 
- animation of rendering for curve readed from file
- api for forming curve points manipulation.

## Requirements
- python 3.8
- pyqt5
- scipy

## Ноw use curve manupulator
- drag and grop points forming the curve
- add new intermidiate point with pressed `A` and click
- delete point with pressed `D` and click

## Input file specification
Curve forming points could be loaded from `.txt` file. This file should set the coordinates of the points line by line. 
Requirements:
- One point per one line
- Point coordinates separated by comma: `x, y`, where x,y are numbers 
- There must be at least 2 points in the file

The file parser is insensitive to spaces and empty lines.


Example of file:
```text
-10, 9
0, 87
35, -35
100, 0

```
## Curve rendering animation
...

