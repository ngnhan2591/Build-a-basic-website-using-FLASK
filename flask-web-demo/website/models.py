from website import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from website import login
from hashlib import md5
from sqlalchemy import or_

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

followers = db.Table("followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(140))
    receive_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return '<Message %s>' % self.message

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), index=True, unique=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    posts = db.relationship('Post', backref="author", lazy="dynamic")
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic"
    )
    comments = db.relationship('Comment', backref='author', lazy="dynamic")


    def follow(self, user):
        if not self.is_following(user=user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user=user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%d'\
            % (digest, size)

    def followed_posts(self):
        followed_posts = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).\
            filter(followers.c.follower_id == self.id)
        my_posts = self.posts.filter_by(status=0)
        posts = followed_posts.union(my_posts).order_by(Post.timestamp.desc())
        return posts

    def my_posts(self):
        posts = self.posts.filter(or_(Post.status==None, Post.status==0)).order_by(Post.timestamp.desc())
        return posts

    def selled(self):
        posts = self.posts.filter_by(status=1).order_by(Post.timestamp.desc())
        return posts

    def __repr__(self) -> str:
        return "<User %s>" % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    image_url = db.Column(db.String(140))
    category = db.Column(db.String(50))
    infor = db.Column(db.String(500))
    detail = db.Column(db.String(500))
    status = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy="dynamic")

    @staticmethod
    def all_posts():
        posts = Post.query.order_by(Post.timestamp.desc())
        return posts

    def __repr__(self) -> str:
        return "<Post %s>" % self.title

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return "<Comment %s>" % self.comment
    