from flask import Flask , render_template , g
import sqlite3

PATH = "db/jobs.sqlite"



app = Flask(__name__)# If you are using a single module , you should use __name__ because depending on if it’s started as application or imported as module the name will be different ('__main__' versus the actual import name).
#This is needed so that Flask knows where to look for templates, static files, and so on.
#If you are using a single module, __name__ is always the correct value. If you however are using a package, it’s usually recommended to hardcode the name of your package
#to ease the debugging
#For example if your application is defined in yourapplication/app.py you should create it with one of the two versions below:

#app = Flask('yourapplication')
#app = Flask(__name__.split('.')[0])


def open_connection():
    connection = getattr(g, '_connection',None)
    if connection is None:
        connection = g._connection = sqlite3.connect(PATH)

    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql , values=() , commit=False , single = False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit is True :
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g , '_connection' , None)
    if connection is not None:
        connection.close()

@app.route('/job/<job_id>')
def job(job_id):
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id],single=True )
    return render_template("job.html", job=job)

@app.route('/employer/<employer_id>')
def employer(employer_id):
    employer = execute_sql('SELECT * FROM employer WHERE id=?', [employer_id], single=True)
    jobs = ('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?',[employer_id])
    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])
    return render_template("employer.html", employer=employer, jobs=jobs, reviews=reviews)

@app.route('/')# the decorator is telling our @app that whenever a user visits our app domain (myapp.com) at the given .route(), execute the jobs() function.
#use the route() decorator to tell Flask what URL should trigger our function.use the route() decorator to tell Flask what URL should trigger our function. A decorator that is used to register a view function for a given URL rule
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)
    # this is to get the html code inside the python. it looks for a folder named template and then searches for the specified name in it. We can also pass parameters if required in the html
