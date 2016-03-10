from django.shortcuts import render_to_response, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.template import Context, loader
from django.core.context_processors import csrf
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from forms import *
from functions import *
from models import *
import humanize
from messagekey import *
from bson import ObjectId
import json
import operator
from django.http import Http404
import datetime
import time
from django.db.models import Count
from django import template

# Create your views here.
user_log = UserLogMsg
reg_key = RegisterFormMsg
main_key = MainMsg
log_key = LoginFormMsg
act_key = ActivateFormMsg
res_key = ResetPasswordFormMsg
set_key = SettingsFormMsg
tri_key = TriggerMsg


# region login/logout/register/activation/reset password
def login_view(request):
    title = main_key.LOGIN_PAGE_TITLE
    form = LoginForm
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    registered = False
    user_image = None
    is_not_activated = False

    # region check is logged_in to main page
    if CheckIsLoggedIn(session) == True:
        return HttpResponseRedirect(main_key.TO_HOME_PAGE)  # Redirect after POST
    # endregion

    if reg_key.REGISTERED in session:
        registered = True
        del session[reg_key.REGISTERED]
    if request.method == main_key.POST:
        form = LoginForm(post)
        if form.is_valid():
            remember_me = form.cleaned_data['remember_me']
            user = GetUserByUsernameOrEmail(form.data[log_key.ACCOUNT])
            if user is not False:
                user_image = user.profile_image
                if user.is_active is False:
                    is_not_activated = True
                else:
                    account = form.data[log_key.ACCOUNT]
                    password = form.data[log_key.PASSWORD]
                    user.last_login = datetime.datetime.now()
                    user.online_status = 0
                    user.save()
                    if remember_me == True:
                        user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                        session[log_key.LOGIN_USER] = account
                        session.set_expiry(365 * 24 * 60 * 60)
                    else:
                        session[log_key.LOGIN_USER] = account
                        session.set_expiry(0)

                    CreateUserLog(user, main_key.LOG_TYPE_CHOICES[0][1], main_key.LOG_TYPE_CHOICES[0][0], None, None)
                    return HttpResponseRedirect(main_key.TO_HOME_PAGE)  # Redirect after POST
        else:
            user = GetUserByUsernameOrEmail(form.data[log_key.ACCOUNT])
            if user is not False:
                user_image = user.profile_image
    else:
        form = LoginForm()

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.FORM: form,
        reg_key.REGISTERED: reg_key.EMAIL_SENDED_MSG if registered is True else None,
        log_key.USER_IMAGE: user_image,
        log_key.IS_NOT_ACTIVATED: log_key.IS_NOT_ACTIVATED_MSG + " " + main_key.PAGE_REDIRECT if is_not_activated is True else None,
    }
    return render(request, main_key.LOGIN_PAGE, context)


def logout_view(request):
    session = request.session

    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    user.online_status = 2
    user.save()
    logout(request)
    return HttpResponseRedirect(main_key.TO_HOME_PAGE)


def register_view(request):
    title = main_key.REGISTER_PAGE_TITLE
    form = RegisterForm
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to main page
    if CheckIsLoggedIn(session) == True:
        return HttpResponseRedirect(main_key.TO_HOME_PAGE)  # Redirect after POST
    # endregion

    if request.method == main_key.POST:  # If the form has been submitted...
        form = RegisterForm(post)  # A form bound to the POST data
        if form.is_valid():
            username = form.data[reg_key.USERNAME]
            display_name = form.data[reg_key.DISPLAY_NAME]
            email = form.data[reg_key.EMAIL]
            password = form.data[reg_key.PASSWORD]
            gender = form.data[reg_key.GENDER]
            user = CreateUser(username, password, email, display_name, gender)
            session[reg_key.REGISTERED] = SendEmail(user, main_key.ACTIVATION_EMAIL_PATH, None)
            return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    else:
        form = RegisterForm()  # An unbound form

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.FORM: form
    }
    return render(request, main_key.REGISTER_PAGE, context)


