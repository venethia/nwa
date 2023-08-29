# Negative Words Analyzer (How to deal with online negativity)

I created this simple app to scan the titles of italian news websites before visit them and see if it's worth it.

Negative news impact on our mental health and we need to be very selective.

Researchers and scientists report many dangerous effects of reading negative news (not only on social media), such as: anxiety, depression, information overload, lack of online safety, invasion of privacy, deception, conflicts and more.

<h2>Technical details</h2>

You can build your own list of negative words by editing the file neg.txt

Tha app isn't perfect, so you can edit the file exclude.txt if to not scan the titles that contain some words (ex. titles of news categories).

This app was built with Python3, HTML, CSS.

If you don't have a personal server, you can buy a basic plan of <a href="https://www.pythonanywhere.com">Python Anywhere</a> (Free plan blocks websites scan).

Tested on Debian 11 and Ubuntu 22.04.

You don't need a webserver.

To start the app in background: <code>sudo nohup python3 app.py &</code>

A file log.txt will be generated.

<h2> How to use the app</h2>

- Insert the URL of the site
- Insert the number of the titles to analyze (if you insert 10, only the first 10 titles will be analyzed).

<h2>Note</h2>

Pay attention: I'm not a full time developer, so the app was created for personal use and may contains errors. Feel free to fork and make changes.

<h2>Contacts:</h2> 

Email: nwa(dot)matteospigolon(dot)com


