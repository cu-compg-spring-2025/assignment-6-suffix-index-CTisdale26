import argparse
import utils

SUB = 0
CHILDREN = 1

def get_args():
    parser = argparse.ArgumentParser(description='Suffix Tree')

    parser.add_argument('--reference',
                        help='Reference sequence file',
                        type=str)

    parser.add_argument('--string',
                        help='Reference sequence',
                        type=str)

    parser.add_argument('--query',
                        help='Query sequences',
                        nargs='+',
                        type=str)

    return parser.parse_args()

def add_suffix(nodes, suf):
    n = 0
    i = 0
    while i < len(suf):
        b = suf[i] 
        children = nodes[n][CHILDREN]
        if b not in children:
            n2 = len(nodes)
            nodes.append([suf[i:], {}])
            nodes[n][CHILDREN][b] = n2
            return
        else:
            n2 = children[b]

        sub2 = nodes[n2][SUB]
        j = 0
        while j < len(sub2) and i + j < len(suf) and suf[i + j] == sub2[j]:
            j += 1

        if j < len(sub2):
            n3 = n2 
            n2 = len(nodes)
            nodes.append([sub2[:j], {sub2[j]: n3}])
            nodes[n3][SUB] = sub2[j:]
            nodes[n][CHILDREN][b] = n2

        i += j
        n = n2

def build_suffix_tree(text):
    text += "$"

    nodes = [ ['', {}] ]

    for i in range(len(text)):
        add_suffix(nodes, text[i:])
    
    return nodes

def search_tree(suffix_tree, P):
    n = 0
    i = 0
    matches = []
    
    # Navigate to the node representing the end of the pattern
    while i < len(P):
        b = P[i]
        children = suffix_tree[n][CHILDREN]
        if b not in children:
            return 0, []  # Pattern not found
        n2 = children[b]
        sub2 = suffix_tree[n2][SUB]
        j = 0
        while j < len(sub2) and i + j < len(P) and P[i + j] == sub2[j]:
            j += 1
        if j < len(sub2):
            return 0, []  # Pattern not found
        i += j
        n = n2
    
    # Helper function to collect all leaf positions
    def collect_leaves(node_id, path_length):
        if not suffix_tree[node_id][CHILDREN]:  # This is a leaf
            # The path length gives us the suffix's starting position
            suffix_start = len(suffix_tree[0][SUB]) - path_length - 1  # -1 for the $ terminator
            matches.append(suffix_start)
        else:
            for child_id in suffix_tree[node_id][CHILDREN].values():
                collect_leaves(child_id, path_length + len(suffix_tree[child_id][SUB]))
    
    # Start collecting leaves from the current node
    collect_leaves(n, len(P))
    
    return len(matches), sorted(matches)
def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]

    tree = build_suffix_tree(T)
        
    if args.query:
        for query in args.query:
            match_count, match_locations = search_tree(tree, query)
            print(f'{query} : {match_count} exact matches, match locations: {match_locations}')
    
    # Keep the print statement from your original code
    print(T[930:940])

if __name__ == '__main__':
    main()