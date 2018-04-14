from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'akxjKJAnlxsk'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    blog = db.Column(db.String(240))


    def __init__(self, title, blog):
        
        self.title = title
        self.blog = blog

@app.route('/blog', methods=['GET'])
def blog():
        id = request.args.get('id')
        blogs = Blog.query.all()
        return render_template('blog.html', title="Build a Blog", id=id,blogs=blogs)
    
   
    
@app.route('/single-blog', methods=['GET'])
def single_blog():
    
    id = int(request.args.get("id"))
    
    blog = Blog.query.filter_by(id=id).first()
    return render_template('single-blog.html', title="Build a Blog", id=id, blog=blog)


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

            return render_template('/newpost.html', title=title, blog=blog,title_error=title_error, blog_error=blog_error)   

        new_blog= Blog(title, blog)
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.all()
        return render_template('/blog.html', blogs=blogs)

    return render_template('/newpost.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['email'] = email
            flash('Logged in')
            
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()

        if not existing_user:
            new_user = User(email,password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return '<h1>Duplicate User!</h1>'

    return render_template('register.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    
    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        task_name = request.form['task']
        
        new_task = Task(task_name, owner)
        db.session.add(new_task)
        db.session.commit()
        
    
    tasks = Task.query.filter_by(completed=False,owner=owner).all()
    completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
    return render_template('todos.html', title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)

    return redirect('/')

if __name__ == '__main__':
    app.run()