from mongoengine import *
from models import *

class TriggerMsg(Document):
    USER = 'user'
    IMAGE = 'image'
    MESSAGE = 'message'
    ID = 'id'
    REQUEST_EVENT = 'request-event'
    REQUEST_ACCEPTED_EVENT = 'request-accepted-event'
    FOLLOWING_MSG = ' is following you.'
    SENT_REQUEST_MSG = ' sent you a follower request.'
    ACCEPT_REQUEST_MSG = ' accepted your follower request.'
    LIKES_MSG = ' likes your post.'
    SHARE_MSG = ' shared your post.'
    COMMENT_MSG = ' commented your post.'

class UserLogMsg(Document):
    logged_in = ' just logged in'
    following = ' is following  '
    accepted = ' accepted '
    posted = ' posted a '
    liked = ' liked '
    shared = ' shared '
    commented = ' commented '

class PrivateLogMsg(Document):
    following = ' is following you.'
    accepted = ' accepted your follower request. '
    liked = ' likes your '
    shared = ' shared your  '
    commented = ' commented your '
class MainMsg(Document):
    FRIENDSHIP_TITLE = 'FriendShip'
    LOGIN_PAGE_TITLE = 'Login'
    HOME_PAGE_TITLE = 'Home'
    SETTINGS_PAGE_TITLE = 'Settings'
    PROFILE_PAGE_TITLE = "%s's Profile"
    FOLLOWING_PAGE_TITLE = 'Your Following'
    FOLLOWERS_PAGE_TITLE = 'Your Followers'
    REGISTER_PAGE_TITLE = 'Registration'
    ACTIVATION_PAGE_TITLE = 'Activation'
    RESET_PASSWORD_PAGE_TITLE = 'Reset Password'
    USER_FOLLOWING_PAGE_TITLE = "%s's Following"
    USER_FOLLOWERS_PAGE_TITLE = "%s's Followers"
    POST = 'POST'
    DELETE = 'delete'
    TEMPLATE_TITLE = 'template_title'
    SUCCESS = 'success'
    FAILED = 'failed'
    FOUND = 'found'
    USER = 'user'
    USER2 = 'user2'
    PRIVATE_LOG = "private_log"
    REQUEST_LOG = "request_log"
    FOLLOWING_USER_LOG = 'following_user_log'
    FOLLOWED = 'followed'
    REQUESTED = 'requested'
    PAGE_COUNT = 'page_count'
    MESSAGE = 'message'
    #region POST
    POSTS_NUMBER = "posts_number"
    POSTS = 'posts'
    OWN_POSTS = 'own_posts'
    POST_ID = 'post_id'
    USER_ID = 'user_id'
    USER_IMAGE = 'user_image'
    USER_DISPLAY_NAME = 'user_display_name'
    POSTED_DATE_TIME = 'posted_date_time'
    POST_CONTENT = 'post_content'
    POST_COMMENT = 'post_comment'
    POST_LOCATION = 'post_location'
    POST_LOCATION_CODE = 'post_location_code'
    POST_LIKE_NUMBER = 'post_like_number'
    POST_SHARE_NUMBER = 'post_share_number'
    POST_COMMENT_NUMBER = 'post_comment_number'
    CREATED_DATE_TIME = 'created_date_time'
    ADDRESS_CODE = 'address_code'
    CONTENT = 'content'
    ADDRESS = 'address'
    #endregion
    FORM = 'form'
    FRIENDS = 'friends'
    NUMBER = 'number'
    LIKES = 'likes'
    SHARE = 'share'
    LIKED_POSTS = 'liked_posts'
    USER_PAGINATION = 'user_pagination'
    POSTS_PAGINATION = 'posts_pagination'
    SEEN = 'seen'
    TO_HOME_PAGE = '/'
    TO_LOGIN_PAGE = '/login/'
    TO_ACTIVATION_PAGE = '/activation/'
    TO_REGISTER_PAGE = '/register/'
    TO_FOLLOWING_PAGE = '/following/'
    TO_SETINGS_PAGE = '/settings/'
    TO_FOLLOWERS_PAGE = '/followers/'
    HOME_PAGE = 'index.html'
    LOGIN_PAGE = 'login.html'
    REGISTER_PAGE = 'register.html'
    SETTINGS_PAGE = 'settings.html'
    PROFILE_PAGE = 'profile.html'
    FOLLOWING_PAGE = 'following.html'
    FOLLOWERS_PAGE = 'followers.html'
    NEWSFEED_NOTIFICATIONS_PAGE = 'newsfeed_notifications.html'
    REQUEST_NOTIFICATIONS_PAGE = 'request_notifications.html'
    PRIVATE_NOTIFICATIONS_PAGE = 'private_notifications.html'
    USER_FOLLOWING_PAGE = 'user_following.html'
    USER_FOLLOWERS_PAGE = 'user_followers.html'
    ACTIVATION_PAGE = 'activation.html'
    FORGET_PASSWORD_PAGE = 'forgetpassword.html'
    CHATLIST_PAGE = 'chatlist.html'
    CURRENT_DATE_TIME = 'current_datetime'
    TITLE = 'title'
    ONLINE_STATUS = 'online_status'
    ACTIVATION_EMAIL_PATH = '/ActivationEmail.txt'
    RESET_PASSWORD_EMAIL_PATH = '/ResetPasswordEmail.txt'
    REQUIRED = 'required'
    CLASS = 'class'
    REQUEST_LOG_ID = 'request_log_id'
    PLACEHOLDER = 'placeholder'
    AUTOFOCUS = 'autofocus'
    ONFOCUS = 'onfocus'
    CURSORTOEND = 'this.value = this.value'
    STYLE = 'style'
    FORM_CONTROL_CLASS = 'form-control'
    BORDER_RED = 'border-color:red;'
    UNKNOWN_ERROR = 'Unknown error'
    PAGE_REDIRECT = 'Page will redirect in 5 seconds, if browser did not perform automatically, please click '
    STATUS_NONE = 0
    STATUS_TRUE = 1
    STATUS_FALSE = 2
    STATUS_REJECTED = 3
    LOG_TYPE_CHOICES = (
        (0, UserLogMsg.logged_in),
        (1, UserLogMsg.accepted),
        (2, UserLogMsg.posted),
        (3, UserLogMsg.following),
        (4, UserLogMsg.liked),
        (5, UserLogMsg.shared),
        (6, UserLogMsg.commented),
    )
    PRIVATE_LOG_TYPE_CHOICES = (
        (0, UserLogMsg.logged_in),
        (1, PrivateLogMsg.accepted),
        (2, UserLogMsg.posted),
        (3, PrivateLogMsg.following),
        (4, PrivateLogMsg.liked),
        (5, PrivateLogMsg.shared),
        (6, PrivateLogMsg.commented),
    )
    COMMERCE_PAGE_TITLE = 'Commerce'
    PRODUCT = 'product'
    SELLINGLIST_PAGE_TITLE = 'Selling List'
    CATEGORY = "category"
    PURCHASE_HISTORY = 'purchase_history',
    BOUGHT = 'bought',
    PAYPAL = 'paypal',
    PRODUCT_DETAIL = 'pdetail'

