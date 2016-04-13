import os
import psycopg2
import psycopg2.extras
import sys
from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)
app.secret_key = 'some_secret'

reload(sys)
sys.setdefaultencoding("UTF8")

def connectToDB():
  connectionString = 'dbname=dump user=dumpuser password=password host=localhost'
  print connectionString
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/')
def mainIndex():
    return render_template('index.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    conn = connectToDB()
    cur = conn.cursor()
    try:
        cur.execute("Select * from images")
    except:
        print("Error executing select")
    results = cur.fetchall()
    
    return render_template('test.html', locations=results)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        conn = connectToDB()
        cur = conn.cursor()
        searchkey = request.form['keyword']
        if searchkey[0] == '+':
            print searchkey[1:]
            #query = "select * from image_join_tag join images on image_id = imageid join tags on tagid = tag_id where tags.name ='" + searchkey[1:] + "'"
        else:
            searchkey = '%%' + searchkey + '%%'
            query = cur.mogrify("Select * from images where name LIKE %s;" , (searchkey,))
        conn = connectToDB()
        cur = conn.cursor()
        try:
            cur.execute(query)
        except:
            print("Error executing select")
        results = cur.fetchall()
        
        return render_template('search.html', locations=results)
    else:
        return render_template('presearch.html')
    
    
# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)