import requests
from bs4 import BeautifulSoup
from functools import partial
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime  # Importa il modulo datetime
import os
import logging

# -*- coding: utf-8 -*-

app = Flask(__name__, static_url_path='/static')

# Configura la chiave segreta per le sessioni
app.secret_key = os.urandom(24)

def load_neg_words(file_path):
    with open(file_path, 'r') as file:
        neg_words = [word.strip() for word in file.readlines()]
    return neg_words

def load_exclude_words(file_path):
    with open(file_path, 'r') as file:
        exclude_words = [word.strip() for word in file.readlines()]
    return exclude_words

def calculate_percentage(total, count):
    if total == 0:
        return 0
    return (count / total) * 100

def is_article_title_h_tag(tag, url):
    # For "repubblica.it", we only want to consider <h2> and <h3> tags as article titles.
    if "repubblica.it" in url.lower():
        return tag.name in ['h2', 'h3']

    # For "corriere.it", we want to consider <h2>, <h3>, and <h4> tags as article titles.
    if "corriere.it" in url.lower():
        return tag.name in ['h2', 'h3', 'h4']

    # For other sites, include <h1> along with <h2> and <h3> tags as article titles.
    return tag.name in ['h1', 'h2', 'h3']

def is_article_title_div(div_tag):
    # Personalize this function based on the specific characteristics of article title divs on the website you are analyzing
    # You can check for attributes, classes, or other characteristics that are common in article titles
    class_list = div_tag.get('class', [])
    return 'title' in class_list or 'article-title' in class_list or 'fp_newsbox__title' in class_list or 'fp_newsbox' in class_list or 'fp_newsbox--breaking' in class_list

def analyze_website(url, neg_words, exclude_words, num_titles):
    if not url.startswith("https://"):
        url = "https://" + url

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', recursive=True)

        is_article_title_h_tag_with_url = partial(is_article_title_h_tag, url=url)
        h_tags = soup.find_all(is_article_title_h_tag_with_url)

        title_divs = [div for div in divs if is_article_title_div(div)]
        div_titles = [title_div.text.strip() for title_div in title_divs]

        h_titles = [h_tag.text.strip() for h_tag in h_tags]

        all_titles = div_titles + h_titles

        return [title for title in all_titles if not any(exclude_word.lower() in title.lower() for exclude_word in exclude_words)][:num_titles]

    except requests.exceptions.RequestException as e:
        print("Error fetching the website:", e)
        return None

def analyze_website_user_defined(url, neg_words, exclude_words, num_titles):
    titles = analyze_website(url, neg_words, exclude_words, num_titles)
    if titles:
        total_titles = len(titles)
        neg_title_count = 0

        log_data = []
        for title in titles:
            neg_words_found = [word for word in neg_words if word.lower() in title.lower()]
            #title = title.encode("latin-1").decode("utf-8")  # Decodifica il titolo come UTF-8
            log_data.append({"title": title, "neg_words": neg_words_found})
            if neg_words_found:
                neg_title_count += 1

        return total_titles, neg_title_count, log_data

    return None, None, None

def create_log_file(log_data):
    with open("log.txt", "w", encoding="utf-8") as file:
        for entry in log_data:
            file.write(f"Title: {entry['title']}\n")
            file.write(f"Negative words found: {', '.join(entry['neg_words'])}\n\n")

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        website_url = request.form["website_url"]
        num_titles = int(request.form["num_titles"])

        try:
            num_titles = int(num_titles)
            if num_titles <= 0:
                raise ValueError("Il numero di titoli deve essere maggiore di zero.")
        except ValueError as e:
            flash(str(e))  # Aggiungi il messaggio di errore alla variabile di contesto flash
            return redirect(url_for("homepage"))

        total_titles, neg_title_count, log_data = analyze_website_user_defined(website_url, neg_words, exclude_words, num_titles)

        if total_titles is not None and neg_title_count is not None and log_data is not None:
            percentage = calculate_percentage(total_titles, neg_title_count)
            create_log_file(log_data)

            # Salva i risultati nella sessione di Flask
            session["total_titles"] = total_titles
            session["neg_title_count"] = neg_title_count
            session["percentage"] = percentage
            session["log_data"] = log_data

            # Effettua un redirect alla rotta "/results"
            return redirect(url_for("show_results"))

    return render_template("homepage.html")

@app.route("/results")
def show_results():
    # Recupera i risultati dalla sessione di Flask
    total_titles = session.get("total_titles")
    neg_title_count = session.get("neg_title_count")
    percentage = session.get("percentage")
    log_data = session.get("log_data", [])

    # Cancella i dati dalla sessione dopo averli recuperati
    session.pop("total_titles", None)
    session.pop("neg_title_count", None)
    session.pop("percentage", None)
    session.pop("log_data", None)

    if total_titles is None or neg_title_count is None or percentage is None:
        # Se non ci sono risultati nella sessione, reindirizza l'utente alla homepage
        return redirect(url_for("homepage"))

    return render_template("results.html", version=datetime.now().timestamp(), total_titles=total_titles, neg_title_count=neg_title_count, percentage=percentage, log_data=log_data)

if __name__ == "__main__":
    neg_words_file_path = "neg.txt"  # Replace with the path to your neg.txt file
    neg_words = load_neg_words(neg_words_file_path)

    exclude_words_file_path = "exclude.txt"  # Replace with the path to your exclude.txt file
    exclude_words = load_exclude_words(exclude_words_file_path)

    logging.basicConfig(level=logging.DEBUG)  # Imposta il livello di registrazione del log a DEBUG
    # Imposta l'indirizzo IP e la porta su cui l'applicazione sarà in ascolto
    # In questo esempio, ascolteremo su localhost (127.0.0.1) e 192.168.1.119 sulla porta 5000
    app.run(host='0.0.0.0', port=5000)