class RegisterFormMsg(Document):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    GENDER = "gender"
    USERNAME = "username"
    EMAIL = "email"
    DISPLAY_NAME = "display_name"
    PASSWORD = "password"
    CONFIRM_PASSWORD = "confirm_password"
    ENTER_USERNAME_MSG = "Enter your Username."
    ENTER_DISPLAYNAME_MSG = "Enter your Display Name."
    ENTER_PASSWORD_MSG = "Enter your Password."
    ENTER_CONFIRM_PASSWORD_MSG = "Enter your Confirm Password."
    ENTER_EMAIL_MSG = "e.g. info@example.com"
    USERNAME_EXISTS = "Username '%s' already exists."
    EMAIL_EXISTS = "Email '%s' already exists."
    USER_NAME_INVALID = "Username is Invalid."
    DISPLAY_NAME_INVALID = "Display Name is Invalid."
    PASSWORD_NOT_MATCH_MSG = "Password not match with Confirm Password."
    CONFIRM_PASSWORD_NOT_MATCH_MSG = "Confirm Password not match with Password."
    REQUIRED_USERNAME_MSG = "Username is required."
    REQUIRED_DISPLAY_NAME_MSG = "Display Name is required."
    REQUIRED_EMAIL_MSG = "Email is required."
    REQUIRED_PASSWORD_MSG = "Password is required."
    REQUIRED_CONFIRM_PASSWORD_MSG = "Confirm Password is required."
    REGISTRATION_SUCCESSFUL_MSG = "Username '%s' Registered Successful!"
    EMAIL_ACTIVATION_MSG = "FriendShip Account Activation"
    RESET_PASSWORD_MSG = "FriendShip Account Reset Password"
    NEW_PASSWORD = "new_password"
    ACTIVATION_LINK = "activation_link"
    ACTIVATION_KEY = "activation_key"
    EMAIL_SENDED_MSG = "An email has been sent to your inbox."
    REGISTERED = "registered"
    REGISTERED_MESSAGE = "registered_message"
    DEFAULT_PHOTO = "images/people/110/default-user.jpg"

