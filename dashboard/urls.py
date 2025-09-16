from django.urls import path
from . import views

app_name = "dashboard"   # 🔥 namespace qo‘shildi

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),   # /dashboard/
    path('index/', views.dashboard_view, name='index'), # /dashboard/index/
    path('stats/input/', views.stats_input_view, name='stats_input'),
    path('expense/input/', views.expense_input_view, name='expense_input'),
    path('expense/chart/', views.expense_chart_view, name='expense_chart'),
    path('expense/pie/', views.expense_pie_chart_view, name='expense_pie_chart'),
    path('expense/recent/', views.recent_expense_chart_view, name='recent_expense_chart'),
]
