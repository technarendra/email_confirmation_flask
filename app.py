from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import socket
import http.client
import datetime

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'indore.narendra@gmail.com',
    MAIL_PASSWORD = 'R*******@12345',
    MAIL_DEBUG = True,
    MAIL_SUPPRESS_SEND = False,
    TESTING = False
)



mail = Mail(app)

# app.config.from_pyfile('config.cfg')


s = URLSafeTimedSerializer('Thisisasecret!')




@app.route('/', methods=['GET', 'POST'])
def index():
	print (socket.gethostname())
	if request.method == 'GET':
		return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
	
	email = request.form['email']
	token = s.dumps(email, salt='email-confirm')
	msg = Message('confirm_email', sender='indore.narendra@gmail.com', recipients=[email])
	link = url_for('confirm_email', token=token, _external=True)
	msg.body = 'Your link is {}.'.format(link)
	mail.send(msg)
	
	return '<h1>The email you entered is {}. The toekn is {}</h1>'.format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
	try:
		email = s.loads(token, salt='email-confirm', max_age=60)
	except SignatureExpired:
		return '<h1> The token is expired! </h1> '
	return '<h1>The token works!<h1>'





if __name__=='__main__':
	app.run (host = "127.0.0.1", port = 5000)
	# app.run(debug=True)