def activate(request, key):
    title = main_key.ACTIVATION_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    activation_expired = False
    already_active = False
    is_success = False
    session = request.session

    # region check is logged_in to main page
    if CheckIsLoggedIn(session) == True:
        return HttpResponseRedirect(main_key.TO_HOME_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByActivationKey(key)
    if user != False:
        if user.is_active is False:
            if datetime.datetime.now() > user.key_expires:
                activation_expired = True  # Display : offer to user to have another activation l ink (a link in template sending to the view new_activation_link)
            else:  # Activation successful
                user.is_active = True
                user.save()
                is_success = True
        else:  # If user is already active, simply display error message
            already_active = True  # Display : error message

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.SUCCESS: act_key.SUCCESSFUL_ACTIVATE_MSG + " " + main_key.PAGE_REDIRECT if is_success is True else None,
        main_key.FOUND: act_key.ACTIVATION_KEY_NOT_FOUND + " " + main_key.PAGE_REDIRECT if is_success is False else None,
        act_key.IS_EXPIRED: act_key.IS_EXPIRED_MSG + " " + main_key.PAGE_REDIRECT if activation_expired is True else None,
        act_key.IS_ALREADY_ACTIVE: act_key.IS_ACTIVATED_MSG + " " + main_key.PAGE_REDIRECT if already_active is True else None,
    }
    return render(request, main_key.ACTIVATION_PAGE, context)


def activation(request):
    title = main_key.ACTIVATION_PAGE_TITLE
    form = ActivationForm
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to main page
    if CheckIsLoggedIn(session) == True:
        return HttpResponseRedirect(main_key.TO_HOME_PAGE)  # Redirect after POST
    # endregion

    if request.method == main_key.POST:
        form = ActivationForm(post)
        if form.is_valid():
            user = GetUserByUsernameOrEmail(form.data[act_key.ACCOUNT])
            if user != False:
                if user.is_active == False:
                    GenerateActivationKey(user)
                    session[reg_key.REGISTERED] = SendEmail(user, main_key.ACTIVATION_EMAIL_PATH, None)
                    return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    else:
        form = ActivationForm()

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.FORM: form,
        main_key.MESSAGE: act_key.ENTER_ACCOUNT_FOR_NEW_LINK,
    }
    return render(request, main_key.ACTIVATION_PAGE, context)


def forget_password(request):
    title = main_key.RESET_PASSWORD_PAGE_TITLE
    form = ResetPasswordForm
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    is_not_activated = False
    # region check is logged_in to main page
    if CheckIsLoggedIn(session) == True:
        return HttpResponseRedirect(main_key.TO_HOME_PAGE)  # Redirect after POST
    # endregion

    if request.method == main_key.POST:
        form = ResetPasswordForm(post)
        if form.is_valid():
            user = GetUserByUsernameOrEmail(form.data[act_key.ACCOUNT])
            if user != False:
                if user.is_active == False:
                    is_not_activated = True
                else:
                    new_password = GenerateRandomPassword(user)
                    session[reg_key.REGISTERED] = SendEmail(user, main_key.RESET_PASSWORD_EMAIL_PATH, new_password)
                    return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    else:
        form = ResetPasswordForm()

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.FORM: form,
        main_key.MESSAGE: res_key.ENTER_ACCOUNT_FOR_NEW_PASSWORD,
        log_key.IS_NOT_ACTIVATED: log_key.IS_NOT_ACTIVATED_MSG + " " + main_key.PAGE_REDIRECT if is_not_activated is True else None,
    }
    return render(request, main_key.FORGET_PASSWORD_PAGE, context)


# endregion

# region following/user_following/followers/user_followers

