# It's more efficient to check every letter against every word in the dictionary than it is to
# generate every possible word from the given letters...

from sys import argv

def get_dict():
    # path_to_dict = "/usr/share/dict/web2" # in-built mac dictionary
    path_to_dict = "/Users/v99352/Documents/code/word_puzzles/anagrams/words.txt"
    with open(path_to_dict, "r") as f:
        dictionary = f.readlines()
    return dictionary

def get_letter_count_dict(letters):
    return {letter:0 for letter in letters}

def parse_dictionary(dictionary, letters, gold):
    """
    Returns a list of words that include the specified letters,
    the specified gold letter, and are greater than len 3.
    Returns an additonal list with pangrams, which include 
    ALL specified letters.

    Iteratively checks each word in the gutenberg dictionary
    to see if any words include all of the specified letters.
    """

    answer = []
    pangrams = []

    for dict_word in dictionary:
        dict_word = "".join((dict_word.strip().lower()))
        valid = True

        if len(dict_word) < 4 or gold not in dict_word:
            continue

        letter_counts = get_letter_count_dict(letters)

        # check if all dict_word letters are in the query letters:
        for dict_letter in dict_word:
            if dict_letter not in letters:
                valid = False
                break
            letter_counts[dict_letter] += 1
        
        if valid: 
            if 0 not in letter_counts.values(): # if pangram, add to pangrams
                pangrams.append(dict_word)
            # else: # otherwise add to matching words
            answer.append(dict_word)

    return sorted(answer,key=len), sorted(pangrams,key=len)



def main():

    if len(argv) < 2:
        print("\n[ERR] No parameters passed.")
        print("\tUsage: \n\t   - anagrams [letters] [gold_letter]\n\t   - anagrams [letters] (with gold letter last)")
        print()
        quit()
    
    letters = argv[1]
    gold = argv[1][-1]

    if len(argv) == 3:
        gold = argv[2]
    

    print("\n\t[IMPORTANT] \n\t   This script uses Webster's Unabridged Dictionary (https://www.gutenberg.org/ebooks/29765) \n\t   The dictionary was last updated on Sept. 5 2023. ")


    answer, pangrams = parse_dictionary(get_dict(), letters, gold)
    print(f"\n\tSOLUTIONS : {answer}")
    print(f"\n\tPANGRAMS  : {pangrams}")
    print()



if __name__ == "__main__":
    main()