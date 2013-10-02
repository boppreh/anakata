anakata
=======

Anakata is a 4D, tiled, command line puzzle game in Python.

Instead of using wireframes and projection, or different colors, the
world is displayed as slices. X and Y look like your regular tile game.
Z are 2D planes stacked, and W is made of 3D columns.

You are `@`, controlled by arrow keys and WSAD, and the goal is to push
`#` into `X`, working around the obstacles `o`.


    ......... ......... .........
    ...ooo... ...ooo... ...ooo...
    ...ooo... ...ooo... ...o.....
    ...ooo... ...ooo... ...ooo...
    .........y......... .........
    .........^......... .........
    .........|......... ......... z
    .........|......... ......... ^
    ......... ......... ......... |
                --> x             |
    ......... ......... ......... |
    ...ooo... ...ooo... ...ooo... |
    ...ooo... ...oXo... ...o.o... |
    ...ooo... ...ooo... ...ooo... |
    ......... ......... ......... |
    ......... ......... ......... |
    ......... ....#.... ......... |
    ......... ....@.... ......... |
    ......... ......... ......... |
                                  |
    ......... ......... ......... |
    ...ooo... ...ooo... ...ooo... |
    ...ooo... ...ooo... ...ooo... |
    ...ooo... ...ooo... ...ooo...
    ......... ......... .........
    ......... ......... .........
    ......... ......... .........
    ......... ......... .........
    ......... ......... .........
          ----------------> w