def following_view(request):
    title = main_key.FOLLOWING_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    count = ''
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    user_pagination = user.following
    # region pagination
    if user_pagination != []:
        user_pagination.sort(key=lambda x: x.user.display_name)
        paginator = Paginator(user_pagination, 2)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            user_pagination = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            user_pagination = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            user_pagination = paginator.page(paginator.num_pages)

        for item in range(user_pagination.paginator.num_pages):
            count += str(item)
    # endregion

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.USER: user,
        main_key.PAGE_COUNT: count,
        main_key.USER_PAGINATION: user_pagination,
        main_key.POSTS_NUMBER: GetUserNumberPosts(user_pagination),
    }
    return render(request, main_key.FOLLOWING_PAGE, context)


def user_following_view(request, key):
    title = main_key.USER_FOLLOWING_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    count = ''
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    user2 = GetUserByObjectID(key)
    requested = GetRequestedLogByUser(user)
    user2 = RemoveUserFollowing(user, user2)
    user_pagination = user2.following
    # region pagination
    user_pagination.sort(key=lambda x: x.user.display_name)
    paginator = Paginator(user_pagination, 2)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        user_pagination = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_pagination = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user_pagination = paginator.page(paginator.num_pages)

    for item in range(user_pagination.paginator.num_pages):
        count += str(item)
    # endregion
    context = {
        main_key.TEMPLATE_TITLE: title % user2.display_name,
        main_key.USER: user,
        main_key.USER2: user2,
        main_key.PAGE_COUNT: count,
        main_key.USER_PAGINATION: user_pagination,
        main_key.REQUESTED: CheckIsRequestedByUserFollowing(user2, requested),
        main_key.FOLLOWED: CheckIsFollowedByUserFollowing(user, user2),
        main_key.POSTS_NUMBER: GetUserNumberPosts(user_pagination),
    }
    return render(request, main_key.USER_FOLLOWING_PAGE, context)


def followers_view(request):
    title = main_key.FOLLOWERS_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    count = ''
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    requested = GetRequestedLogByUser(user)
    user_pagination = user.followers
    # region pagination
    if user_pagination != []:
        user_pagination.sort(key=lambda x: x.user.display_name)
        paginator = Paginator(user_pagination, 2)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            user_pagination = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            user_pagination = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            user_pagination = paginator.page(paginator.num_pages)

        for item in range(user_pagination.paginator.num_pages):
            count += str(item)
    # endregion

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.USER: user,
        main_key.PAGE_COUNT: count,
        main_key.USER_PAGINATION: user_pagination,
        main_key.REQUESTED: CheckIsRequestedByUserFollowers(user, requested),
        main_key.FOLLOWED: CheckIsFollowedByUserFollowers(user, user),
        main_key.POSTS_NUMBER: GetUserNumberPosts(user_pagination),
    }
    return render(request, main_key.FOLLOWERS_PAGE, context)


def user_followers_view(request, key):
    title = main_key.USER_FOLLOWERS_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    count = ''
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    user2 = GetUserByObjectID(key)
    requested = GetRequestedLogByUser(user)
    user2 = RemoveUserFollowers(user, user2)
    user_pagination = user2.followers
    # region pagination
    user_pagination.sort(key=lambda x: x.user.display_name)
    paginator = Paginator(user_pagination, 2)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        user_pagination = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_pagination = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user_pagination = paginator.page(paginator.num_pages)

    for item in range(user_pagination.paginator.num_pages):
        count += str(item)
    # endregion
    context = {
        main_key.TEMPLATE_TITLE: title % user2.display_name,
        main_key.USER: user,
        main_key.USER2: user2,
        main_key.PAGE_COUNT: count,
        main_key.USER_PAGINATION: user_pagination,
        main_key.REQUESTED: CheckIsRequestedByUserFollowers(user2, requested),
        main_key.FOLLOWED: CheckIsFollowedByUserFollowers(user, user2),
        main_key.POSTS_NUMBER: GetUserNumberPosts(user_pagination),
    }
    return render(request, main_key.USER_FOLLOWERS_PAGE, context)


# endregion

