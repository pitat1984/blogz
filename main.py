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

@app.route('/blog', methods=['POST', 'GET'])
def index():
        
        
        blogs = Blog.query.all()
        return render_template('blog.html', title="Build a Blog",blogs=blogs)
        
    
   
    
@app.route('/single-blog', methods=['GET'])
def blog():
    
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

if __name__ == '__main__':
    app.run()