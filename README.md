# asapp

Instructions:

1. set directory for a virtual environment with flask. Here's a simple command list.

$ virtualenv flask
New python executable in flask/bin/python
Installing setuptools............................done.
Installing pip...................done.
$ flask/bin/pip install flask

2. run app.py
./app.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader

3. run search. the command structure is 'http://localhost:5000/search/'search term'
where search term is of the format "this+and+that"

results should look like the following format:

curl http://localhost:5000/search/'i+can'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 155
Server: Werkzeug/0.10.4 Python/2.7.6
Date: Tue, 14 Jul 2015 15:24:43 GMT

{
  "results": [
    "I can assist you", 
    "I can help you", 
    "I can assist you with this", 
    "I can help you with this", 
    "I can help"
  ]
}


