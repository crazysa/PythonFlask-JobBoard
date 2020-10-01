from flask import Flask , render_template
app = Flask(__name__)# If you are using a single module , you should use __name__ because depending on if it’s started as application or imported as module the name will be different ('__main__' versus the actual import name).
#This is needed so that Flask knows where to look for templates, static files, and so on.
#If you are using a single module, __name__ is always the correct value. If you however are using a package, it’s usually recommended to hardcode the name of your package
#to ease the debugging
#For example if your application is defined in yourapplication/app.py you should create it with one of the two versions below:

#app = Flask('yourapplication')
#app = Flask(__name__.split('.')[0])

@app.route('/')# the decorator is telling our @app that whenever a user visits our app domain (myapp.com) at the given .route(), execute the jobs() function.
#use the route() decorator to tell Flask what URL should trigger our function.use the route() decorator to tell Flask what URL should trigger our function. A decorator that is used to register a view function for a given URL rule
@app.route('/jobs')
def jobs():
     return render_template('index.html') # this is to get the html code inside the python. it looks for a folder named template and then searches for the specified name in it. We can also pass parameters if required in the html
