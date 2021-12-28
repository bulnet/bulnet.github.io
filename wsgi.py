from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/home')
@app.route('/')
def index():
    #films = get_films()
    return render_template("index.html") #films=films


@app.route('/create-art', methods=['POST', 'GET'])
def create_art():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Art(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Виникла помилка!"
    else:
        return render_template("create_art.html")


@app.route('/posts')
def posts():
    articles = Art.query.order_by(Art.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Art.query.get(id)
    return render_template("posts_detail.html", article=article)


@app.route('/about')
def about():
    return render_template("about.html", title="About")


@app.route('/oppos')
def oppos():
    return render_template("oppos.html")


if __name__ == '__main__':
    app.run(debug=True)