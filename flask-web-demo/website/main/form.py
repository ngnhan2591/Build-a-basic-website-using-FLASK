from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


class EditProfile(FlaskForm):
    username = StringField(label="Họ và tên", validators=[DataRequired()])
    about_me = StringField(label="Mô tả", validators=[Length(min=0, max=140)])
    submit = SubmitField(label="Lưu")

class PostForm(FlaskForm):
    title = StringField(label="Tên sản phẩm", validators=[Length(min=1, max=140)])
    image_url = StringField(label="Hình ảnh")
    category = StringField(label="Phân loại nhanh", validators=[Length(min=1, max=140)])
    infor = StringField(label="Thông tin sản phẩm", validators=[Length(min=1, max=500)])
    detail = StringField(label="Mô tả chi tiết")
    submit = SubmitField(label="Đăng")

class CommentForm(FlaskForm):
    comment = StringField(label="Bình luận", validators=[Length(min=1, max=140)])
    submit = SubmitField(label="Đăng")

class PostUpdate(FlaskForm):
    title = StringField(label="Tên sản phẩm", validators=[Length(min=1, max=140)])
    image_url = StringField(label="Hình ảnh")
    category = StringField(label="Phân loại nhanh", validators=[Length(min=1, max=140)])
    infor = StringField(label="Thông tin sản phẩm", validators=[Length(min=1, max=500)])
    detail = StringField(label="Mô tả chi tiết")
    submit = SubmitField(label="Đăng")
    status = SelectField(label="Tình trạng", choices=['Chưa bán', 'Đã bán'])
    submit = SubmitField(label='Lưu')