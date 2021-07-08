from django.urls import path
from django.conf.urls import url
from .views import *
from Rooms.admin import admin_site

urlpatterns = [
    url(r'^sabhe-booking/', admin_site.urls),
    path('', index, name='index'),
    path('rooms/', room_list, name='rooms_list'),
    path('add/', rooms_create, name='rooms_create'),
    path('edit/<int:id>', rooms_edit, name='room_edit'),
    path('delete/<int:id>', rooms_delete, name='room_delete'),
    path('donations/', donations_list, name='donations_list'),
    path('donations_add/', donations_add, name='donations_add'),
    path('ambulance/', ambulance_list, name='ambulance_list'),
    path('ambulance_add/', ambulance_add, name='ambulance_add'),
    path('booking_list/', booking_list, name='booking_list'),
    path('booking_add/', booking_add, name='booking_add'),
    path('booking_edit/<int:id>', booking_edit, name='booking_edit'),
    path('reports_view/', reports_view, name='reports_view'),
    path('pdf/', view_pdf, name='view_pdf'),
    path('view_receipt/<int:booking_id>', view_receipt, name='view_receipt'),
    path('view_ambulance_receipt/<int:booking_id>', view_ambulance_pdf, name='view_ambulance_receipt'),
    path('view_donation_receipt/<int:booking_id>', view_donations_pdf, name='view_donations_receipt'),
    path('expenses_add/', expenses_add, name='expenses_add'),
    path('view_expense_receipt/<int:booking_id>', view_expense_receipt, name='view_expense_receipt'),
    path('view_tomorrow_pdf/', view_tomorrow_pdf, name='view_tomorrow_pdf'),
    path('detailed_report_view/', detailed_view, name='detailed_report_view'),
    path('detailed_report_pdf/', view_detailed_pdf, name='detailed_report_pdf'),
    path('today_booking/', today_booking, name='today_booking'),
    path('booking_cancel/<int:booking_id>', booking_cancel, name='booking_cancel'),
]
