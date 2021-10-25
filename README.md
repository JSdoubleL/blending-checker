# Blending Checker

Checks whether a newick tree is contains blending with reference to newick constraint trees.

## Dependencies

- Python 3
- [Treeswift](https://github.com/niemasd/TreeSwift)

## Usage

**Input:** Input tree containing all taxa and disjoint constraint trees defining taxa groups

**Output:** Returns true if the taxa in the input tree are separated so that each taxa group could be removed by deleting one edge (i.e., the tree is unblended).

```cmd
python3 blending-checker.py -i <input_tree_file> -t <constraint_tree> ...
```

### Arguments

- `-i`: (string) Input tree file
- `-t`: (strings) Constraint tree files
