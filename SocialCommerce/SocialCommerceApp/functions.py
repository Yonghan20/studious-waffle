from messagekey import *
from models import *
from django.core.mail import send_mail,BadHeaderError
from django.template import Context, Template
from SocialCommerce import settings
import hashlib
import random
import string
from django.db.models import Count
from bson import ObjectId

reg_key = RegisterFormMsg
main_key = MainMsg
log_key = LoginFormMsg
act_key = ActivateFormMsg
res_key = ResetPasswordFormMsg
tri_key = TriggerMsg
def CheckIsLoggedIn(request):
    if log_key.LOGIN_USER not in request:
        return False
    else:
        return True

def CheckIsRequested(user, user2):
    try:
        requested = RequestsLog.objects.get(user=user, to_user = user2, status=None)
        return requested
    except DoesNotExist:
        return False
    except Exception, e:
        return False

def CheckIsRequestedByUserFollowing(user2, requested):
    temp_requested = []
    for item in user2.following:
        for item2 in requested:
            if item.user == item2.to_user:
                temp_requested.append(item.user)

    return temp_requested

def CheckIsFollowedByUserFollowing(user, user2):
    temp_followed = []
    for item in user2.following:
        for item2 in user.following:
            if item.user == item2.user:
                temp_followed.append(item.user)

    return temp_followed

def CheckIsRequestedByUserFollowers(user, requested):
    temp_requested = []
    for item in user.followers:
        for item2 in requested:
            if item.user == item2.to_user:
                temp_requested.append(item.user)

    return temp_requested

def CheckIsFollowedByUserFollowers(user, user2):
    temp_followed = []
    for item in user2.followers:
        for item2 in user.following:
            if item.user == item2.user:
                temp_followed.append(item.user)

    return temp_followed

def RemoveUserFollowing(user, user2):
    for item in user2.following:
        if user == item.user:
            user2.following.remove(item)

    return user2

def RemoveUserFollowers(user, user2):
    for item in user2.followers:
        if user == item.user:
            user2.followers.remove(item)

    return user2

def GenerateActivationKey(user):
    #We will generate a random activation key
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    usernamesalt = user.username
    if isinstance(usernamesalt, unicode):
        usernamesalt = usernamesalt.encode('utf8')

    activation_key = hashlib.sha1(salt+usernamesalt).hexdigest()
    user.activation_key = activation_key
    user.key_expires = datetime.datetime.now() + datetime.timedelta(days=2)
    user.save()
    return activation_key

def GenerateRandomPassword(user):
    key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    user.set_password(key)
    user.save()
    return key

def CreateUser(username, password, email, display_name, gender):
    user = CustomUser.create_user(username=username,
                                email=email,
                                password=password)
    GenerateActivationKey(user)
    user.gender = gender
    user.is_active = False
    user.display_name = display_name
    user.last_login = datetime.datetime.now()
    user.date_joined = datetime.datetime.now()
    user.save()
    return user

def CreateUserLog(user, description, type, user2, posts):
    log = UserLog()
    log.user = user.to_dbref()
    log.description = description
    log.type = type
    log.to_user = None if user2 is None else user2.to_dbref()
    log.posts = None if posts is None else posts.to_dbref()
    log.created_date_time = datetime.datetime.now()
    log.save()

def CreatePrivateLog(user, description, type, user2, posts):
    log = PrivateLog()
    log.user = user.to_dbref()
    log.description = description
    log.type = type
    log.from_user = user2.to_dbref()
    log.posts = None if posts is None else posts.to_dbref()
    log.created_date_time = datetime.datetime.now()
    log.save()
    user.private_notifications = True
    user.save()

def CreateRequestsLog(user, user2):
    requests = RequestsLog()
    requests.user = user.to_dbref()
    requests.to_user = user2.to_dbref()
    requests.created_date_time = datetime.datetime.now()
    requests.save()

def CreateFollowingData(user2):
    following = Following()
    following.user = user2.to_dbref()
    following.created_date_time = datetime.datetime.now()
    return following

def CreateFollowersData(user):
    followers = Followers()
    followers.user = user.to_dbref()
    followers.created_date_time = datetime.datetime.now()
    return followers

def GetRequestedLogByObjectID(input):
    try:
        requested = RequestsLog.objects.get(id=input)
        return requested
    except DoesNotExist:
        return False
    except Exception, e:
         return False

def GetPostsByObjectID(input):
    try:
        posts = Posts.objects.get(id=input)
        return posts
    except DoesNotExist:
        return False
    except Exception, e:
         return False

def GetUserLikesByPosts(posts, user):
    liked = False
    for item in posts.likes:
        if item.user == user:
            liked = True

    return liked

def GetUserLikedPosts(user):
    temp = []
    for item in Posts.objects.all():
        for item2 in item.likes:
            if item2.user == user:
                temp.append(item)

    return temp

def CreateUserLikesForPosts(posts, user):
    like = Likes()
    like.user = user.to_dbref()
    like.created_date_time = datetime.datetime.now()
    posts.likes.append(like)
    posts.save()
    return posts

def RemoveUserLikesForPosts(posts, user):
    for item in posts.likes:
        if item.user == user:
            posts.likes.remove(item)

    posts.save()
    return posts

def GetRequestedLogByUser(user):
    requested = RequestsLog.objects.filter(user=user, status=None)
    return requested

def GetPrivateLogByUser(user):
    private = PrivateLog.objects.filter(user=user)
    return private

def GetUserRequestedLogByUser(user):
    requested = RequestsLog.objects.filter(to_user=user, status=None)
    return requested

