
import time
import enchant
from sys import argv
from itertools import combinations

def recursive_permuations(letters, i, length, data):
    if i == length:
        data.append(''.join(letters))
    else:
        for j in range(i,length):
            letters[i],letters[j] = letters[j],letters[i]
            recursive_permuations(letters, i+1, length, data )
            letters[i],letters[j] = letters[j],letters[i]

def get_permuations(letters):
    data = []
    recursive_permuations(list(letters), 0, len(letters), data)
    return data

# TODO: account for up to 3 times every possible letter
# TODO: use combinatorics and not permutation-based approach
def permuations_and_substrings(letters):
    """
    Return all permutations and substrings
    """

    substrings = []
    # starting point is length
    for length in range(1, len(letters)+1):
        # ending point is i
        for i in range(len(letters)-length+1):
            j = i + length -1
            # substring is characters from current starting point to current ending point
            substring = ""
            for k in range(i,j+1):
                substring += letters[k]
            
            # only include substrings longer than 3 characters
            if len(substring) >= 3:
                substrings.append(substring)
    
    all_queries = []
    for entry in substrings:
        all_queries += get_permuations(entry)

    return all_queries

def main():

    start = time.time()

    print()
    print("************************************************")
    print(f"Test started at {start-start}. ")

    d = enchant.Dict("en_US")

    dictionary_built = time.time()

    print()
    print("************************************************")
    print(f"Dictionary built at {dictionary_built-start}")

    print()
    print("************************************************")
    query = argv[1]
    print(f"Using \"{query}\" in tests.")

    queries = permuations_and_substrings(query)

    show_permuations = False
    if (len(queries) < 50):
        print()
        print("************************************************")
        print("All words from query:")
        print("  | name | solutions")
        show_permuations = True

    query_start = time.time()

    answer = []
    for i, query in enumerate(queries):
        if d.check(query) and query not in answer:
            answer.append(query)
        if show_permuations:
            print(i,"|",query,"|",answer)

    query_stop = time.time()

    print()
    print("************************************************")
    print(f"All testing complete at {query_stop-query_start}s.")
    print(f"Total time: {query_stop-start}s.")
    print(f"Solution: {answer}")


if __name__ == "__main__":
    main()