# region request/private/newsfeed notifications view
def request_notifications_view(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session

    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    context = {
        main_key.USER: user,
        main_key.REQUEST_LOG: GetUserRequestedLogByUser(user),
    }
    return render(request, main_key.REQUEST_NOTIFICATIONS_PAGE, context)


def private_notifications_view(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session

    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    context = {
        main_key.USER: user,
        main_key.PRIVATE_LOG: GetPrivateLogByUser(user),
    }
    return render(request, main_key.PRIVATE_NOTIFICATIONS_PAGE, context)


def newsfeed_notifications_view(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session

    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    context = {
        main_key.USER: user,
        main_key.FOLLOWING_USER_LOG: GetFollowingUserLog(user),
    }
    return render(request, main_key.NEWSFEED_NOTIFICATIONS_PAGE, context)


def chatlist_view(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session

    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    context = {
        main_key.USER: user,
    }
    return render(request, main_key.CHATLIST_PAGE, context)
# endregion

def index(request):
    title = main_key.HOME_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    count = ""
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    liked_posts = GetUserLikedPosts(user)
    posts = GetFollowingUserPost(user)
    posts_pagination = posts
    # region pagination
    if posts_pagination != []:
        paginator = Paginator(posts_pagination, 5)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            posts_pagination = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts_pagination = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts_pagination = paginator.page(paginator.num_pages)

        for item in range(posts_pagination.paginator.num_pages):
            count += str(item)
    # endregion
    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.POSTS: posts_pagination ,
        main_key.PAGE_COUNT: count,
        main_key.OWN_POSTS: GetOwnPost(user),
        main_key.USER: user,
        main_key.LIKED_POSTS: liked_posts,
    }
    return render(request, main_key.HOME_PAGE, context)


def settings_view(request):
    title = main_key.SETTINGS_PAGE_TITLE
    form = SettingsForm
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    updated = False
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    if set_key.UPDATED in session:
        updated = True
        del session[set_key.UPDATED]

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])

    if request.method == main_key.POST:  # If the form has been submitted...
        form = SettingsForm(post)  # A form bound to the POST data
        if form.is_valid():
            display_name = form.data[reg_key.DISPLAY_NAME]
            privacy = form.data[set_key.PRIVACY]
            password = form.data[set_key.PASSWORD]
            user = UpdateSettings(user, display_name, privacy, password)
            if user == True:
                session[set_key.UPDATED] = True
            return HttpResponseRedirect(main_key.TO_SETINGS_PAGE)  # Redirect after POST
    else:
        form = SettingsForm()  # An unbound form

    form.fields[reg_key.DISPLAY_NAME].initial = user.display_name
    form.fields[set_key.PRIVACY].initial = user.need_request
    form.fields[reg_key.USERNAME].initial = user.username
    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.FORM: form,
        main_key.USER: user,
        set_key.UPDATED: set_key.UPDATE_SUCCESSFUL_MSG if updated is True else None,
    }
    return render(request, main_key.SETTINGS_PAGE, context)


def profile_view(request, key):
    title = main_key.PROFILE_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    count = ''

    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    user2 = GetUserByObjectID(key)
    posts = GetProfilePosts(user2)
    posts_pagination = posts
    # region pagination
    if posts_pagination != []:
        paginator = Paginator(posts_pagination, 5)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            posts_pagination = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts_pagination = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts_pagination = paginator.page(paginator.num_pages)

        for item in range(posts_pagination.paginator.num_pages):
            count += str(item)
    # endregion
    context = {
        main_key.TEMPLATE_TITLE: title % user2.display_name,
        main_key.USER: user,
        main_key.USER2: user2,
        main_key.POSTS: posts_pagination,
        main_key.PAGE_COUNT: count,
        main_key.POSTS_NUMBER: GetUserProfileNumberPosts(user2),
    }
    return render(request, main_key.PROFILE_PAGE, context)


def messages_view(request):
    title = main_key.LOGIN_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session

    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.USER: user,
    }
    return render(request, 'messages.html', context)


