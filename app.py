from flask import Flask, render_template, request, jsonify
import string
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import random
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

SQLALCHEMY_DATABASE_URL = 'sqlite:///test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()






@app.route('/')
def home():
    return render_template('home.html')

@app.route('/connexion')
def connexion():
	return render_template('signin.html')

@app.route('/inscription/add', methods = ['POST'])
def add_inscription():
	create_produit(request.form)
	return 'ok'

@app.route('/produit/get/all')
def get_all_product():
	data = read_all_product()
	output = []
	for i in data:
		tmp = {}
		tmp['name'] = i.name
		tmp['id'] = i.id
		tmp['categorie'] = i.categorie
		output.append(tmp)
	return jsonify(output)




def generate_id(length: int):
	uid = []
	while len(uid) != length:
		rand = random.randrange(2)
		if rand == 1:
			uid.append(generate_int(10))
		else:
			uid.append(generate_string(1))
	return (''.join(uid))

def generate_int(length):
	return str(random.randrange(10))

def generate_string(length):
	letters = string.ascii_lowercase
	res = ''.join(random.choice(letters) for i in range(length))
	return res


class ProduitModel(Base):
	__tablename__ = "produits"

	id = Column(String, primary_key=True, index=True)
	name = Column(String)
	categorie = Column(String)


Base.metadata.create_all(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

def create_produit(form, db: Session = SessionLocal()):
	item = ProduitModel(id=generate_id(23), name=form['name'], categorie=form['categorie'])
	db.add(item)
	db.commit()

def read_all_product(db: Session = SessionLocal()):
	# return db.query(ProduitModel).filter_by(categorie='fond de teint')first()
	return db.query(ProduitModel).all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)