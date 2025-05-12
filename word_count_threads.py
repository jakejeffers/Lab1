import threading # Import threading for parallel processing
from collections import Counter # Import Counter for counting word frequencies
import sys # Import sys for command line arguments

# Thread worker function
def count_words(segment, results, index): # This function will be run in a separate thread
    words = segment.split()
    word_count = Counter(words) # Count words in the segment
    results[index] = word_count
    print(f"Thread {index} intermediate count:\n{word_count}\n") # Print intermediate count for debugging

def main(file_path, num_segments): # Main function to read file and count words
    # Read entire file content
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Split into segments
    segment_size = len(text) // num_segments
    segments = []
    start = 0

    for i in range(num_segments): # Split text into segments
        end = start + segment_size
        if i == num_segments - 1:  # last segment takes the rest
            end = len(text)
        segments.append(text[start:end])
        start = end

    # Shared list to store thread results
    results = [None] * num_segments
    threads = []

    for i in range(num_segments): # Create and start threads
        thread = threading.Thread(target=count_words, args=(segments[i], results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Consolidate results from all threads
    final_count = Counter()
    for partial_count in results:
        final_count.update(partial_count)

    print("Final word frequency count:")
    print(final_count)

if __name__ == "__main__": # Entry point for the script
    # Check for correct number of command line arguments
    if len(sys.argv) != 3:
        print("Usage: python word_count_threads.py <file_path> <num_segments>")
    else:
        file_path = sys.argv[1]
        num_segments = int(sys.argv[2])
        main(file_path, num_segments)