# region ajax
@csrf_exempt
def arequest_notifications_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    success = True
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    log = GetRequestedLogByObjectID(ObjectId(post[main_key.REQUEST_LOG_ID]))
    user2 = GetUserByObjectID(log.user.id)
    if log != False:
        log.status = True
        log.edited_date_time = datetime.datetime.now()
        log.save()
        following = CreateFollowingData(user)
        followers = CreateFollowersData(user2)
        user2.following.append(following)
        user.followers.append(followers)
        user2.save()
        user.save()
        CreateUserLog(user, main_key.LOG_TYPE_CHOICES[1][1], main_key.LOG_TYPE_CHOICES[1][0], user2, None)
        CreatePrivateLog(user2, main_key.PRIVATE_LOG_TYPE_CHOICES[1][1], main_key.PRIVATE_LOG_TYPE_CHOICES[1][0], user,
                         None)
        PrivateTrigger(user, user2, tri_key.REQUEST_ACCEPTED_EVENT, tri_key.ACCEPT_REQUEST_MSG, str(user.id))
    else:
        success = False
    return HttpResponse(jsonify({main_key.SUCCESS: success}))


@csrf_exempt
def rrequest_notifications_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    success = True
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    log = GetRequestedLogByObjectID(ObjectId(post[main_key.REQUEST_LOG_ID]))
    if log != False:
        log.status = None
        log.edited_date_time = datetime.datetime.now()
        log.save()
    else:
        success = False
    return HttpResponse(jsonify({main_key.SUCCESS: success}))


@csrf_exempt
def crequest_notifications_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    user.request_notifications = False;
    user.save()
    return HttpResponse(jsonify({main_key.SUCCESS: True}))


@csrf_exempt
def cprivate_notifications_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    user.private_notifications = False;
    user.save()
    return HttpResponse(jsonify({main_key.SUCCESS: True}))


@csrf_exempt
def action_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    temp = []
    temp2 = []
    status = main_key.STATUS_NONE
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    data = post[main_key.FRIENDS]
    user2 = GetUserByObjectID(ObjectId(data))
    for item in user.following:
        if item.user.id == ObjectId(data):
            temp.append(item)
            break

    if temp == []:
        requested = CheckIsRequested(user, user2)
        if user2.need_request is True:
            if requested == False:
                CreateRequestsLog(user, user2)
                status = main_key.STATUS_FALSE
            else:
                requested.delete()
        else:
            if requested != False:
                requested.delete()
            else:
                following = CreateFollowingData(user2)
                followers = CreateFollowersData(user)
                user.following.append(following)
                user2.followers.append(followers)
                user2.save()
                CreateUserLog(user, main_key.LOG_TYPE_CHOICES[3][1], main_key.LOG_TYPE_CHOICES[3][0], user2, None)
                CreatePrivateLog(user2, main_key.PRIVATE_LOG_TYPE_CHOICES[3][1],
                                 main_key.PRIVATE_LOG_TYPE_CHOICES[3][0], user, None)
                PrivateTrigger(user, user2, tri_key.REQUEST_ACCEPTED_EVENT, tri_key.FOLLOWING_MSG, str(user.id))
                status = main_key.STATUS_TRUE
    else:
        user.following.remove(temp[0])
        for item in user2.followers:
            if item.user.id == user.id:
                temp2.append(item)
                break
        if temp2 != []:
            user2.followers.remove(temp2[0])
            user2.save()

    user.save()
    if status == main_key.STATUS_FALSE:
        PrivateTrigger(user, user2, tri_key.REQUEST_EVENT, tri_key.SENT_REQUEST_MSG, None)
        user2.request_notifications = True
        user2.save()

    return HttpResponse(jsonify({main_key.SUCCESS: status}))


@csrf_exempt
def seen_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    data = post[main_key.SEEN]
    log = GetUserLogByObjectId(ObjectId(data))
    temp = []
    for item in log.seen:
        temp.append(item.user)

    if user not in temp:
        log.seen.append(CreateSeen(user))
        log.save()

    return HttpResponse(jsonify({main_key.SUCCESS: True}))


