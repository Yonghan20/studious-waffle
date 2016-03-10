"""SocialCommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]"""
from django.conf.urls import patterns, url, include
urlpatterns = patterns('',
    url(r'^$', 'SocialCommerceApp.views.index', name='FriendShip'),
    url(r'^login/', 'SocialCommerceApp.views.login_view', name='Login'),
    url(r'^logout/', 'SocialCommerceApp.views.logout_view', name='Login'),
    url(r'^register/', 'SocialCommerceApp.views.register_view', name='Registration'),
    url(r'^activation/', 'SocialCommerceApp.views.activation', name='Activation'),
    url(r'^activate/(?P<key>.+)/', 'SocialCommerceApp.views.activate', name='Activation'),
    url(r'^forgetpassword/', 'SocialCommerceApp.views.forget_password', name='Forget Password'),
    url(r'^profile/(?P<key>.+)/', 'SocialCommerceApp.views.profile_view', name='Profile'),
    url(r'^messages/', 'SocialCommerceApp.views.messages_view', name='Messages'),
    url(r'^settings/', 'SocialCommerceApp.views.settings_view', name='Messages'),
    url(r'^following/', 'SocialCommerceApp.views.following_view', name='Following'),
    url(r'^user_following/(?P<key>.+)/', 'SocialCommerceApp.views.user_following_view', name='User Following'),
    url(r'^followers/', 'SocialCommerceApp.views.followers_view', name='Followers'),
    url(r'^user_followers/(?P<key>.+)/', 'SocialCommerceApp.views.user_followers_view', name='User Followers'),
    url(r'^chatlist_view/', 'SocialCommerceApp.views.chatlist_view', name='ChatList'),
    url(r'^action/', 'SocialCommerceApp.views.action_ajax', name='Action'),
    url(r'^seen/', 'SocialCommerceApp.views.seen_ajax', name='Seen'),
    url(r'^newsfeed_menuaction/', 'SocialCommerceApp.views.newsfeedmenu_ajax', name='Seen'),
    url(r'^commerce/', 'SocialCommerceApp.views.commerce', name='E-Commerce'),
    url(r'^sellingList/', 'SocialCommerceApp.views.sellingList', name='Selling List'),
    url(r'^product_details/', 'SocialCommerceApp.views.product_detail', name='Product Details'),
    url(r'^addProduct/', 'SocialCommerceApp.views.addProduct', name='Add Product'),
    url(r'^editProduct/', 'SocialCommerceApp.views.editProduct', name='Edit Product'),
    url(r'^removeProduct/', 'SocialCommerceApp.views.removeProduct', name='Remove Product'),
    url(r'^purchaseHistory/', 'SocialCommerceApp.views.purchaseHistory', name='Purchase History'),
    url(r'^posts_ajax/', 'SocialCommerceApp.views.post_ajax', name='Posts'),
    url(r'^likes_ajax/', 'SocialCommerceApp.views.likes_ajax', name='Likes'),
    url(r'^share_ajax/', 'SocialCommerceApp.views.share_ajax', name='Share'),
    url(r'^delete_ajax/', 'SocialCommerceApp.views.delete_ajax', name='Delete'),
    url(r'^edit_post_ajax/', 'SocialCommerceApp.views.edit_post_ajax', name='Edit'),
    url(r'^comment_ajax/', 'SocialCommerceApp.views.comment_ajax', name='Load Comment'),
    url(r'^topup/', 'SocialCommerceApp.views.topup', name='Top Up'),
    url(r'^paypal/', 'SocialCommerceApp.views.paypal', name='Pay Pal'),
    #c=clear a=accept r=reject
    url(r'^arequest_notifications/', 'SocialCommerceApp.views.arequest_notifications_ajax', name='aRequest Notifications'),
    url(r'^rrequest_notifications/', 'SocialCommerceApp.views.rrequest_notifications_ajax', name='rRequest Notifications'),
    url(r'^crequest_notifications/', 'SocialCommerceApp.views.crequest_notifications_ajax', name='cRequest Notifications'),
    url(r'^request_notifications/', 'SocialCommerceApp.views.request_notifications_view', name='Request Notifications'),
    url(r'^cprivate_notifications/', 'SocialCommerceApp.views.cprivate_notifications_ajax', name='cPrivate Notifications'),
    url(r'^private_notifications/', 'SocialCommerceApp.views.private_notifications_view', name='Private Notifications'),
    url(r'^newsfeed_notifications/', 'SocialCommerceApp.views.newsfeed_notifications_view', name='NewsFeed Notifications'),
)
