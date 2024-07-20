from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write_blog', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_blog = Blog(title=title, content=content)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('write_blog.html')

@app.route('/read_blogs')
def read_blogs():
    blogs = Blog.query.all()
    return render_template('read_blogs.html', blogs=blogs)

@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return render_template('blog_detail.html', blog=blog)

if __name__ == '__main__':
    app.run(debug=True)