@csrf_exempt
def newsfeedmenu_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion

    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])

    if user.open_news_feeds:
        user.open_news_feeds = False
    else:
        user.open_news_feeds = True

    user.save()

    return HttpResponse(jsonify({main_key.SUCCESS: True}))


@csrf_exempt
def post_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    posts = post[main_key.POSTS]
    address = post[main_key.ADDRESS]
    address_code = post[main_key.ADDRESS_CODE]
    if address == '' or address_code == '':
        address = None
        address_code = None

    data = CreatePost(user, posts, address, address_code)
    log = CreateUserLog(user, main_key.LOG_TYPE_CHOICES[2][1], main_key.LOG_TYPE_CHOICES[2][0], None, data)
    context = {
        main_key.POST_ID: str(data.id),
        main_key.USER_ID: str(user.id),
        main_key.USER_IMAGE: user.profile_image,
        main_key.USER_DISPLAY_NAME: user.display_name,
        main_key.POSTED_DATE_TIME: str(data.created_date_time),
        main_key.POST_CONTENT: data.content,
        main_key.POST_LOCATION: data.location,
        main_key.POST_LOCATION_CODE: data.location_code,
        main_key.POST_LIKE_NUMBER: len(data.likes),
        main_key.POST_SHARE_NUMBER: len(data.share),
        main_key.POST_COMMENT_NUMBER: len(data.comments),
    }
    return HttpResponse(jsonify(context))

@csrf_exempt
def likes_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    likes = post[main_key.LIKES]
    posts = GetPostsByObjectID(ObjectId(likes))
    if posts != False:
        liked = GetUserLikesByPosts(posts, user)
        if liked == False:
            posts = CreateUserLikesForPosts(posts, user)
            CreateUserLog(user, main_key.LOG_TYPE_CHOICES[4][1], main_key.LOG_TYPE_CHOICES[4][0], posts.user, posts)
            if posts.user != user:
                CreatePrivateLog(posts.user, main_key.PRIVATE_LOG_TYPE_CHOICES[4][1], main_key.PRIVATE_LOG_TYPE_CHOICES[4][0], user, posts)
                PrivateTrigger(user, posts.user, tri_key.REQUEST_ACCEPTED_EVENT, tri_key.LIKES_MSG, str(posts.id))
        else:
            posts = RemoveUserLikesForPosts(posts, user)

    return HttpResponse(jsonify({main_key.SUCCESS: posts != False, main_key.NUMBER: len(posts.likes)}))

@csrf_exempt
def comment_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    posts = post[main_key.POSTS]
    content = post[main_key.POST_COMMENT]
    posts = GetPostsByObjectID(ObjectId(posts))
    if posts != False:
        comment = Comments()
        comment.user = user
        comment.created_date_time = datetime.datetime.now()
        comment.content = content
        posts.comments.append(comment)
        posts.save()
        CreateUserLog(user, main_key.LOG_TYPE_CHOICES[6][1], main_key.LOG_TYPE_CHOICES[6][0], posts.user, posts)
        if posts.user != user:
            CreatePrivateLog(posts.user, main_key.PRIVATE_LOG_TYPE_CHOICES[6][1], main_key.PRIVATE_LOG_TYPE_CHOICES[6][0], user, posts)
            PrivateTrigger(user, posts.user, tri_key.REQUEST_ACCEPTED_EVENT, tri_key.COMMENT_MSG, str(posts.id))

    return HttpResponse(jsonify({main_key.SUCCESS: posts != False,
                                  main_key.NUMBER: len(posts.comments),
                                  main_key.USER_ID: str(user.id),
                                  main_key.CONTENT: comment.content,
                                  main_key.USER_IMAGE: user.profile_image,
                                  main_key.USER_DISPLAY_NAME: user.display_name,
                                  main_key.CREATED_DATE_TIME: humanize.naturaltime(comment.created_date_time)}))

