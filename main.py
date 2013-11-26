from flask import Flask

from room import Room

app = Flask(__name__)

rooms = {}
html_template = "<html><body>{}</body></html>"

DEBUG = True
STATIC_HOMEPAGE = """
placeholder
""" # TODO

def getroom(name):
	if name not in rooms:
		rooms[name] = Room(name)
	return rooms[name]

@app.route('/')
def homepage():
	return STATIC_HOMEPAGE

@app.route('/<name>', methods=['GET'])
def displayroom(name):
	"""Create room if doesn't exist. Return room contents."""
	return html_template.format(getroom(name).render())

@app.route('/<name>/roll', methods=['POST'])
def roll(name):
	n, sides, bonus = 1, 6, 0 # TODO get args from user
	roll = getroom(name).roll(n, sides, bonus)
	return html_template.format(roll.render())


if __name__=='__main__':
	app.run(debug=DEBUG)
