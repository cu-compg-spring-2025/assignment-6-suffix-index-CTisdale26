import argparse
import utils
import suffix_tree

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

def build_suffix_array(T):
    suffixes = [(T[i:], i) for i in range(len(T))]
    suffixes.sort()
    suffix_array = [s[1] for s in suffixes]
    return suffix_array

def common_prefix_length(s1, s2):
    prefix_len = 0
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            prefix_len += 1
        else:
            break
    return prefix_len

def search_array(T, suffix_array, q):
    lo = 0
    hi = len(suffix_array)
    max_prefix_len = 0
    
    # First, find the leftmost occurrence
    left = 0
    right = len(suffix_array)
    while left < right:
        mid = (left + right) // 2
        suffix = T[suffix_array[mid]:]
        prefix_len = common_prefix_length(q, suffix)
        max_prefix_len = max(max_prefix_len, prefix_len)
        
        if suffix.startswith(q):
            right = mid
        elif q < suffix:
            right = mid
        else:  # q > suffix
            left = mid + 1
    
    # Starting index of matches
    first = left
    
    # Find the rightmost occurrence
    left = first
    right = len(suffix_array)
    while left < right:
        mid = (left + right) // 2
        suffix = T[suffix_array[mid]:]
        prefix_len = common_prefix_length(q, suffix)
        max_prefix_len = max(max_prefix_len, prefix_len)
        
        if suffix.startswith(q):
            left = mid + 1
        elif q < suffix:
            right = mid
        else:  # q > suffix
            left = mid + 1
    
    # Ending index of matches (exclusive)
    last = right
    
    # Collect all matches
    matches = [suffix_array[i] for i in range(first, last)]
    matches.sort()
    
    return len(matches), max_prefix_len, matches

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]

    array = build_suffix_array(T)

    if args.query:
        match_results = []
        for query in args.query:
            exact_match_count, match_len, match_locations = search_array(T, array, query)
            match_results.append((exact_match_count, match_len, match_locations))
            print(f'{query} : {exact_match_count} exact matches, longest common prefix length: {match_len}, match locations: {match_locations}')
        return match_results
    
    print(T[930:940])

if __name__ == '__main__':
    main()