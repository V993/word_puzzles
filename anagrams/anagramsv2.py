
import time
import enchant
from sys import argv
from itertools import combinations, product

def permutations_and_substrings(letters):

    """

    IDEA!

    l e t t e r s <- permutations
  + l l l l l l l <- letter
  -----------------------------------------
    l e t t e r s [\] ll el tl tl el rl sl <- array of new


    l e t t e r s [\] ll el tl tl el rl sl <- permutations
  + e e e e e e e [\] e  e  e  e  e  e  e  <- letter
  -----------------------------------------
    l e t t e r s [\] le ee te te ee re se [\] ll el tl tl el rl sl [\] lle ele tle tle ele rle sle <- array of new
    """
   
    letters_list = list(letters)

    set_permutations = []

    permutations = []
    permutations.append(letters_list)

    for element in permutations:
        print(element)

    for letter in letters:
        
        array_of_new = []

        for permutation in permutations:
            new_array = []
            for index in permutation:
                new_index = index+letter
                new_array.append(new_index)
                if new_index not in set_permutations and len(new_index) > 2:
                    set_permutations.append(new_index)

            array_of_new.append(new_array)

        permutations += array_of_new 
    
        # print("added",letter)
        # for element in permutations:
        #     print(element)

    return set_permutations



# decpreciated. using combinations instead.
def subsets(letters):
    # return [letters[i:j] for i in range(len(letters)) 
    #                      for j in range(i+1, len(letters)+1)]

    letters = list(letters)

    for length in range(len(letters)+1):
        for subset in combinations(letters,length):
            print(subset)

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


    query_start = time.time()
    queries = permutations_and_substrings(query)
    query_stop = time.time()

    show_permuations = False
    if (len(queries) < 50):
        print()
        print("************************************************")
        print("All words from query:")
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