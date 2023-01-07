
import time
import enchant
from sys import argv
from operator import add
from functools import reduce
from itertools import combinations


def all_combinations(letters):
    """
    Given a list of letters, find all possible combinations.
    Returns list of lists. 
    """
    if len(letters) == 0:
        return [[]]
    
    combinations = []
    for c in all_combinations(letters[1:]):
        combinations += [c, c+[letters[0]]]
    
    return combinations

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


def recommend_letters(letters):
    """
    Algorithm to dynamically choose letters to add.
    """
    new_letters = []

    letters = ''.join(sorted(letters))

    # most commonly repeated letters:
    if 'l' in letters and 'll' not in letters:
        new_letters += 'l'
    elif 's' in letters and 'ss' not in letters:
        new_letters += 's'
    elif 'e' in letters and 'ee' not in letters:
        new_letters += 'e'
    elif 't' in letters and 'tt' not in letters:
        new_letters += 't'
    elif 'f' in letters and 'ff' not in letters:
        new_letters += 'f'
    elif 'm' in letters and 'mm' not in letters:
        new_letters += 'm'
    elif 'o' in letters and 'oo' not in letters:
        new_letters += 'o'
    else:
        new_letters += '0'
    
    return new_letters



# TODO: implement this algoriithm with a rotating addition of characters (up to 2)
# in order to account for pangrams longer than the input string size.
def permuations_and_substrings(letters):

    combinations = sorted(all_combinations(letters),key=len)

    # merge arrays in-place and remove smaller than 3 
    i = 0 
    while (i < len(combinations)):
        if len(combinations[i]) < 3:
            combinations.remove(combinations[i])
            i-=1
        combinations[i] = reduce(add,combinations[i])
        i+=1

    all_queries = []
    for combination in combinations:
        all_queries += get_permuations(combination)

    return all_queries

def main():

    start = time.time()

    print()
    print("************************************************")
    print(f"Test started at {start-start}.")

    d = enchant.Dict("en_US")

    dictionary_built = time.time()

    print()
    print("************************************************")
    print(f"Dictionary built in {dictionary_built-start}s.")

    print()
    print("************************************************")
    query = argv[1]
    print(f"Using \"{query}\" and building combinations.")

    # Suggest duplicates: 
    # print("Suggested duplicates:")
    # suggestions = recommend_letters(query)
    # for suggestion in suggestions:
    #     print(f"| {suggestion}", end= " ")
    # print("|")
    # for i in range(len(suggestions)):
    #     print(f"| {i}", end= " ")
    # print("|")

    # Add any characters
    print("Suggested duplicates:")
    for c in query:
        print(f"| {c}", end= " ")
    print("|")
    for i in range(len(query)):
        print(f"| {i}", end= " ")
    print("|")

    print("Add duplicates? (num or enter for none))")
    which_duplicates = input("\t:")

    if which_duplicates != "":
        for duplicate in which_duplicates:
            query += query[int(duplicate)]

    query_start = time.time()
    queries = permuations_and_substrings(query)
    query_stop = time.time()

    print()
    print("************************************************")
    print(f"Preparing to query {len(queries)} words.")

    show_permuations = False
    if (len(queries) < 50):
        print("  | name | solutions")
        show_permuations = True

    answer = []
    for i, query in enumerate(queries):
        if d.check(query) and query not in answer:
            answer.append(query)
        if show_permuations:
            print(i,"|",query,"|",answer)

    answer = sorted(answer,key=len)

    end = time.time()

    print()
    print("************************************************")
    print(f"Query took  : {query_stop-query_start}s.")
    print(f"Total time  : {end-start}s.")
    print(f"Solution    : {answer}")


if __name__ == "__main__":
    main()