
import time
import math
import enchant
import multiprocessing
from sys import argv
from tqdm import trange, tqdm

def get_combinations(letters, gold):

    combinations = recursive_combinations(letters)

    # filter for only gold combinations
    exclusive_combinations = set()

    [exclusive_combinations.add("".join(sorted(combination))) for combination in combinations if gold in combination and len(combination) >= 4]

    return list(exclusive_combinations)

def recursive_combinations(letters):
    """
    Given a list of letters, find all possible combinations.
    Returns list of lists. 
    """
    if len(letters) == 0:
        return [[]]
    
    combinations = []
    for c in recursive_combinations(letters[1:]):
        combinations += [c, c+[letters[0]]]
    
    return combinations

def recursive_permutations(s):
    # Given a string s, returns all possible permutations of the string, for a total of len(s)!
    if len(s) == 1:
        return [s]
    else:
        perms = []
        for i, c in enumerate(s):
            for perm in recursive_permutations(s[:i] + s[i+1:]):
                perms.append(c + perm)
        return perms
    
def duplicate_chars(string):
    # Returns a list of all combinations of three characters from the original string.
    # resultant list will be iteratively appended to all combinations to create more
    # permutations inlcuding duplicates.

    all_duplicate_chars = set()

    # for i in range(len(string)):
    #     # for j in range(len(string)):
    #         # for k in range(len(string)):
    #             duplicate_chars = "".join(sorted(string[i]))#+string[k]))
    #             all_duplicate_chars.add(duplicate_chars)
    
    return all_duplicate_chars

def add_duplicates(combination, duplicate_strings):
    # given a string combination and an array of duplicate strings, returns a list of
    # new combinations including all possible duplicate strings.
    new_combinations = set()
    for duplicate in duplicate_strings:
        new_combinations.add("".join(sorted(combination+duplicate)))
    return new_combinations

def parallelized_permutations(combinations,letters):
    # Given an array of strings, find all possile permutations of each string, appending 
    # all permutations of all strings to a permutations array.
    all_permutations = []
    with multiprocessing.Pool() as pool:
        # pool.map takes a recursive function and an array of values to call the function.
        # the recursive_permutations function will return an array of permutations which will
        # need to be aggregated. pool.map executes all calls concurrently in this line, no
        # strings attached.
        
        # Get two duplicate chars to add to each combination 
        all_duplicates = duplicate_chars(letters)
        all_new_combinations = set()
        for combination in combinations:
            new_combinations = add_duplicates(combination, all_duplicates)
            all_new_combinations.update(new_combinations)

        # print(f"number of original combinations: {len(combinations)}")
        combinations += (list(all_new_combinations))
        # print(f"total number of combinations: {len(combinations)}")
        # print("Getting permutations...")

        results = pool.map(recursive_permutations, combinations)

    [ all_permutations.extend(result) for result in results ]
    return list(set(all_permutations))
        
def get_num_permutations(a):
    # Given an array a, checks all string lengths and gets the number of permutations for all substrings
    total_perms = 0
    for s in a:
        permutations = math.factorial(len(s))
        total_perms += permutations
    
    return total_perms

def check_if_word(args):
    d, word = args
    return d.check(word)

def add_if_word(args):
    d, word = args
    if d.check(word):
        return word
    return None

def get_words(letters, gold):

    # start = time.time()
    # print(f"Getting combinations for string of len: {len(letters)}.")
    # 10 possible combinations for a 7 letter string including all strings of len >4
    combinations = get_combinations(letters, gold)
    # print(f"Combinations: {combinations}")
    # end = time.time()

    # print(f"Took {end-start}")
    # print(f"\tGetting all permuations for all {len(combinations)} combinations.")
    # print(f"Evaluating the sum of each substring's length factorial, the number of permutations will be: {get_num_permutations(combinations)}")

    # start = time.time()
    # 6936 possible permutations of all 10 substrings
    all_permutations = parallelized_permutations(combinations,letters)

    # end = time.time()

    # print("\tNumber of permutations:", len(all_permutations), "Preparing to query english dictionary.")
    
    # Recursive can handle ~4-5 million combinations within 5 seconds
    # [(all_permutations.extend(recursive_permutations(combination))) for combination in combinations]

    d = enchant.Dict("en_US")

    # start = time.time()

    answer = []

    # concurrently check each permutation in the dictionary
    with multiprocessing.Pool() as pool:
        args = [(d, permutation) for permutation in all_permutations]
        answer = pool.map(add_if_word, args)
    
    # end = time.time()

    # print(f"Took: {end-start}")
    # remove None entries and filter by length
    return sorted(filter(lambda item: item is not None, answer), key=len)

def main():
    letters = "blmiepa" 
    gold = 'i'
    debug = True

    answer = set()

    # start = time.time()
    # answer = sorted(get_words(letters, gold))
    # end = time.time()

    start = time.time()
    for i in trange(49, leave=False):
        letter1 = letters[i//7]
        letter2 = letters[i%7]
        if debug:
            tqdm.write(f"Iteration {i}\t:\tquerying   '{letter1+letter2}'")
        words = get_words(letters + letter1 + letter2, gold)
        for word in words: 
            answer.add(word)
    end = time.time()

    print(f"Took {end-start}")
    print(sorted(answer))

if __name__ == "__main__":
    main()