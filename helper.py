import enchant
import Queue
import random

alph_num_dict = {'a': '2', 'b': '2', 'c': '2',
                 'd': '3', 'e': '3', 'f': '3',
                 'g': '4', 'h': '4', 'i': '4',
                 'j': '5', 'k': '5', 'l': '5',
                 'm': '6', 'n': '6', 'o': '6',
                 'p': '7', 'q': '7', 'r': '7', 's': '7',
                 't': '8', 'u': '8', 'v': '8',
                 'w': '9', 'x': '9', 'y': '9', 'z': '9'}

num_alph_dict = {'2': 'ABC', '3': 'DEF', '4': 'GHI',
                 '5': 'JKL', '6': 'MNO', '7': 'PQRS',
                 '8': 'TUV', '9': 'WXYZ'}

# assumes US phone number is in format 1-xxx-xxx-xxxx where x is a digit
# assumes US wordified phone number is in format 1-xxx-yyyyyyy where x is digit and y is letter
US_phone_num_length = 14
US_wordified_phone_num_length = 13
US_phone_dialing_code = '1'
phone_num_deliminator = '-'
first_deliminator_index = 1
middle_deliminator_index = 5
last_deliminator_index = 9
deliminator_index_diff = 4

def is_US_phone_num_valid(phone_num):
    if len(phone_num) != US_phone_num_length:
        return False
    
    # because US telephone code is 1, position 0 of phone_num should be 1
    if phone_num[0] != US_phone_dialing_code:
        return False
    
    # hyphens should exist in positions 1, 5, and 9
    for i in range(first_deliminator_index, last_deliminator_index + 1, deliminator_index_diff):
        if phone_num[i] != phone_num_deliminator:
            return False
    
    # rest of the phone number should be digits
    for i in range(first_deliminator_index + 1, len(phone_num)):
        if i != middle_deliminator_index and i != last_deliminator_index:
            if phone_num[i] < '0' or phone_num[i] > '9':
                return False

    return True

def is_wordified_US_phone_num_valid(phone_num):
    if len(phone_num) != US_wordified_phone_num_length:
        return False
    
    # because US telephone code is 1, position 0 of phone_num should be 1
    if phone_num[0] != US_phone_dialing_code:
        return False
    
    # hyphens should exist in positions 1 and 5
    for i in range(first_deliminator_index, middle_deliminator_index + 1, deliminator_index_diff):
        if phone_num[i] != phone_num_deliminator:
            return False
    
    # area code should be digits
    for i in range(first_deliminator_index + 1, middle_deliminator_index):
        if phone_num[i] < '0' or phone_num[i] > '9':
            return False
    
    # rest of the phone number should be lowercase alphabet characters
    for i in range(middle_deliminator_index + 1, len(phone_num)):
        if phone_num[i] < 'a' or phone_num[i] > 'z':
            return False

    return True

def words_to_number(wordified_phone_num):
    # lowercase wordified_phone_num before transforming to phone number
    input = wordified_phone_num.lower()

    if not is_wordified_US_phone_num_valid(input):
        print "%s is not a valid US wordified phone number" % wordified_phone_num
        return wordified_phone_num
    
    output = wordified_phone_num[:middle_deliminator_index + 1]

    for i in range(middle_deliminator_index + 1, last_deliminator_index):
        if input[i] in alph_num_dict:
            output += alph_num_dict[input[i]]
    
    output += phone_num_deliminator

    for i in range(last_deliminator_index, len(input)):
        if input[i] in alph_num_dict:
            output += alph_num_dict[input[i]]

    return output

def all_wordifications(phone_num):
    if not is_US_phone_num_valid(phone_num):
        return []

    all_possible_wordifications = []
    q = Queue.Queue()
    us_dict = enchant.Dict("en_US")

    # process first non area phone digit into queue
    first_digit_letters = num_alph_dict[phone_num[middle_deliminator_index + 1]]
    for i in range(len(first_digit_letters)):
        q.put(first_digit_letters[i])

    # process rest of the non-area phone digits by creating all combinations of 7 letter strings
    for i in range(middle_deliminator_index + 2, len(phone_num)):
        local_possible_words = []
        if phone_num[i] in num_alph_dict:
            possible_chars = num_alph_dict[phone_num[i]]
            while not q.empty():
                possible_word = q.get()
                for i in range(len(possible_chars)):
                    local_possible_words.append(possible_word + possible_chars[i])
            for i in range(len(local_possible_words)):
                q.put(local_possible_words[i])

    # check if any 7 letter strings are valid US English words
    while not q.empty():
        word = q.get()
        if us_dict.check(word):
            all_possible_wordifications.append(phone_num[:middle_deliminator_index + 1] + word)
    
    return all_possible_wordifications

def number_to_words(phone_num):
    if not is_US_phone_num_valid(phone_num):
        print "%s is not a valid US phone number" % phone_num
        return phone_num

    all_valid_wordifications = all_wordifications(phone_num)

    # if no valid wordifications exist, return original phone_num
    if not all_valid_wordifications:
        print "%s cannot be converted into any valid US wordified phone numbers" % phone_num
        return phone_num

    # otherwise return random valid wordification from all_valid_wordifications
    rand_index = random.randint(0, len(all_valid_wordifications) - 1)
    return all_valid_wordifications[rand_index]
