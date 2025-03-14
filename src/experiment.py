import argparse
import utils
import time
import random
import sys
import psutil
import os
from suffix_tree import build_suffix_tree, search_tree
from suffix_array import build_suffix_array, search_array

# Import matplotlib and set a backend explicitly
import matplotlib
# Use 'Agg' backend if running in a non-interactive environment
if not sys.stdout.isatty():
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description='String Matching Performance Comparison')

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

    parser.add_argument('--experiment',
                        help='Run performance experiment',
                        action='store_true')

    parser.add_argument('--output',
                        help='Output directory for plots',
                        type=str,
                        default='data')

    return parser.parse_args()

def get_memory_usage():
    """Get memory usage of current process in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert to MB

def run_experiment(max_size=10000, step=1000, num_queries=10, query_length=5, output_dir='data'):
    """Run performance experiment for different data structures"""
    # Generate random DNA sequence
    bases = ['A', 'C', 'G', 'T']
    sizes = list(range(step, max_size + step, step))
    
    # Results storage
    results = {
        'sizes': sizes,
        'array': {'build_time': [], 'search_time': [], 'memory': []},
        'tree': {'build_time': [], 'search_time': [], 'memory': []}
    }
    
    for size in sizes:
        print(f"Testing with sequence of length {size}")
        # Generate random sequence
        sequence = ''.join(random.choice(bases) for _ in range(size))
        
        # Generate random queries
        queries = []
        for _ in range(num_queries):
            start = random.randint(0, size - query_length)
            queries.append(sequence[start:start + query_length])
        
        # Measure for Suffix Array
        start_mem = get_memory_usage()
        start_time = time.time()
        suffix_array = build_suffix_array(sequence)
        build_time = time.time() - start_time
        end_mem = get_memory_usage()
        memory_usage = end_mem - start_mem
        print(f"Suffix Array - Start Memory: {start_mem:.2f} MB, End Memory: {end_mem:.2f} MB, Usage: {memory_usage:.2f} MB")
        
        start_time = time.time()
        for query in queries:
            search_array(sequence, suffix_array, query)
        search_time = (time.time() - start_time) / num_queries
        
        results['array']['build_time'].append(build_time)
        results['array']['search_time'].append(search_time)
        results['array']['memory'].append(memory_usage)
        
        # Clear memory
        del suffix_array
        
        # Measure for Suffix Tree
        start_mem = get_memory_usage()
        start_time = time.time()
        suffix_tree = build_suffix_tree(sequence)
        build_time = time.time() - start_time
        end_mem = get_memory_usage()
        memory_usage = end_mem - start_mem
        print(f"Suffix Tree - Start Memory: {start_mem:.2f} MB, End Memory: {end_mem:.2f} MB, Usage: {memory_usage:.2f} MB")
        
        start_time = time.time()
        for query in queries:
            search_tree(suffix_tree, query)
        search_time = (time.time() - start_time) / num_queries
        
        results['tree']['build_time'].append(build_time)
        results['tree']['search_time'].append(search_time)
        results['tree']['memory'].append(memory_usage)
        
        # Clear memory
        del suffix_tree
    
    # Ensure the directory for saving the plot exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create directory with explicit permissions
    output_path = os.path.join(output_dir, 'performance_comparison.png')
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    # Build time
    plt.subplot(2, 2, 1)
    plt.plot(sizes, results['array']['build_time'], 'r-', label='Suffix Array')
    plt.plot(sizes, results['tree']['build_time'], 'g-', label='Suffix Tree')
    plt.xlabel('Sequence Length')
    plt.ylabel('Build Time (seconds)')
    plt.title('Build Time vs Sequence Length')
    plt.legend()
    plt.grid(True)
    
    # Search time
    plt.subplot(2, 2, 2)
    plt.plot(sizes, results['array']['search_time'], 'r-', label='Suffix Array')
    plt.plot(sizes, results['tree']['search_time'], 'g-', label='Suffix Tree')
    plt.xlabel('Sequence Length')
    plt.ylabel('Search Time (seconds)')
    plt.title('Search Time vs Sequence Length')
    plt.legend()
    plt.grid(True)
    
    # Memory usage
    plt.subplot(2, 2, 3)
    plt.plot(sizes, results['array']['memory'], 'r-', label='Suffix Array')
    plt.plot(sizes, results['tree']['memory'], 'g-', label='Suffix Tree')
    plt.xlabel('Sequence Length')
    plt.ylabel('Memory Usage (MB)')
    plt.title('Memory Usage vs Sequence Length')
    plt.legend()
    plt.grid(True)
    
    
    # Save the plot with explicit error handling
    try:
        plt.savefig(output_path)
        print(f"Performance comparison plot saved to '{output_path}'")
    except Exception as e:
        print(f"Error saving plot: {e}")
        # Try saving to current directory as fallback
        try:
            plt.savefig('performance_comparison.png')
            print("Plot saved to current directory as fallback")
        except Exception as e2:
            print(f"Error saving to fallback location: {e2}")
    
    # Show the plot (only works in interactive environments)
    try:
        plt.show()
    except Exception as e:
        print(f"Note: Could not display plot (this is normal in non-interactive environments): {e}")
    
    plt.close()
    
    # Also save results as text for debugging
    try:
        with open(os.path.join(output_dir, 'results.txt'), 'w') as f:
            f.write("Performance Results:\n")
            f.write(f"Sizes: {results['sizes']}\n")
            f.write(f"Array Build Time: {results['array']['build_time']}\n")
            f.write(f"Tree Build Time: {results['tree']['build_time']}\n")
            f.write(f"Array Search Time: {results['array']['search_time']}\n")
            f.write(f"Tree Search Time: {results['tree']['search_time']}\n")
            f.write(f"Array Memory: {results['array']['memory']}\n")
            f.write(f"Tree Memory: {results['tree']['memory']}\n")
    except Exception as e:
        print(f"Error saving results as text: {e}")
    
    return results

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]
    else:
        T = "ACGTACGT"  # Default sequence for testing

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        try:
            os.makedirs(args.output, exist_ok=True)
            print(f"Created output directory: {args.output}")
        except Exception as e:
            print(f"Warning: Could not create output directory: {e}")
            args.output = '.'  # Use current directory as fallback

    if args.experiment:
        # Run the experiment with different parameters depending on system capability
        try:
            available_memory = psutil.virtual_memory().available / (1024 * 1024)  # in MB
            print(f"Available memory: {available_memory:.2f} MB")
            
            if available_memory > 8000:  # More than 8GB
                run_experiment(max_size=20000, step=2000, num_queries=10, output_dir=args.output)
            elif available_memory > 4000:  # More than 4GB
                run_experiment(max_size=10000, step=1000, num_queries=10, output_dir=args.output)
            elif available_memory > 2000:  # More than 2GB
                run_experiment(max_size=5000, step=500, num_queries=10, output_dir=args.output)
            else:  # Limited memory
                run_experiment(max_size=2000, step=200, num_queries=10, output_dir=args.output)
                
        except Exception as e:
            print(f"Error during experiment: {e}")
            # Fallback to a very small experiment
            run_experiment(max_size=1000, step=100, num_queries=5, output_dir=args.output)
    else:
        # Standard query processing
        print("Building data structures...")
        
        # Build and time suffix array
        start_time = time.time()
        suffix_array = build_suffix_array(T)
        array_time = time.time() - start_time
        array_memory = sys.getsizeof(suffix_array) / 1024  # KB
        
        # Build and time suffix tree
        start_time = time.time()
        suffix_tree = build_suffix_tree(T)
        tree_time = time.time() - start_time
        tree_memory = sys.getsizeof(suffix_tree) / 1024  # KB
        
        print(f"\nPerformance Summary for text length {len(T)}:")
        print(f"Suffix Array: Build time = {array_time:.6f}s, Memory = {array_memory:.2f} KB")
        print(f"Suffix Tree: Build time = {tree_time:.6f}s, Memory = {tree_memory:.2f} KB")
        
        if args.query:
            print("\nQuery Results:")
            for query in args.query:
                print(f"\nSearching for '{query}':")
                
                start_time = time.time()
                array_count, max_prefix, array_positions = search_array(T, suffix_array, query)
                array_search_time = time.time() - start_time
                
                start_time = time.time()
                tree_count, tree_positions = search_tree(suffix_tree, query)
                tree_search_time = time.time() - start_time
                
                print(f"Suffix Array: {array_count} matches found in {array_search_time:.6f}s")
                if array_count > 0:
                    print(f"  Positions: {array_positions}")
                
                print(f"Suffix Tree: {tree_count} matches found in {tree_search_time:.6f}s")
                if tree_count > 0:
                    print(f"  Positions: {tree_positions}")

if __name__ == "__main__":
    main()