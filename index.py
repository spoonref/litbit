# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, json
import random
import os
import countsyl
import click
app = Flask(__name__)

#def get_books():
#	book_list = []
	#books = os.listdir("books")
#	books = json.load("books.json")
	#for book in books:
	#	book = unicode(book.replace(".txt", ""), 'utf-8')
	#	book_list.append(book)
#	for book in books:
#		book_list.append(book.author)

#	return book_list

@app.cli.command('register')
@click.option('--file', prompt=True)
@click.option('--title', prompt=True)
@click.option('--author', prompt=True)
@click.option('--year', prompt=True)
@click.option('--image', prompt=True)
def register_book(file,title,author,year,image):
	#read the file provided, create a json file, update the books.json meta file
	new_book = dict()
	with app.open_resource('books/books.json') as f:
		books = json.load(f)

	new_id = books["books"][-1]["id"] + 1
	new_book["id"] = new_id
	new_book["title"] = title
	new_book["file"] = file
	new_book["author"] = author
	new_book["image"] = image
	new_book["year"] = year

	books["books"].append(new_book)
	with open('books/books.json', 'w') as f:
		json.dump(books,f)
	output = (title, new_id)
	click.echo("%s Registered\nID: %d" % output)

def get_books():
	with app.open_resource('books/books.json') as f:
		books = json.load(f)

	return books

def get_filename(title,books):
	for b in books:
		if b.title == title:
			return b.file

	return False

def read_book(filename):
	f = open("books/"+filename, "r")
	return get_haiku(f)

def get_poem_code(code_list):
	code = code_list[0]+"|"+code_list[1]+"|"+code_list[2]
	#encrypt
	return code

def read_poem_code(code):
	code_list = code.split("|")
	return code_list

def generate_poem(title,books):
	poem = []
	filename = get_filename(title, books)
	if filename:
		f = open("books/"+filename, "r")
		
	else:
		return False

def get_haiku(book):
	print "get haiku"
	five_syllables = []
	seven_syllables = []
	grab_bag = []

	for line in book:
		syllable = random.randint(1,10)
		clean_line = line.strip().rstrip(',')
		clean_line = clean_line[:1].upper() + clean_line[1:]
		if not clean_line.startswith('"'):
			clean_line = clean_line.rstrip('"')

		if not clean_line.startswith('“'):
			clean_line = clean_line.rstrip('”')

		if not clean_line.startswith('‘'):
			clean_line = clean_line.rstrip('’')

		if not clean_line.startswith("'"):
			clean_line = clean_line.rstrip("'")

		if len(clean_line):
			syl_count = countsyl.count_syllables(clean_line)

			#if syl_count[0] >= 4 and syl_count[0] <= 7:
			#	grab_bag.append(clean_line)
			if syl_count[0] == 5 and syl_count[1] in [5,6]:
				five_syllables.append(clean_line)

			if syl_count[0] == 7 and syl_count[1] in [7,8]:
				seven_syllables.append(clean_line)

	if len(five_syllables) > 2 and len(seven_syllables) > 0:
		return [random.choice(five_syllables), random.choice(seven_syllables), random.choice(five_syllables)]
	else:
		return False

	#if len(grab_bag) > 2:
	#	return [random.choice(grab_bag), random.choice(grab_bag), random.choice(grab_bag)]
	#else:
	#	return False

@app.route("/")
def index():
	books = get_books()
	#Show the user the home page where they can select a book
	return render_template('index.html', books=books["books"])

@app.route("/<book>")
def get_poem(book):
	books = get_books()
	poem = list()
	return render_template('display_poem.html', poem=poem, books=books["books"])

@app.route("/<book>/<code>")
def display_poem(book, code):
	books = get_books()
	#Show a poem generated by the book and code provided
	code_list = read_poem_code(code)
	poem = list()
	return render_template('display_poem.html', poem=poem, books=books["books"])

"""@app.route("/", methods=['GET', 'POST'])
def layout():
	#books = get_books()
	#books = json.load("books/books.json")
	with app.open_resource('books/books.json') as f:
		books = json.load(f)
	if request.method == 'POST':
		title = request.form["book"]
	else:
		title = "Moby Dick"

	haiku = read_book(title+".txt")
	line1 = unicode(haiku[0], 'utf-8')
	line2 = unicode(haiku[1], 'utf-8')
	line3 = unicode(haiku[2], 'utf-8')
	return render_template('layout.html', title=title,line1=line1,line2=line2,line3=line3,books=books["books"])"""

if __name__ == "__main__":
	app.run()