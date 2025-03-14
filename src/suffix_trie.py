import argparse
import utils

def get_args():
    parser = argparse.ArgumentParser(description='Suffix Trie')

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

def build_suffix_trie(s):
    root = {}
    
    # Insert all suffixes into the trie
    for i in range(len(s)):
        current_node = root
        for char in s[i:]:
            if char not in current_node:
                current_node[char] = {}
            current_node = current_node[char]
        current_node['$'] = True  # Mark the end of a suffix
    
    return root

def search_trie(trie, pattern):
    current_node = trie
    for char in pattern:
        if char not in current_node:
            return False
        current_node = current_node[char]
    return True

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]

    trie = build_suffix_trie(T)

    if args.query:
        for query in args.query:
            match_found = search_trie(trie, query)
            print(f'{query} : {match_found}')

if __name__ == '__main__':
    main()
