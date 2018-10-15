from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
   path('fup/from/<int:from_year>/<int:from_month>/<int:from_day>/to/<int:to_year>/<int:to_month>/<int:to_day>', views.fup, name='fup'),
   # path('<int:question_id>/results/', views.results, name='results'),
   # path('<int:question_id>/vote/', views.vote, name='vote'),
        ]
