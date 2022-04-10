from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/FaDi1997/admin/', admin.site.urls),

    # Editor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Blog App
    path('', include('blog.urls')),

    #Accounts App
    path('accounts/', include('accounts.urls')),

    # Articles App
    path('articles/', include('articles.urls')),

    # Search App
    path('search/', include('search.urls')),

    # Comments App
    path('comments/', include('comments.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)