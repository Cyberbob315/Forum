from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from accounts.api.urls import router as account_router
from subjects.api.urls import router as subject_router
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_page, name='home'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^forum/', include('subforums.urls', namespace='forum')),
    url(r'^threads/', include('threads.urls', namespace='threads')),
    url(r'^search/', views.search, name='search'),
    url(r'^api/subforum/', include(
        'subforums.api.urls', namespace='subforum-api')),
    url(r'^api/thread/', include('threads.api.urls', namespace='thread-apis')),
    url(r'^api/comment/',
        include('comments.api.urls', namespace='comment-apis')),
    url(r'^api/account/',
        include(account_router.urls, namespace='account-api')),
    url(r'^student/', include('subjects.urls', namespace='student')),
    url(r'^student_admin/',
        include('admin_student.urls', namespace='student_admin')),
    url(r'^api/subject-mark/',
        include(subject_router.urls, namespace='subject-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
