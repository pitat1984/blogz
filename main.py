from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'akxjKJAnlxsk'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    blog = db.Column(db.String(240))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, blog, owner):
                
        self.title = title
        self.blog = blog
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,email,password):

        self.email = email
        self.password = password
        

def valid_input(text_input):
    
    if len(text_input) < 3 or len(text_input) > 20:
        return False
    elif " " in text_input:
        return False
    else:
        return True

def valid_userpass(text_input):

    if (not text_input) or (valid_input(text_input) == False):
        return False
    else:
        return True

def valid_email(text_input):
    at_count = 0
    dot_count = 0
    for char in text_input:
        if char is "@":
            at_count = at_count + 1
        if char is ".":
            dot_count = dot_count + 1

    if text_input is "":
        return True    
    elif (at_count == 1) and (dot_count == 1) and (valid_input(text_input) == True):
        return True
    else:
        return False    
    
def passwords_match(input_one, input_two):

    if (not input_two) or (input_one != input_two):
        return False
    else:
        return True

@app.route('/blog', methods=['POST', 'GET'])
def blog():
        
        blogs = Blog.query.all()
        return render_template('blog.html', title="Build a Blog",blogs=blogs) 
    
@app.route('/single-blog', methods=['GET'])
def single_blog():
    
    id = request.args.get("id")
    
    blog = Blog.query.filter_by(id=id).first()
    return render_template('single-blog.html', title="Build a Blog",blog=blog)

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        
        if not title or not blog:
            if not title:
                title_error = 'Please enter a title'
            else:
                title_error = ''
                
            if not blog:
                blog_error = 'Please enter a body'
            else:
                blog_error = ''

            return render_template('newpost.html', title=title, blog=blog,title_error=title_error, blog_error=blog_error)   

        new_blog= Blog(title, blog)
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.all()
        id = str(new_blog.id)
        return redirect('single-blog?id=' + id)

    return render_template('newpost.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['email'] = email
            flash('Logged in')
            
            return redirect('/newpost')
        elif not user:
            flash('Username does not exist', 'error')
        elif user.password != password:
            flash('Password is incorrect', 'error')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':   
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()
            
        if valid_userpass(password) == False:
            password_error = "That's not a valid password"
        else:
            password_error = ""

        if passwords_match(password,verify) == False:
            match_error = "Passwords don't match"
        else:
            match_error = ""

        if valid_email(email) == False:
            email_error = "That's not a valid email"
        else:
            email_error = ""

        if (valid_userpass(password) == False) or (passwords_match(password,verify) == False) or (valid_email(email) == False):  
            return render_template('signup.html', email=email, password_error=password_error, match_error=match_error, email_error=email_error)

        if not existing_user:
            new_user = User(email,password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/newpost')
        else:
            flash('That user already exists', 'error')
            
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/blog')

@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return render_template('/', title="Build a Blog",users=users)
    
if __name__ == '__main__':
    app.run()