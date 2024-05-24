from newsapplication import app
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

app.secret_key = 'its a secret!'
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)