@csrf_exempt
def share_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    posts = post[main_key.POSTS]
    content = post[main_key.POST_CONTENT]
    created_post = CreatePost(user, content, None, None)
    posts = GetPostsByObjectID(ObjectId(posts))
    if posts != False:
        share = Share()
        share.user = user.to_dbref()
        share.created_date_time = datetime.datetime.now()
        posts.share.append(share)
        posts.save()
        created_post.from_user = posts.user.to_dbref() if posts.from_user is None else posts.from_user.to_dbref()
        created_post.from_posts = posts.to_dbref() if posts.from_posts is None else posts.from_posts.to_dbref()
        created_post.save()
        CreateUserLog(user, main_key.LOG_TYPE_CHOICES[5][1], main_key.LOG_TYPE_CHOICES[5][0], posts.user, posts)
        if posts.user != user:
            CreatePrivateLog(posts.user, main_key.PRIVATE_LOG_TYPE_CHOICES[5][1], main_key.PRIVATE_LOG_TYPE_CHOICES[5][0], user, posts)
            PrivateTrigger(user, posts.user, tri_key.REQUEST_ACCEPTED_EVENT, tri_key.SHARE_MSG, str(posts.id))

    return HttpResponse(jsonify({main_key.SUCCESS: posts != False}))

@csrf_exempt
def delete_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    delete = post[main_key.DELETE]
    posts = GetPostsByObjectID(ObjectId(delete))
    if posts != False:
        posts.delete()
    return HttpResponse(jsonify({main_key.SUCCESS: posts != False}))

@csrf_exempt
def edit_post_ajax(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    posts = post[main_key.POSTS]
    content = post[main_key.POST_CONTENT]
    posts = GetPostsByObjectID(ObjectId(posts))
    if posts != False:
        posts.content = content
        posts.edited_date_time = datetime.datetime.now()
        posts.save()

    return HttpResponse(jsonify({main_key.SUCCESS: posts != False}))

def jsonify(object, fields=None, to_dict=False):
    '''Funcion utilitaria para convertir un query set a formato JSON'''
    try:
        import json
    except ImportError:
        import django.utils.simplejson as json

    out = []

    if type(object) not in [dict, list, tuple]:
        for i in object:
            tmp = {}
            if fields:
                for field in fields:
                    tmp[field] = unicode(i.__getattribute__(field))
            else:
                for attr, value in i.__dict__.iteritems():
                    tmp[attr] = value
            out.append(tmp)
    else:
        out = object

    if to_dict:
        return out
    else:
        return json.dumps(out)


# endregion

# region commerce
def commerce(request):
    title = main_key.COMMERCE_PAGE_TITLE
    form = LoginForm
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    product = GetProduct()

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.FORM: form,
        main_key.USER: user,
        main_key.PRODUCT: product
    }
    return render(request, 'commerce.html', context)


# endregion

def sellingList(request):
    title = main_key.SELLINGLIST_PAGE_TITLE
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    form = LoginForm
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    following_user_log = GetFollowingUserLog(user)
    product = Product.objects.filter(seller=user)
    category = GetCategory()

    context = {
        main_key.TEMPLATE_TITLE: title,
        main_key.FORM: form,
        main_key.USER: user,
        main_key.PRODUCT: product,
        main_key.CATEGORY: category,
        main_key.FOLLOWING_USER_LOG: following_user_log
    }

    if request.POST.get('id'):
        return HttpResponse(1)
    else:
        return render(request, 'sellinglist.html', context)


@csrf_exempt
def addProduct(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])

    dataUser = user
    dataName = json.loads(request.POST.get('name'))
    dataCategory = json.loads(request.POST.get('category'))
    dataGender = json.loads(request.POST.get('gender'))
    dataPrice = json.loads(request.POST.get('price'))
    dataDesc = json.loads(request.POST.get('desc'))
    dataImage = json.loads(request.POST.get('image'))
    # dataTag = json.loads(request.POST.get('tag'))

    product = Product(
        name=dataName,
        category=dataCategory,
        gender=dataGender,
        price=dataPrice,
        description=dataDesc,
        status='Available',
        image=dataImage,
        create_date=datetime.datetime.now(),
        discount='20%',
        seller=dataUser
    )

    product.save()
    return HttpResponse(jsonify({main_key.SUCCESS: True}))


