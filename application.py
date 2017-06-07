from cs50 import SQL
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)
db = SQL("sqlite:///ycbaulan.db")                      

# displays list of artists upon loading webpage              
@app.route("/")                                         
def index():                                                                                         
    rows = db.execute("SELECT * FROM artists2 LIMIT 10")                
    return render_template("artists.html", artists=rows)           

# displays list of artists
@app.route("/artists", methods=["POST"])
def back_to_artists():                                                  
    rows = db.execute("SELECT * FROM artists2 LIMIT 10")                        
    return render_template("artists.html", artists=rows)

# when 'match' selected, moves selected row to matches table, 
# removes from general artist list
# when 'nonmatch' selected, moves selected row to nonmatches table,
# removes from general artist list
@app.route("/match", methods=["POST"])  
def match():
    
    if request.form["match?"] == "match":
        db.execute("INSERT INTO matches (ulan_id, artist_name, Nationality, begin_date, end_date) VALUES (:ulan_id, :artist_name, :Nationality, :begin_date, :end_date)", 
        ulan_id=request.form["id"], artist_name=request.form["name"], Nationality=request.form["nationality"], begin_date=request.form["begin"], end_date=request.form["end"])
    
        db.execute("DELETE FROM artists2 WHERE ulan_id = :ulan_id", ulan_id=request.form["id"])
    
        rows = db.execute("SELECT * FROM matches LIMIT 10")                         
        return render_template("matches.html", matches=rows) 
        
    elif request.form["match?"] == "notmatch":
        db.execute("INSERT INTO nonmatches (ulan_id, artist_name, Nationality, begin_date, end_date) VALUES (:ulan_id, :artist_name, :Nationality, :begin_date, :end_date)",
        ulan_id=request.form["id"], artist_name=request.form["name"], Nationality=request.form["nationality"], begin_date=request.form["begin"], end_date=request.form["end"])
        
        db.execute("DELETE FROM artists2 WHERE ulan_id = :ulan_id", ulan_id=request.form["id"])
        
        rows = db.execute("SELECT * FROM nonmatches LIMIT 10")
        return render_template("nonmatches.html", nonmatches=rows)
   
# when clicked, displays list of matches                         
@app.route("/matches", methods=["POST"])                
def view_matches():                                          
    rows = db.execute("SELECT * FROM matches LIMIT 10")                
    return render_template("matches.html", matches=rows)    

# when clicked, displays list of nonmatches    
@app.route("/nonmatches", methods=["POST"])
def view_nonmatches():
    rows = db.execute("SELECT * FROM nonmatches LIMIT 10")
    return render_template("nonmatches.html", nonmatches=rows)

# when clicked, moves matches row back to artists table and 
# removes from matches table 
@app.route("/undo", methods=["POST"])
def undo_match():
    
    db.execute("INSERT INTO artists2 (ulan_id, artist_name, Nationality, begin_date, end_date) VALUES (:ulan_id, :artist_name, :Nationality, :begin_date, :end_date)",
    ulan_id=request.form["id"], artist_name=request.form["name"], Nationality=request.form["nationality"], begin_date=request.form["begin"], end_date=request.form["end"])
    
    db.execute("DELETE FROM matches WHERE ulan_id = :ulan_id", ulan_id=request.form["id"])
    
    rows = db.execute("SELECT * FROM matches LIMIT 10")
    return render_template("matches.html", matches=rows)
    
# when clicked, moves nonmatches row back to artists table and 
# removes from nonmatches table     
@app.route("/undo-non-match", methods=["POST"])
def undo_non_match():
    
    db.execute("INSERT INTO artists2 (ulan_id, artist_name, Nationality, begin_date, end_date) VALUES (:ulan_id, :artist_name, :Nationality, :begin_date, :end_date)", 
    ulan_id=request.form["id"], artist_name=request.form["name"], Nationality=request.form["nationality"], begin_date=request.form["begin"], end_date=request.form["end"])
    
    db.execute("DELETE FROM nonmatches WHERE ulan_id = :ulan_id", ulan_id=request.form["id"])
    
    rows = db.execute("SELECT * FROM nonmatches LIMIT 10")
    return render_template("nonmatches.html", nonmatches=rows)