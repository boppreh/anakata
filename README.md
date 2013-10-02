anakata
=======

Anakata is a 4D, tiled, command line puzzle game in Python.

Instead of using wiremashes and projection, or different colors, the
world is displayed as slices.

You are `@`, controlled by arrow keys and WSAD, and the goal is to push
`#` into `X`.


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
