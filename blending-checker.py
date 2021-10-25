import treeswift as ts
import argparse

def blended(tree, constraint_trees) -> bool:
    """
    Uses Fitches parsimony algorithm to determine if tree is blended given tree and groups of taxa.

    Args:
        ``tree`` (``treeswift tree``): Tree to assess for blending

        ``taxa_map`` (``list[treeswift tree]``): List of constraint trees
    """
    # TODO: check that constraint trees cover all taxa in tree

    taxa_map = {}
    for i, t in enumerate(constraint_trees):
        for taxa in ts.read_tree_newick(t).labels(internal=False):
            taxa_map[taxa] = i

    # Arbitrarily root tree
    if tree.root.num_children() != 2:
        tree.reroot(next(tree.traverse_preorder()))
    if tree.num_nodes(leaves=False) != tree.num_nodes(internal=False) - 1:
        raise Exception("Input tree is not fully resolved")

    # Compute score
    score = 0
    for v in tree.traverse_postorder():
        if v.is_leaf():
            v.state = {taxa_map[v.get_label()]}
        else:
            [left, right] = v.child_nodes()
            if len(left.state.intersection(right.state)) == 0:
                v.state = left.state.union(right.state)
                score += 1
            else:
                v.state = left.state.intersection(right.state)

    return score != len(constraint_trees) - 1


def main(args):
    input_tree = ts.read_tree_newick(args.input_tree)
    constraint_trees = [ts.read_tree_newick(t) for t in args.constraint_trees]
    print('Tree contains blending.' if blended(input_tree, constraint_trees) else 'Tree is unblended.')

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-tree', type=str, required=True, 
                        help="Input tree to check for blending")
    parser.add_argument('-t', '--constraint-trees', type=str, nargs="+", required=True,
                        help="Disjoint constraint trees")

    main(parser.parse_args())
