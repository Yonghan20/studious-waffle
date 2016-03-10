from mongoengine.django.auth import User
from mongoengine import *
from messagekey import *
import datetime
import os

main_key = MainMsg
reg_key = RegisterFormMsg

class RegisterUser(Document):
    username = StringField(max_length=10, required=True)
    display_name = StringField(max_length=10, required=True)
    email = EmailField(required=True)
    password = StringField(min_length=6, max_length=12, required=True)
    confirm_password = StringField(min_length=6, max_length=12, required=True)

class RequestsLog(Document):
    user = ReferenceField('CustomUser')
    to_user = ReferenceField('CustomUser')
    status = BooleanField()
    edited_date_time = DateTimeField()
    created_date_time = DateTimeField()

class Seen(EmbeddedDocument):
    user = ReferenceField('CustomUser')
    created_date_time = DateTimeField()

class UserLog(Document):
    user = ReferenceField('CustomUser')
    to_user = ReferenceField('CustomUser')
    posts = ReferenceField('Posts')
    description = StringField()
    type = IntField(choices=main_key.LOG_TYPE_CHOICES)
    seen = ListField(EmbeddedDocumentField(Seen))
    created_date_time = DateTimeField()

class PrivateLog(Document):
    user = ReferenceField('CustomUser')
    from_user = ReferenceField('CustomUser')
    posts = ReferenceField('Posts')
    description = StringField()
    type = IntField(choices=main_key.PRIVATE_LOG_TYPE_CHOICES)
    created_date_time = DateTimeField()

class Likes(EmbeddedDocument):
    user = ReferenceField('CustomUser')
    created_date_time = DateTimeField()

class Share(EmbeddedDocument):
    user = ReferenceField('CustomUser')
    created_date_time = DateTimeField()

class Comments(EmbeddedDocument):
    user = ReferenceField('CustomUser')
    content = StringField()
    created_date_time = DateTimeField()

class Posts(Document):
    user = ReferenceField('CustomUser')
    from_user = ReferenceField('CustomUser')
    from_posts = ReferenceField('Posts')
    likes = ListField(EmbeddedDocumentField(Likes))
    share = ListField(EmbeddedDocumentField(Share))
    comments = ListField(EmbeddedDocumentField(Comments))
    content = StringField(max_length=300)
    location = StringField()
    location_code = StringField()
    created_date_time = DateTimeField()
    edited_date_time = DateTimeField()

class Following(EmbeddedDocument):
    user = ReferenceField('CustomUser')
    created_date_time = DateTimeField()

class Followers(EmbeddedDocument):
    user = ReferenceField('CustomUser')
    created_date_time = DateTimeField()

class Posts_Number(Document):
    user = StringField()
    number = IntField()

class CustomUser(User):
    activation_key = StringField(max_length=40)
    display_name = StringField(max_length=10)
    gender = StringField(max_length=1, choices=reg_key.GENDER_CHOICES)
    need_request = BooleanField(default=False)
    open_news_feeds = BooleanField(default=True)
    key_expires = DateTimeField()
    last_update = DateTimeField()
    credit = DecimalField()
    online_status = IntField()
    request_notifications = BooleanField(default=False)
    private_notifications = BooleanField(default=False)
    profile_image = StringField(default=reg_key.DEFAULT_PHOTO)
    following = ListField(EmbeddedDocumentField(Following))
    followers = ListField(EmbeddedDocumentField(Followers))

class Product(Document):
    name = StringField(max_length=60)
    category = StringField(max_length=20)
    gender = StringField(max_length=10)
    # price = DecimalField(max_digits=5, decimal_places=2)
    price = StringField(max_length=50)
    description = StringField(max_length=400)
    status = StringField(max_length=15)
    image = StringField(default=reg_key.DEFAULT_PHOTO)
    create_date = DateTimeField()
    discount = StringField(max_length=3)
    seller = ReferenceField('CustomUser')

class Category(Document):
    shoes = StringField(max_length=5)
    clothing = StringField(max_length=8)
    accessory = StringField(max_length=9)
    bag = StringField(max_length=3)
    sport = StringField(max_length=5)
    watch = StringField(max_length=5)

class Purchase(Document):
    purchase_user = ReferenceField('CustomUser')
    purchase_product = ReferenceField('Product')
    quantity = StringField(max_length=5)
    purchase_date = DateTimeField()
