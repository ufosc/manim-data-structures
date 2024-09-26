# Manim Data Structures
This repository is a fork of [manim-data-structures](https://github.com/drageelr/manim-data-structures). The code should be used as a reference for we're going for, but we are aiming to make the animation interface for our objects a little more fluid.

## Background
Manim is a library for math animation written by Grant Sanderson (3b1b) to create videos for his [YouTube channel](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiwmZ7-1az9AhWfQjABHR0aAFsQtwJ6BAgLEAE&url=https%3A%2F%2Fm.youtube.com%2Fc%2F3blue1brown&usg=AOvVaw1S8JSB2H-8tYFl1lqqZxdb). The open source community adopted his project and began developing the [community version of Manim](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjq-rX41qz9AhVaTTABHWnSCEIQFnoECAkQAQ&url=https%3A%2F%2Fwww.manim.community%2F&usg=AOvVaw0TyF2Amnk2xgbI5hRRBDsJ). What Manim provides is a set of Mobjects (mathematical objects) that can be instantiated and manipulated programatically as well as a rendering engine that can be called to convert the manipulations into videos.

## Motivation
We are aiming to create Mobjects that implement common structures from computer science. For example similarly to how Manim provides a Plane Mobject we will provide a Variable Mobject that can hold an Mobject. Then we can build up more complex Mobjects such as arrays, pointers, linked lists, etc. These Mobjects will be able to be manipulated and animated in the same way as the Mobjects provided by Manim, thus allowing for the creation of videos that demonstrate the use of these data structures with very little additional effort.

## Goals
The goal is to produce a [Manim Plugin](https://www.manim.community/en/stable/plugins.html) that can be installed and used by the community. The plugin will provide a set of Mobjects that can be used to create animations of common data structures. The plugin will also provide a set of animations that can be used to manipulate the Mobjects in a way that is consistent with the way the Mobjects are used in the real world. For example, when a variable is assigned a value, the value is copied into the variable.

### Mobjects
#### TODO
- [ ] Variable
- [ ] Pointer
- [ ] Array
- [ ] List
- [ ] Stack
- [ ] Queue
- [ ] Set
- [ ] Map
- [ ] Linked List
- [ ] Nary-Tree
    - [ ] B-Trees
    - [ ] Heap

#### Reach Goals
- [ ] Graph
    - [ ] Directed Graph
    - [ ] Undirected Graph
    - [ ] Weighted Graph
    - [ ] Directed Weighted Graph
    - [ ] Undirected Weighted Graph
- [ ] Trie

## Contributing
For information on how to contribute to this project, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Installation Instructions
To install the project and its dependencies, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-link.git
2. Navigate to the project directory:
    cd your-project-directory
3. Install the required dependencies using pip:
   pip install -r requirements.txt

Once installed, you can run the project by executing the following command:
python mlinearcollection.py

For detailed usage examples, refer to the following sections in the documentation:
-Arrays
-Variables

## Building the Documentation
This project uses Sphinx for generating its documentation. To generate the HTML documentation locally, follow these steps:

1. Navigate to the docs directory:
   cd docs
2. Build the documentation using the Makefile:
   make html
3. The documentation will be available at _build/html/index.html. Open it in a web browser to view the project documentation.


## Resources Links
- [Getting Started](https://docs.manim.community/en/stable/installation.html)
- [Official Manim Community Documentation](https://docs.manim.community/en/stable/)
- [Official Manim Community GitHub](https://github.com/ManimCommunity/manim)
- [Official Manim Plugin Documentation](https://docs.manim.community/en/stable/plugins.html#creating-plugins)
- [Manim Animation Guidelines](https://docs.manim.community/en/stable/reference_index/animations.html)
- [3b1b Manim Structure (potentially different) from community version)](https://3b1b.github.io/manim/getting_started/structure.html#manim-execution-process)