def GetUserByUsernameOrEmail(input):
    try:
        user = CustomUser.objects.get(username=input)
        return user
    except DoesNotExist:
        try:
            user = CustomUser.objects.get(email=input)
            return user
        except DoesNotExist:
            return False
        except Exception, e:
            return False
    except Exception, e:
         return False

def GetUserByObjectID(input):
    try:
        user = CustomUser.objects.get(id=input)
        return user
    except DoesNotExist:
        return False
    except Exception, e:
         return False

def GetUserByActivationKey(input):
    try:
        user = CustomUser.objects.get(activation_key=input)
        return user
    except DoesNotExist:
        return False
    except Exception, e:
        return False

def SendEmail(user, path, new_password):
    email_path = path
    email_subject = reg_key.EMAIL_ACTIVATION_MSG if path == main_key.ACTIVATION_EMAIL_PATH else reg_key.RESET_PASSWORD_MSG
    email_sender = main_key.FRIENDSHIP_TITLE + '<no-reply@'+main_key.FRIENDSHIP_TITLE+'.com>'
    link = 'http://127.0.0.1:8000/activate/'
    c=Context({reg_key.ACTIVATION_LINK: link, reg_key.ACTIVATION_KEY: user.activation_key,
               main_key.CURRENT_DATE_TIME: datetime.datetime.now(),
               reg_key.NEW_PASSWORD: new_password,
               main_key.TITLE: reg_key.EMAIL_ACTIVATION_MSG if path == main_key.ACTIVATION_EMAIL_PATH else reg_key.RESET_PASSWORD_MSG})
    f = open(settings.MEDIA_ROOT + email_path, 'r')
    t = Template(f.read()) # read txt file
    f.close()
    message = t.render(c)
    try:
        send_mail(email_subject, message, email_sender, [user.email],fail_silently=False)
        return True
    except BadHeaderError:
        return False

def GetProduct():
    # try:
        product = Product.objects.all()
        return product
    # except Exception, e:
    #     return False

def GetFollowingUserLog(user):
    temp = []
    for item in user.following:
        temp.append(item.user)

    log = UserLog.objects.filter(user__in=temp).order_by("-created_date_time")[:20]
    return log

def GetUserLogByObjectId(input):
    try:
        log = UserLog.objects.get(id=input)
        return log
    except DoesNotExist:
        return False
    except Exception, e:
         return False

def CreateSeen(user):
    seen = Seen()
    seen.user = user.to_dbref()
    seen.created_date_time = datetime.datetime.now()
    return seen

def GetCategory():
    category = Category.objects.all()
    return category

def CreateProduct(name, description, category, gender, price, image, tags):
    product = Product()
    product.name = name
    product.description = description
    product.category = category
    product.gender = gender
    product.price = price
    product.status = 'available'
    product.image = 'images/product/sampleshoes.jpg'
    product.create_date = datetime.datetime.now()
    product.discount = ''
    product.save()
    return product

def GetPurchaseHistory(user):
    ph = Purchase.objects.filter(purchase_user=user)#.order_by("purchase_date")[:20]
    return ph

def CreatePost(user, post, address, address_code):
    posts = Posts()
    posts.user = user.to_dbref()
    posts.content = post
    posts.location = None if address is None else address
    posts.location_code = None if address_code is None else address_code
    posts.created_date_time = datetime.datetime.now()
    posts.save()
    return posts

def PrivateTrigger(user, user2, event, message, id):
    settings.pusher_client.trigger(str(user2.id),event ,
                                   {tri_key.USER: user.display_name,
                                    tri_key.IMAGE: user.profile_image,
                                    tri_key.MESSAGE: message,
                                    tri_key.ID: id});

def GetFollowingUserPost(user):
    temp = []
    for item in user.following:
        temp.append(item.user)

    posts = Posts.objects.filter(user__in=temp).order_by("-created_date_time")#.filter(created_date_time__gt=user.last_login)
    return posts

def GetOwnPost(user):
    posts = Posts.objects.filter(user=user).filter(created_date_time__gt=datetime.datetime.now()-datetime.timedelta(minutes=1))
    return posts

def GetProfilePosts(user2):
    posts = Posts.objects.filter(user=user2).order_by("-created_date_time")
    return posts

def GetUserNumberPosts(user_pagination):
    posts = Posts.objects.item_frequencies('user')
    temp = []
    for item2 in user_pagination:
        try:
            temp_posts = Posts_Number()
            temp_posts.user = item2.user.id
            temp_posts.number = posts[item2.user.id]
            temp.append(temp_posts)
        except KeyError:
            temp_posts = Posts_Number()
            temp_posts.user = item2.user.id
            temp_posts.number = 0
            temp.append(temp_posts)

    return temp

def GetUserProfileNumberPosts(user2):
    posts = Posts.objects.filter(user=user2).item_frequencies('user')
    try:
        temp_posts = Posts_Number()
        temp_posts.user = user2.id
        temp_posts.number = posts[user2.id]
        temp = temp_posts
    except KeyError:
        temp_posts = Posts_Number()
        temp_posts.user = user2.id
        temp_posts.number = 0
        temp = temp_posts

    return temp

def UpdateSettings(user, display_name, privacy, password):
    if (user.display_name == display_name) and \
        (user.need_request is (True if privacy == "True" else False)) and \
        (user.check_password(password) if len(password) > 0 else True):
        return False

    user.display_name = display_name
    user.need_request = True if privacy == "True" else False
    if len(password) > 0:
        user.set_password(password)

    user.last_update = datetime.datetime.now()
    user.save()
    return True

def GetProductDetail(pid):
    p = Product.objects.filter(id=pid)
    return p