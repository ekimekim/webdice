import re
import os

from flask import Flask, session, request, redirect

from room import Room

app = Flask(__name__)
app.secret_key = os.urandom(24)

rooms = {}
html_template = "<html><body>{}</body></html>"
rollspec_pattern = re.compile(r"^([0-9]+)d([0-9]+)([+-][0-9]+)?$")

DEBUG = True
STATIC_HOMEPAGE = """
<form method="post">
Room: <input type="text" name="room"><br>
Name: <input type="text" name="user"><br>
<input type="submit" value="Go to room">
</form>
"""

def getroom(name):
	if name not in rooms:
		rooms[name] = Room(name)
	return rooms[name]

@app.route('/', methods=['GET','POST'])
def homepage():
	if request.method == 'POST':
		session['user'] = request.form['user']
		return redirect("/{}".format(request.form['room']))
	return STATIC_HOMEPAGE

@app.route('/<room>', methods=['GET'])
def displayroom(room):
	"""Create room if doesn't exist. Return room contents."""
	return html_template.format(getroom(room).render())

@app.route('/<room>/roll', methods=['POST'])
def roll(room):
	user = session['user']
	rollspec = request.form['rollspec']
	match = rollspec_pattern.match(rollspec)
	try:
		if not match: raise ValueError()
		n, sides, bonus = match.groups()
		if not bonus: bonus = 0
		n, sides, bonus = map(int, (n, sides, bonus))
		if n < 0 or sides < 0: raise ValueError()
		if n > 100: raise ValueError()
	except ValueError:
		return "Bad rollspec", 400
	roll = getroom(room).roll(user, n, sides, bonus)
	return html_template.format(roll.render())


if __name__=='__main__':
	app.run(debug=DEBUG)
