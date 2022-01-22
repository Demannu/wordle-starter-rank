from wordlist import wordlist
from random import randint


class WordleHelper:
    def __init__(self, wordlist):
        if len(wordlist) < 1:
            raise ValueError('The wordlist is empty!')

        self.wordlist = wordlist
        self.attempts = []

    def pick(self):
        choice = randint(0, len(self.wordlist))
        return self.wordlist[choice]

    def average(self):
        results = {
            "full_correct": 0,
            "partial_correct": 0,
            "none_correct": 0
        }

        if len(self.attempts) == 0:
            return results

        total = len(self.attempts) * 5

        for attempt in self.attempts:
            results["full_correct"] += attempt["full_correct"]
            results["partial_correct"] += attempt["partial_correct"]
            results["none_correct"] += attempt["none_correct"]
        for result in results:
            results[result] = results[result] / total

        return results

    def random_calculate(self, word):
        if len(word) != 5:
            raise ValueError('Your word is not 5 characters long!')

        random_word = self.pick()
        self.attempts.append(self.compare(word, random_word))
        return self.attempts

    def full_calculate(self, user_word):
        if len(user_word) != 5:
            raise ValueError('Your word is not 5 characters long!')

        self.attempts = []
        for word in self.wordlist:
            self.attempts.append(self.compare(user_word, word))

        return self.average()

    def compare(self, user_word, picked):
        result = {
            "full_correct": 0,
            "partial_correct": 0,
            "none_correct": 0
        }

        for i, v in enumerate(user_word):
            if picked[i] == v:
                result["full_correct"] += 1
            elif v in picked:

                result["partial_correct"] += 1
            else:
                result["none_correct"] += 1
        return result

    def compare_two_word_efficiency(self, word1, word2):
        word1_results = self.full_calculate(word1)
        word2_results = self.full_calculate(word2)
        if word1_results is None or word2_results is None:
            raise BaseException(
                'There has been an issue calculating one of the words, please check your inputs')

        difference = {
            "word1": word1,
            "word2": word2,
            "full_correct": word1_results["full_correct"] - word2_results["full_correct"],
            "partial_correct": word1_results["partial_correct"] - word2_results["partial_correct"],
            "none_correct": word1_results["none_correct"] - word2_results["none_correct"]
        }
        return difference

    def display_two_word_efficiency(self, word1, word2):
        difference = self.compare_two_word_efficiency(word1, word2)
        return f"The difference between {word1} and {word2}\nFull Correct: {difference['full_correct']:.2%}\nPartial Correct:{difference['partial_correct']:.2%}\nNone Correct:{difference['none_correct']:.2%}"
