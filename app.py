from flask import Flask, request, redirect
from twilio import twiml
import requests
import json

app_id = 'd595965d'
app_key = '0145ffbeaab3f5a9c11d837d30d9e9e3'

language = 'en'

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
	number = request.form['From']
	message_body = request.form['Body']
	option = message_body.split(' ', 1)[0].lower()

	if(option == 'options'):
		resp = twiml.Response()
		resp.message('The options are:\n- define [word]: to define a word\n- options: to show options\n- library: to see all books\n- read [bookname]: to read a book')
		return str(resp)
	elif(option == 'define'):
		define_this_word = message_body.split(' ', 1)[1]

		word_id = define_this_word

		url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() + '/definitions'

		r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

		definition = json.dumps(r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0])

		resp = twiml.Response()
		resp.message('{} :\n {}.'.format(define_this_word.upper(), definition))
		return str(resp)
	elif(option == 'library'):
		resp = twiml.Response()
		resp.message('Library List:\nNothing at the moment.')
		return str(resp)
	elif(option == 'read'):
		bookname = message_body.split(' ', 1)[1]
		resp = twiml.Response()
		resp.message('{}:\n is the book you want to read.'.format(bookname))
		return str(resp)
	else:
		resp = twiml.Response()
		resp.message('An error occurred. To see the options, message OPTIONS.')
		return str(resp)

if __name__ == "__main__":
	app.run(debug=True)
