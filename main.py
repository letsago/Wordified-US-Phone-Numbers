from helper import *

tests = [
            ["1-800-724-6837", ["1-800-PAINTER"]],  # only one valid wordification 
            ["1-800-784-9937", ["1-800-QUIZZER", "1-800-QUIZZES"]],  # multiple valid wordifications
            ["1-800-999-9999", ["1-800-999-9999"]], # no valid wordifications 
            ["93342", ["93342"]],                   # not a valid US phone number 
        ]

for test in tests:
    assert(number_to_words(test[0]) in test[1])
    for wordification in test[1]:
        assert(test[0] == words_to_number(wordification))