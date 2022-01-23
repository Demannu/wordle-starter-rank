from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from wordlist import wordlist
from wordleStarter import WordleStarter
from wordlistHelper import WordlistHelper

app = FastAPI()


## Load wordlist, import from various methods
words = WordlistHelper()
words.load("../resources/sgb.list")
words.combine(wordlist)

starter = WordleStarter(words.words)


@app.get("/")
async def root():
    with open("./views/index.html") as file:
        content = file.read()
        return HTMLResponse(content=content, status_code=200)


@app.get("/calculate/{word}")
async def calculate_word(word):
    if len(word) != 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The length of the word must be 5",
        )

    result = starter.full_calculate(word)
    jsonData = {
        "datapoints": result.data_points,
        "full_correct": result.full_correct,
        "partial_correct": result.partial_correct,
        "none_correct": result.none_correct,
    }
    return JSONResponse(content=jsonData)


@app.get("/compare/{word1}/{word2}")
async def compare_words(word1, word2):
    if len(word1) != 5 or len(word2) != 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The length of the word must be 5",
        )

    result = starter.compare_two_word_efficiency(word1, word2)
    print("RESULT")
    print(result)
    jsonData = {
        "word1": word1,
        "word2": word2,
        "full_correct": result["full_correct"],
        "partial_correct": result["partial_correct"],
        "none_correct": result["none_correct"],
    }
    return JSONResponse(content=jsonData)
    pass
