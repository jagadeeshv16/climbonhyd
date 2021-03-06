from django.conf.urls import url
from . import views
from django.urls import path, include
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    path('dashboard/', views.Home.as_view(), name="home_page"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('thank-you/', views.RegistrationSuccess.as_view(), name="thank_you"),
    path('login/', views.LogInView.as_view(), name="login"),
    path('userdashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('logout/', views.LogOutView.as_view(), name="logout"),
    path('profile-edit/', views.ProfileEdit.as_view(), name="profile_edit"),
    path('password-reset/', views.ForgotPassword.as_view(), name="password_reset"),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('password-reset/done/', views.PasswordResetSuccessView.as_view(), name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.PasswordResetConfirmationEmail.as_view(), name="password_reset_confirm"),
    path('staff/', views.StaffList.as_view(), name='staff_list'),
    path("inactive/<int:id>/", views.staff_inactive, name="staff_inactive"),
    path("active/<int:id>/", views.staff_active, name="staff_active"),
    path("staffadd/<int:id>/", views.staff_add, name="staff_add"),
    path("staffremove/<int:id>/", views.staff_remove, name="staff_remove"),
    path("staffedit/<int:id>/", views.staff_edit, name="staff_edit"),
    path("staffdelete/<int:pk>/", views.StaffDelete.as_view(), name="staffdelete"),
    path('sitecontent/', views.SiteContentCreateView.as_view(), name="sitecontent"),
    path('contentlist/',views.SiteContentList.as_view(), name='sitecontent_list'),
    path('sitecontentupdate/<int:pk>/', views.SiteContentUpdate.as_view(), name="sitecontent_update"),
    path('sitecontentdelete/<int:pk>/', views.SiteContentDelete.as_view(), name="sitecontent_delete"),
    path('up/<int:id>/', views.up, name="up"),
    path('down/<int:id>/', views.down, name="down"),
    path('eventdata/',views.Upcoming_Eventdata.as_view(), name='eventdata'),
    path('pasteventsdata/',views.Past_Eventdata.as_view(), name='pastevents'),
    path('events/', views.EventDataList.as_view(), name='eventslist'),


]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]