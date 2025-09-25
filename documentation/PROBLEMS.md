### Problems and Future Work

## Concept
- one of the basic concepts: introduce students to python
- students are supposed to fill in certain parts of the int solver (diff equation)
- implementation of the int solver as class makes sense within the software architecture, but not very beginner friendly
- future work: hide the int solver class from students and only let them define the diff eq

## General
- incomplete documentation
- incomplete/bad comments
- imports not sorted
- mostly no type hinting
- redundant code
    - gui, animation and matplotlib_manager modules
    - usage of super classes mitigates this problem only partially, since the structure is always the same but small changes must be made
    - redundant code for `animate_visual` and `draw_first_frame`
    - future work: make inheritance more efficient and find a more sophisticated solution for redundante code
- different layers of Multi Anim Canvas not in variables in most animations, makes it hard to read
- anim modules future work (Prof. Zierath's idea):
    - create a small "library" of shapes (circle, rec, ...)
    - include specific animation functions for each shape that can be called from the animation module
    - should make the animation module cleaner and more easy to read
    - started that already in `src.anim.modules`
- spring damping element (feder dämpfer element) future work:
    - is static at the moment
    - use coordinate transformation to make it look more natural


## Aufgabe 2 Übung 2
- sporadic flickering in the animation

## Aufgabe 1 Übung 5
- when tuning s_dot_0: position of grey rectangle changes, shouldnt change because s_dot_0 just determines the initial velocity: should be because of different max, min values of the deflection array which impacts the mapping function
- animation doesnt fit whats happening in the graphs sometimes
