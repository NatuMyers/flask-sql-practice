from flask import Flask, render_template, url_for, redirect, request, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DeceptronItem

engine = create_engine('sqlite:///deceptron.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# These routes handle all HTML website services
@app.route('/')
@app.route('/deceptronItems')
def home():
    # Shows all DeceptronItems
    deceptronItems = session.query(DeceptronItem).all()
    return render_template('deceptronItems.html', deceptronItems=deceptronItems)

@app.route('/deceptronItem/new', methods=['GET', 'POST'])
def newDeceptronItem():
    # Add a new DeceptronItem
    if request.method == "POST":
        newDeceptronItem = DeceptronItem(name = request.form['newDeceptronItem'])
        session.add(newDeceptronItem)
        session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('newDeceptronItem.html') 

@app.route('/deceptronItem/<int:rest_id>/edit', methods=['GET', 'POST'])
def editDeceptronItem(rest_id):
    # Edits a specifies DeceptronItem Name
    deceptronItem = session.query(DeceptronItem).filter_by(id=rest_id).one()
    if request.method == "POST":
        editDeceptronItem = session.query(DeceptronItem).filter_by(id=rest_id).one()
        editdeceptronItem.name = request.form['editDeceptronItem']
        session.add(editDeceptronItem)
        session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('editDeceptronItem.html', deceptronItem=deceptronItem)

@app.route('/deceptronItem/<int:rest_id>/delete', methods=['GET','POST'])
def deleteDeceptronItem(rest_id):
    # Deletes a specific deceptronItem
    deceptronItem = session.query(DeceptronItem).filter_by(id=rest_id).one()
    if request.method == "POST":
        deleteDeceptronItem = session.query(DeceptronItem).filter_by(id=rest_id).one()
        session.delete(deleteDeceptronItem)
        session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('deleteDeceptronItem.html', deceptronItem=deceptronItem) 

@app.route('/deceptronItem/<int:rest_id>')




# These routes hand all REST API requests. They will respond with JSON
@app.route('/deceptronItems/JSON')
def deceptronItemsJSON():
    deceptronItems = session.query(DeceptronItem).all()
    return jsonify(DeceptronItems=[r.serialize for r in deceptronItems])



if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
