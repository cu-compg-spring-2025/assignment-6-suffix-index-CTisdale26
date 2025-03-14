[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2H4hMYgM)
# suffix_index
Suffix data structures for aligning reads to a reference.

## Overview
This project implements suffix data structures, including suffix trees and suffix arrays, for efficient string matching and alignment. The project includes the following files:

- `suffix_tree.py`
- `suffix_array.py`
- `suffix_trie.py`
- `utils.py`
- `experiment.py`

## Suffix Tree

### `suffix_tree.py`

#### `add_suffix(nodes, suf)`

**Purpose**: Integrates a suffix `suf` into an existing tree structure represented by nodes.

**Parameters**:
- `nodes`: A list of nodes representing the current state of the suffix tree. Each node is a list containing two elements:
  1.  A substring (`SUB`) representing the edge label leading from the parent to the current node. The root node will have the empty string (`''`) as its edge label.
  2.  A dictionary (`CHILDREN`) mapping the first character in the child's edge label to node indices representing the node's children.

- `suf`: A string representing the suffix to be added to the suffix tree.

### Operation
- The function iterates over the characters of `suf`.
- For each character, it checks if the character is already represented in the tree at the current node's children.
- If not, a new node is created for the remaining part of `suf`, and the process terminates for this suffix.
- If the character is found, the function compares the suffix with the substring of the found node to check how much of it matches.
- If a mismatch is found before the end of the node's substring, a new intermediate node is created to represent the common prefix, and the original node is split into two parts: the common prefix and the remaining substring.
- This process is repeated until the entire suffix has been processed.

### Notes
- This function is called iteratively by `build_suffix_tree` for each suffix of the input text.
- The constants `CHILDREN` and `SUB` are assumed predefined indices or keys that correspond to the children dictionary and the substring part of a node, respectively.

#### `build_suffix_tree(text)`

**Purpose**: Constructs a suffix tree for a given input string `text`.

**Parameters**:
- `text`: The input string for which the suffix tree is to be constructed.

**Returns**: A list of nodes representing the suffix tree of the input text.

### Operation
- Appends a terminal symbol `$` to the end of `text` to mark the end of the string. This ensures that all suffixes are considered unique.
- Initializes the tree with a single root node having an empty substring and no children.
- Iterates over each index of `text`, treating each suffix starting from that index as a new suffix to be added to the tree.
- Calls `add_suffix` for each of these suffixes, passing the current state of the tree and the suffix.
- Returns the constructed suffix tree.

### Notes
- The suffix tree structure allows for efficient search and analysis operations on the input text, such as finding substrings, repetitions, etc.
- The terminal symbol `$` is crucial for ensuring that no suffix is a prefix of another, simplifying the tree construction logic.

## Suffix Array

### `suffix_array.py`

#### `build_suffix_array(T)`

**Purpose**: Constructs a suffix array for a given input string `T`.

**Parameters**:
- `T`: The input string for which the suffix array is to be constructed.

**Returns**: A list of integers representing the starting indices of the sorted suffixes of `T`.

**Example**:
```python
suffix_array = build_suffix_array('your_text_here')
```

## Methods and Experiments

The methods in this repository are designed to construct and manipulate suffix data structures such as suffix trees and suffix arrays. These methods include functions for adding suffixes to trees, building complete suffix trees and arrays, and performing various string matching operations. The `experiment.py` file contains scripts to test and benchmark these data structures, providing insights into their performance and efficiency in different scenarios.