@csrf_exempt
def editProduct(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    # pid = request.GET.get('pid','')
    pid = json.loads(request.POST.get('pid'))
    pStatus = json.loads(request.POST.get('status'))
    # p = Product.objects.get(id = ObjectId('56d144348df0554f85646d0a'))
    p = Product.objects.get(id=ObjectId(pid))
    p.status = pStatus
    p.save()
    return HttpResponse(jsonify({main_key.SUCCESS: True}))


@csrf_exempt
def removeProduct(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    pid = request.GET.get('pid', '')
    p = Product.objects.get(id=pid)
    p.delete()
    return HttpResponseRedirect('/sellingList/')


def purchaseHistory(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    form = LoginForm
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    following_user_log = GetFollowingUserLog(user)
    ph = Purchase.objects.all()
    product = GetProduct()
    context = {
        main_key.TEMPLATE_TITLE: 'Purchase History',
        main_key.FORM: form,
        main_key.USER: user,
        main_key.PURCHASE_HISTORY: ph,
        # main_key.PRODUCT: product,
        # main_key.FOLLOWING_USER_LOG: following_user_log,

    }
    return render(request, 'purchasehistory.html', context)


@csrf_exempt
def topup(request):
    post = request.POST
    post._mutable = True  # allow change data in request.POST
    session = request.session
    form = LoginForm
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    following_user_log = GetFollowingUserLog(user)

    context = {
        main_key.TEMPLATE_TITLE: 'Top Up',
        main_key.USER: user,
        main_key.FOLLOWING_USER_LOG: following_user_log,
        main_key.FORM: form,
    }
    return render(request, 'topup.html', context)


@csrf_exempt
def paypal(request):

    if 'topUp10' in request.POST:
        paypal_itemName = "Top Up Level 1"
        paypal_amount = "10"
    elif 'topUp30' in request.POST:
        paypal_itemName = "Top Up Level 2"
        paypal_amount = "30"
    elif 'topUp75' in request.POST:
        paypal_itemName = "Top Up Level 3"
        paypal_amount = "75"
    elif 'topUp150' in request.POST:
        paypal_itemName = "Top Up Level 4"
        paypal_amount = "150"
    else:
        paypal_itemName = "Top Up Level 5"
        paypal_amount = "300"

    paypal_url = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_xclick&business=friendship_api1.live.com'
    paypal_business = "friendship@live.com"
    paypal_quantity = "1"
    paypal_returnUrl = "http://localhost:8000/commerce/"
    paypal_cancelUrl = "http://localhost:8000/topup/"

    paypal_url = paypal_url + '&first_name=Han' + "&business=" + paypal_business + "&item_name=" + paypal_itemName + "&amount=" + paypal_amount + "&quantity=" + paypal_quantity + "&return=" + paypal_returnUrl + "&cancel_return=" + paypal_cancelUrl
    return HttpResponseRedirect(paypal_url)


def product_detail(request):
    post = request.POST
    post._mutable = True
    session = request.session
    form = LoginForm
    # region check is logged_in to login page
    if CheckIsLoggedIn(session) == False:
        return HttpResponseRedirect(main_key.TO_LOGIN_PAGE)  # Redirect after POST
    # endregion
    user = GetUserByUsernameOrEmail(session[log_key.LOGIN_USER])
    following_user_log = GetFollowingUserLog(user)
    pid = request.GET.get('pid', '')
    p = GetProductDetail(pid)
    context = {
        main_key.TEMPLATE_TITLE: 'Product Detail',
        main_key.FORM: form,
        main_key.USER: user,
        main_key.PRODUCT_DETAIL: p,
        main_key.FOLLOWING_USER_LOG: following_user_log,
    }

    return render(request, 'product_details.html', context)
