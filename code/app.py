from wordlist import wordlist
from wordlistHelper import WordlistHelper
from wordleStarter import WordleStarter


## Load wordlist, import from various methods
words = WordlistHelper()
words.load("./resources/sgb.list")
words.combine(wordlist)

starter = WordleStarter(words.words)
print(starter.display_two_word_efficiency("whore", "stare"))
