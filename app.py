from flask import Flask, render_template, request, redirect, url_for
import random
from linecache import getline
import os
import json

app = Flask(__name__)
choicesnum = 976

def load_choices():
    id1, id2 = random.sample(range(choicesnum), 2)
    tag1, tag2 = getline("id_to_tag.txt", id1+1).split(" - ")[1][:-1], getline("id_to_tag.txt", id2+1).split(" - ")[1][:-1]
    choice1, choice2 = [], []
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, f"database/items/{tag1}.txt"), 'r', encoding='windows-1251') as f:
        f.readline()
        choice1.append(f.readline().split(": ")[1][:-1])
        choice1.append(f"/static/images/{tag1}.jpg")
        x = f.readline().split(": ")[1]
        if x == x[:99]:
            choice1.append(x)
        else:
            choice1.append(x[:99] + '...')
        choice1.append(id1)

    with open(os.path.join(script_dir, f"database/items/{tag2}.txt"), 'r', encoding='windows-1251') as f:
        f.readline()
        choice2.append(f.readline().split(": ")[1][:-1])
        choice2.append(f"/static/images/{tag2}.jpg")
        x = f.readline().split(": ")[1]
        if x == x[:99]:
            choice2.append(x)
        else:
            choice2.append(x[:99] + '...')
        choice2.append(id2)
    return choice1, choice2    #[name, imagepath, info, id]

def log_choice(win, lose):
    with open('results.json', 'r') as f:
        players = json.load(f)

    if win in players and lose in players:
        players[win]['w'] += 1
        players[lose]['l'] += 1

    with open('results.json', 'w') as f:
        json.dump(players, f)

@app.route('/')
def index():
    x = load_choices()
    return render_template('index.html', choice1=x[0], choice2=x[1], count=0)

@app.route('/choose', methods=['POST'])
def choose():
    win = request.form['choice+']
    lose = request.form['choice-']
    count = int(request.form['count']) + 1

    log_choice(win, lose)

    # Получаем новые варианты
    x = load_choices()
    return render_template('index.html', choice1=x[0], choice2=x[1], count=count)

if __name__ == '__main__':
    app.run(debug=True, port=8001)