import time
import random
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
# make sure to import all of these libraries to make the code work

def wpm(words, seconds):
    mins,secs = divmod(seconds, 60)
    tmin = mins + (secs/60)
    return int(words/tmin)

def inac(correct, total):
    percent = (correct/total)
    return round(percent*100)

def gen_words():
    web = requests.get("http://www.mieliestronk.com/corncob_lowercase.txt")
    soup = BeautifulSoup(web.text, 'html.parser')
    english_words = list(soup)[0].strip("\r").split()
    select = random.choice(english_words)
    return select

def plot(file_name):
    file = open(file_name, "r")
    text = file.read()
    stats = text.split("\n")
    del stats[len(stats) - 1]
    new_stats = []
    for score in stats:
        stat = score.split()
        new_stats.append(stat)
    new_stats = np.array(new_stats)
    new_stats = new_stats.T
    new_stats = list(new_stats)
    wpm, ac = new_stats
    wpm = [int(x) for x in wpm]
    ac = ["Test #" + str(pos + 1) + ": " + num + "%" for pos, num in enumerate(ac)]
    ypos = np.arange(len(ac))
    plt.xticks(ypos, ac)
    plt.bar(ypos, wpm)
    plt.show()

def main(length):
    name = input("What is your name?\n")
    file_name = name + ".txt"
    file = open(file_name, "ab")
    total = 0
    count = 0
    start = time.time()
    end = time.time()
    inp = None
    word = None
    while int(end - start) <= length:
        word = gen_words()
        inp = input(word + "\n")
        if str(inp) == word:
            count += 1
        total += 1
        end = time.time()
    if str(inp) == word:
        count -= 1
    file.write(bytes(str(wpm(count, length - total*1.75)) + " " + str(inac(count, total - 1)) + "\n", "UTF-8"))
    file.close()
    plot(file_name)

main(60) # you can choose how many seconds you want, default is 60
