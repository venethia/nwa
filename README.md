# Negative Words Analyzer (How to deal with online negativity)

I created this simple app to scan the titles of Italian news websites before visiting them and see if it's worth it.

Negative news impacts our mental health and we need to be very selective.

Researchers and scientists report many dangerous effects of reading negative news (not only on social media), such as anxiety, depression, information overload, lack of online safety, invasion of privacy, deception, conflicts, and more.

<h2>Technical details</h2>

You can build your list of negative words by editing the file neg.txt

The app isn't perfect, so you can edit the file exclude.txt to not scan the titles that contain some words (e.g. titles of news categories).

This app was built with Python3 (Flask), HTML, and CSS.

If you don't have a personal server, you can buy a basic plan of <a href="https://www.pythonanywhere.com" target="_blank">Python Anywhere</a> (The free plan blocks website scan).

Tested on Debian 11 and Ubuntu 22.04.

You don't need a web server.

To start the app in the background: <code>sudo nohup python3 app.py &</code>

A file log.txt will be (re)generated after every scan.

<h2> How to use the app</h2>

- Open your browser: <code>http://yourserverip:5000</code>
- Insert the URL of the site
- Insert the number of the titles to analyze (if you insert 10, only the first 10 titles will be analyzed).

<h2>Screenshots</h2>

![immagine](https://github.com/venethia/nwa/assets/95854664/38db62e1-14de-43af-8b1b-20d2692dac5f)

![nwascreen2](https://github.com/venethia/nwa/assets/95854664/6e73b3c2-51f2-4a0d-9adb-50b447af990e)

<h2>Note</h2>

The app was created for personal use and may contain errors. 

Feel free to fork it and make changes.

The logo is a dystopian image randomly generated by A.I. and it has no meaning.

<h2>Contacts:</h2> 

Email: nwa(dot)matteospigolon(dot)com


