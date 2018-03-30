"""code_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import threading

from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import SimpleRouter

from core import views
from core.commit_input_handler import main


router = SimpleRouter()
router.register(r'monitor', views.MonitorView)
router.register(r'commit', views.CommitView)

urlpatterns = router.urls + [
    # url(r'^', include(router.urls)),
    url(r'^$', views.CodeBoard.as_view(), name='code-board'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^reports/', views.ReportView.as_view(), name='report'),
    url(r'^user/issues/(?P<user_id>[0-9]+)/', views.UserIssues.as_view(), name='issues-users'),
    url(r'^user/compare/', views.UserCompare.as_view(), name='compare-users'),
]

process_data = main.ProcessData()
download_thread = threading.Thread(target=process_data.run_consumer)
download_thread.start()
