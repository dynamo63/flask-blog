from flask import render_template, url_for, flash, redirect, abort, request, jsonify
from flask_login import login_required, current_user
from flaskBlog import app, db
from flaskBlog.forms import PostForm
from flaskBlog.models import Post

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('blog/about.html')

# --------------------- CRUD: POST DATA ------------------ 

@app.route('/post/new', methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created', 'success')
        return redirect(url_for('home'))
    return render_template('blog/create_post.html', form=form, legend='New Post')

@app.route('/post/<slug>')
def detail_post(slug: str):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/detail_post.html', post=post)

@app.route('/post/<slug>/update', methods=['GET','POST'])
@login_required
def update_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('detail_post', slug=post.slug))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('blog/create_post.html', form=form, legend='Update Post')


@app.route('/post/<int:id>/delete', methods=['DELETE'])
def delete_post(id: int):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    # flash('Your Post has been deleted', 'success')
    return jsonify({"success": 'Your Post has benn deleted'})

# ---------------- Cuztomize error page -------------------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', message=error)

@app.errorhandler(403)
def unautorized(error):
    return render_template('403.html', message=error)