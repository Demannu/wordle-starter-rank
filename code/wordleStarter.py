from wordlist import wordlist
from random import choice
from collections import Counter


class Results:
    def __init__(self):
        self.full_correct = 0
        self.partial_correct = 0
        self.none_correct = 0
        self.data_points = 0

    def __iadd__(self, other):
        self.full_correct += other.full_correct
        self.partial_correct += other.partial_correct
        self.none_correct += other.none_correct
        self.data_points += 1
        return self

    def __sub__(self, other):
        self.full_correct -= other.full_correct
        self.partial_correct -= other.partial_correct
        self.none_correct -= other.none_correct
        return self

    def __str__(self):
        return f"(datapoints: {self.data_points}, full_correct: {self.full_correct}, partial_correct: {self.partial_correct}, none_correct: {self.none_correct}"

    def __repl__(self):
        return f"Results({self.full_correct},{self.partial_correct},{self.none_correct},{self.data_points}"

    def average(self):
        total = self.data_points * 5
        self.full_correct /= total
        self.partial_correct /= total
        self.none_correct /= total
        return self


class WordleStarter:
    def __init__(self, wordlist):
        if len(wordlist) < 1:
            raise IndexError("The wordlist is empty!")
        self.wordlist = wordlist
        self.attempts = []

    def pick(self):
        return choice(self.wordlist)

    def average(self):
        results = Results()
        total = len(self.attempts) * 5

        if total == 0:
            return results

        for attempt in self.attempts:
            results += attempt

        results.average()
        return results

    def random_calculate(self, word):
        if len(word) != 5:
            raise ValueError("Your word is not 5 characters long!")

        random_word = self.pick()
        self.attempts.append(self.compare(word, random_word))
        return self.attempts

    def full_calculate(self, user_word):
        if len(user_word) != 5:
            raise ValueError("Your word is not 5 characters long!")
        self.attempts = []
        for word in self.wordlist:
            self.attempts.append(self.compare(user_word, word))
        return self.average()

    def compare(self, user_word, picked):
        result = Results()
        for i, v in enumerate(user_word):
            if picked[i] == v:
                result.full_correct += 1
            elif v in picked:
                result.partial_correct += 1
            else:
                result.none_correct += 1
        return result

    def compare_two_word_efficiency(self, word1, word2):
        word1_results = self.full_calculate(word1)
        word2_results = self.full_calculate(word2)
        if word1_results is None or word2_results is None:
            raise Exception(
                "There has been an issue calculating one of the words, please check your inputs"
            )
        final = word1_results - word2_results
        difference = {
            "word1": word1,
            "word2": word2,
            "full_correct": final.full_correct,
            "partial_correct": final.partial_correct,
            "none_correct": final.none_correct,
        }
        return difference

    def display_two_word_efficiency(self, word1, word2):
        difference = self.compare_two_word_efficiency(word1, word2)
        return f"The difference between {word1} and {word2}\nFull Correct: {difference['full_correct']:.2%}\nPartial Correct:{difference['partial_correct']:.2%}\nNone Correct:{difference['none_correct']:.2%}"

    def display_full_calculate(self, word1):
        result = self.full_calculate(word1)
        return f"Wordle Starter Efficiency: ({word1})\nFull Correct: {result.full_correct:.2%}\nPartial Correct: {result.partial_correct:.2%}\nNone Correct: {result.none_correct:.2%}"