class SettingsFormMsg(Document):
    PRIVACY_CHOICES = (
        (True, 'Private'),
        (False, 'Public'),
    )
    UPDATED = "updated"
    PRIVACY = "privacy"
    OLD_PASSWORD = "old_password"
    PASSWORD = "password"
    CONFIRM_PASSWORD = "confirm_password"
    ENTER_OLD_PASSWORD_MSG = "Enter your Old Password."
    ENTER_PASSWORD_MSG = "Enter your New Password."
    ENTER_CONFIRM_PASSWORD_MSG = "Confirm your New Password."
    OLD_PASSWORD_INVALID_MSG = "Old Password is invalid."
    PASSWORD_NOT_MATCH_MSG = "New Password not match with Confirm Password."
    CONFIRM_PASSWORD_NOT_MATCH_MSG = "Confirm Password not match with New Password."
    REQUIRED_OLD_PASSWORD_MSG = "Old Password is required."
    REQUIRED_PASSWORD_MSG = "New Password is required."
    REQUIRED_CONFIRM_PASSWORD_MSG = "Confirm Password is required."
    REQUIRED_PRIVACY_MSG = "Privacy is required."
    UPDATE_SUCCESSFUL_MSG = "Settings updated successful!"

class LoginFormMsg(Document):
    ACCOUNT = "account"
    PASSWORD = "password"
    REMEMBER_ME = "remember_me"
    IS_NOT_ACTIVATED = "is_not_activated"
    REQUIRED_ACCOUNT_MSG = "Username or Email is required."
    REQUIRED_PASSWORD_MSG = "Password is required."
    ENTER_ACCOUNT_MSG = "Username or Email."
    ENTER_PASSWORD_MSG = "Enter your Password."
    INVALID_ERROR_MSG = "Invalid Account or Password."
    IS_NOT_ACTIVATED_MSG = "Your account is not activated."
    USER_FOUND = "user_found"
    USER_IMAGE = "user_image"
    LOGIN_USER = "login_user"

class ActivateFormMsg(Document):
    ACCOUNT = "account"
    ENTER_ACCOUNT_MSG = "Username or Email."
    REQUIRED_ACCOUNT_MSG = "Username or Email is required."
    USERNAME_OR_EMAIL_NOT_EXIST = "Username or Email is not exists"
    IS_EXPIRED = "is_expired"
    IS_ALREADY_ACTIVE = "is_already_active"
    IS_ACTIVATED_MSG = "Your account already activated."
    IS_EXPIRED_MSG = "Activation link already expired."
    ACTIVATION_KEY_NOT_FOUND = "Activation link not found."
    SUCCESSFUL_ACTIVATE_MSG = "Your account activated successfully."
    NEW_ACTIVATION_LINK_SENDED = "New activation link has been sent to your email inbox."
    ENTER_ACCOUNT_FOR_NEW_LINK = "Please enter your Username or Email and click Submit for new activation link."

class ResetPasswordFormMsg(Document):
    ENTER_ACCOUNT_FOR_NEW_PASSWORD = "Please enter your Username or Email and click Submit for new password."