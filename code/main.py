from db import db, session, Base
from wordleStarter import WordleStarter
from wordlistHelper import WordlistHelper
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse

from models.words import Words

app = FastAPI()

## Create tables
Base.metadata.create_all(db)

## Load wordlist, import from various methods
words = WordlistHelper()
words.load("./resources/wordle-answers.list")
words.load("./resources/wordle-allowed.list")

## Initialize helper class
starter = WordleStarter(words.words)


@app.get("/")
async def root():
    with open("./views/index.html") as file:
        content = file.read()
        return HTMLResponse(content=content, status_code=200)


@app.get("/calculate/{word}")
async def calculate_word(word):
    word = word.lower()

    ## We now verify if the word is a real word
    if not starter.check_wordlist(word):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The word {word} does not exist in the wordlist",
        )

    ## Verify if word is actually 5 characters long
    if len(word) != 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The length of the word must be 5",
        )

    if Words.check_db(word):
        result = Words(word=word).get_from_db()
    else:
        result = starter.full_calculate(word)
        Words(word=word).add_to_db(result)
    jsonData = {
        "full_correct": result.full_correct,
        "partial_correct": result.partial_correct,
        "none_correct": result.none_correct,
        "score": result.score,
    }
    return JSONResponse(content=jsonData)


@app.get("/compare/{word1}/{word2}")
async def compare_words(word1, word2):
    ## We now verify if the words are real
    if not starter.check_wordlist(word1) or not starter.check_wordlist(word2):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The word does not exist in the wordlist",
        )

    word1 = word1.lower()
    word2 = word2.lower()
    if len(word1) != 5 or len(word2) != 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The length of the word must be 5",
        )

    result = starter.compare_two_word_efficiency(word1, word2)
    jsonData = {
        "word1": word1,
        "word2": word2,
        "full_correct": result["full_correct"],
        "partial_correct": result["partial_correct"],
        "none_correct": result["none_correct"],
        "score": result["score"],
    }
    return JSONResponse(content=jsonData)


@app.get("/highscore")
async def highscore():
    top_words = Words.get_highest_scores("full_correct")
    top_words = [
        {
            "word": value.word,
            "full_correct": value.full_correct,
            "partial_correct": value.partial_correct,
            "none_correct": value.none_correct,
            "score": value.score,
        }
        for value, in top_words
    ]
    return JSONResponse(content=top_words)
