from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

# fake data base : 웹 생성 과정에서 매번 데이터를 오랜 시간 검색 결과물을 보기엔 오래 걸리므로 이와 같이 react로 미리 검색해둔 것을 저장해두는?
db = {}


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
        # jobs = get_jobs(word)
        # db[word] = jobs
        print(jobs)
    else:
        return redirect("/")
    return render_template("report.html",
                           searchingBy=word,
                           resultsNumber=len(jobs),
                           jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")


# @app.route("/<username>")
# def potato(username):
#   return f"Hello {username}! How are you?"

app.run(host="0.0.0.0")
# host="0.0.0.0"은 replit 환경에서 작업하기 때문에 넣어줌
