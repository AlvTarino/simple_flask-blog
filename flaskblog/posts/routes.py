from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import db
from flaskblog.models import Post
from flask_login import current_user, login_required
from flaskblog.posts.forms import PostForm


# instance of the blueprint, with 'posts' as name of the blueprint
posts = Blueprint('posts', __name__)


# route to enable users create posts
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


# route to display single post using post id
@posts.route('/post/<int:post_id>')
def display_single_post(post_id):
    xpost = Post.query.get_or_404(post_id)
    return render_template('post.html', title=xpost.title, sample=xpost)


# route to update a post
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_single_post(post_id):
    updatepost = Post.query.get_or_404(post_id)
    # to check if current user is the author of the post to be updated
    if updatepost.author != current_user:
        # return a 403 error
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        updatepost.title = form.title.data
        updatepost.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.display_single_post', post_id=updatepost.id))
    elif request.method == 'GET':
        # to populate the form with current user data
        form.title.data = updatepost.title
        form.content.data = updatepost.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


# route to delete a post
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    deletepost = Post.query.get_or_404(post_id)
    # to check if current user is the author of the post to be updated
    if deletepost.author != current_user:
        # return a 403 error
        abort(403)
    db.session.delete(deletepost)
    db.session.commit()
    flash('Your blog post has been deleted', 'success')
    return redirect(url_for('main.home'))
