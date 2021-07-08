from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from Rooms.models import Rooms, Booking, Donations, Ambulance, Expenses
from .forms import RoomsAddForm, DonationsAddForm, AmbulanceAddForm, BookingAddForm, AvailabilityForm, ReportForm, ExpenseAddForm
import datetime


class RoomList(ListView):
    model = Rooms

class BookingList(ListView):
    model = Booking

# Create your views here.
def index(request):
    booking = Booking.objects.filter(start__lte=datetime.datetime.today(),
                                     end__gte=datetime.datetime.today(),
                                     status = "Booked")
    return render(request, 'index.html', {'bookings': booking})

def room_list(request):
    r = Rooms.objects.all()
    roomdict = {'rooms': r}
    return render(request, 'room_booking.html', context = roomdict)

def rooms_edit(request, id):
    room = Rooms.objects.get(id = id)
    context = {'room': room}
    if request.method == 'GET':
        return render(request, 'rooms_edit.html', context)
    if request.method == "POST":
        room.room_id = request.POST['room_id']
        room.room_type = request.POST['room_type']
        room.price = request.POST['room_price']
        room.save()
        return render(request, "success_template.html", {'type': "Room Edit"})

def rooms_delete(request, id):
    room = Rooms.objects.get(id=id)
    room.delete()
    return render(request, "success_template.html", {'type': "Room Delete"})

def rooms_create(request):
    if request.method == 'POST':
        form = RoomsAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms_list')
        else:
            print(form.errors)
    form = RoomsAddForm()
    return render(request, 'room_add.html', {'form':form})

def donations_add(request):
    if request.method == "POST":
        form = DonationsAddForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return render(request, 'donation_success.html', {'booking': booking})
        else:
            print("Invalid form data")
            print(form.errors)
            return redirect('donations_list')
    form = DonationsAddForm()
    return render(request, 'donations_add.html', {'form':form})

def donations_list(request):
    try:
        donations = Donations.objects.filter(booked_on = datetime.datetime.today())
    except Donations.DoesNotExist:
        donations = None
    context = {
        'donations' : donations
    }
    return render(request, 'donations_list.html', context)

def ambulance_list(request):
    try:
        ambulances = Ambulance.objects.filter(booked_on = datetime.datetime.today())
    except Donations.DoesNotExist:
        ambulances = None
    context = {
        'ambulances' : ambulances
    }
    return render(request, 'ambulance_list.html', context)

def ambulance_add(request):
    if request.method == "POST":
        form = AmbulanceAddForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return render(request,
                          'ambulance_booking_success.html',
                          {'booking': booking})
        else:
            print("Invalid form data")
            print(form.errors)
            return redirect('ambulance_list')
    form = AmbulanceAddForm()
    return render(request, 'ambulance_add.html', {'form':form})

def booking_add(request):
    form = BookingAddForm()
    if request.method == "GET":
        form.fields['room'].initial = request.GET.get('room_id')
        start = datetime.datetime.strptime(request.GET.get('start'), "%B %d, %Y").date()
        end = datetime.datetime.strptime(request.GET.get('end'), "%B %d, %Y").date()
        form.fields['start'].initial = start
        form.fields['end'].initial = end
    elif request.method == "POST":
        form = BookingAddForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start']
            end_date = form.cleaned_data['end']
            room = form.cleaned_data['room']
            RoomsBooked = Booking.objects.filter(room=room,
                                             start__lte=end_date,
                                             end__gte=start_date,
                                             status="Booked")
            if RoomsBooked.count() > 0:
                return render(request, 'booking_failure.html',
                              {'room' : room})
            else:
                print("Successs")
                booking = form.save()
                return render(request,
                              'booking_success.html',
                              {'booking': booking})
        else:
            print("Form is not valid")
    return render(request, 'booking_add.html', {'form':form})

def view_receipt(request, booking_id):
    booking_info = Booking.objects.filter(pk = booking_id)
    for b in booking_info:
        room = Rooms.objects.filter(room_id = b.room)
        for r in room:
            delta = (b.end - b.start)
            if delta.days == 0:
                price = 1 * r.price
            else:
                price = delta.days * r.price
    pdf = render_to_pdf('receipt_pdf.html', {'booking': booking_info,
                                             'price': price})
    return HttpResponse(pdf, content_type='application/pdf')

def view_ambulance_pdf(request, booking_id):
    ambulance_info = Ambulance.objects.filter(pk = booking_id)
    pdf = render_to_pdf('ambulance_receipt_pdf.html', {'booking': ambulance_info})
    return HttpResponse(pdf, content_type='application/pdf')

def view_donations_pdf(request, booking_id):
    donation_info = Donations.objects.filter(pk = booking_id)
    pdf = render_to_pdf('ambulance_receipt_pdf.html', {'booking': donation_info})
    return HttpResponse(pdf, content_type='application/pdf')

def booking_list(request):
    if request.method == "POST":
        cnt = 0
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start']
            end_date = form.cleaned_data['end']
            today = datetime.date.today()
            delta = start_date - today
            if (delta.days > 15):
                    return render(request, 'availability_form.html',
                              {'error': "More than 15 days advance booking is not allowed", 'form' : form}) 
            if (end_date < start_date):
                return render(request, 'availability_form.html',
                              {'error': "End date should be greater than start date", 'form' : form})
            x = Rooms.objects.none()
            for room in Rooms.objects.all():
                RoomsBooked = Booking.objects.filter(room=room.room_id,
                                                     start__lte=end_date,
                                                     end__gte=start_date,
                                                     status="Booked")
                count = RoomsBooked.count()
                count = int(count)
                if count == 0:
                    cnt = cnt + 1
                    x = x | Rooms.objects.filter(pk = room.pk)
            if cnt > 0:
                form = AvailabilityForm()
                context = {'rooms': x, 'count': cnt,
                           'form': form, 'start_date': start_date,
                           'end_date': end_date }
                return render(request, 'availability_form.html', context)
            else:
                print("No rooms availabile")
    form = AvailabilityForm()
    return render(request, 'availability_form.html', {'form': form})


def booking_edit(request, id):
    pass

def __get_booking_details(request):
    context = {}
    total = 0
    if request.method == "GET":
        if request.GET.get('start_year') is not None:
            start_date = datetime.datetime(int(request.GET.get('start_year')),
                                   int(request.GET.get('start_month')),
                                   int(request.GET.get('start_day')))
        else:
            start_date = datetime.datetime.today()

        if request.GET.get('end_year') is not None:
            end_date = datetime.datetime(int(request.GET.get('end_year')),
                                     int(request.GET.get('end_month')),
                                     int(request.GET.get('end_day')))
        else:
            end_date = datetime.datetime.today()

        form = ReportForm()
        context['Ambulance'] = 0
        for ambulance_earnings in Ambulance.objects.filter(
                booked_on__gte=start_date,
                booked_on__lte=end_date):
            context['Ambulance'] += int(ambulance_earnings.amount)

        context['Donations'] = 0
        for donations in Donations.objects.filter(
                booked_on__gte=start_date,
                booked_on__lte=end_date):
            context['Donations'] += int(donations.amount)

        context['Expenses'] = 0
        for expenses in Expenses.objects.filter(
                booked_on__gte=start_date,
                booked_on__lte=end_date):
            context['Expenses'] += int(expenses.amount)

        for booking in Booking.objects.filter(
                booked_on__gte=start_date,
                booked_on__lte=end_date,
                status = "Booked"):
            try:
                room_id = str(booking.room)
                print("room " + room_id)
                room_info = Rooms.objects.get(room_id=room_id)
                if room_info.room_type in context:
                    context[room_info.room_type] += room_info.price
                    total += room_info.price
                else:
                    context[room_info.room_type] = room_info.price
                    total += room_info.price
            except:
                print(booking.room + " not found")

        total += context['Ambulance'] + context['Donations'] - context['Expenses']
        print(context)
    return {'data': context, 'total': total, 'form' : form,
            'start_date' : start_date, 'end_date' : end_date}

def reports_view(request):
    context = {}
    total = 0
    context = __get_booking_details(request)
    return render(request, 'reports_view.html', {'data': context['data'],
                                                 'total': context['total'],
                                                 'form' : context['form']})

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


def view_pdf(request):
    print("In view_pdf")
    data = __get_booking_details(request)
    pdf = render_to_pdf('pdf_template.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def expenses_add(request):
    if request.method == "POST":
        print ("In the if")
        form = ExpenseAddForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return render(request, 'expense_add_success.html', {'booking': booking})
        else:
            print("Invalid form data")
            print(form.errors)
            return redirect('index')
        print("coming here")
    form = ExpenseAddForm()
    return render(request, 'expense_add.html', {'form':form})

def view_expense_receipt(request, booking_id):
    expenses_info = Expenses.objects.filter(pk = booking_id)
    pdf = render_to_pdf('expenses_receipt_pdf.html', {'booking': expenses_info})
    return HttpResponse(pdf, content_type='application/pdf')

def view_tomorrow_pdf(request):
    tomo = datetime.datetime.today() + datetime.timedelta(days=1)
    booking_info = Booking.objects.filter(start__lte = tomo, end__gte = tomo,
                                          status = "Booked")
    print(booking_info)
    pdf = render_to_pdf('tomorrow_events_pdf.html', {'booking': booking_info,
                                                     'tomo': tomo})
    return HttpResponse(pdf, content_type='application/pdf')

def detailed_view(request):
    print("Here")
    form = ReportForm()
    return render(request, 'detailed_report.html', {'form': form})

def view_detailed_pdf(request):
    if request.GET.get('start_year') is not None:
        start_date = datetime.datetime(int(request.GET.get('start_year')),
                                               int(request.GET.get('start_month')),
                                               int(request.GET.get('start_day')))
    else:
        start_date = datetime.datetime.today()

    if request.GET.get('end_year') is not None:
        end_date = datetime.datetime(int(request.GET.get('end_year')),
                                         int(request.GET.get('end_month')),
                                         int(request.GET.get('end_day')))
    else:
        end_date = datetime.datetime.today()

    booking_info = Booking.objects.filter(booked_on__gte=start_date,
                                          booked_on__lte=end_date)
    room_prices=[]
    for b in booking_info:
        room = Rooms.objects.filter(room_id = b.room)
        for r in room:
            delta = (b.end - b.start)
            if delta.days == 0:
                price = 1 * r.price
            else:
                price = delta.days * r.price
            room_prices.append(price)

    ambulance_info = Ambulance.objects.filter(booked_on__gte=start_date,
                                              booked_on__lte=end_date)
    donation_info = Donations.objects.filter(booked_on__gte=start_date,
                                             booked_on__lte=end_date)
    expenses_info = Expenses.objects.filter(booked_on__gte=start_date,
                                            booked_on__lte=end_date)

    pdf = render_to_pdf('detailed_report_pdf.html', {'booking': booking_info,
                                                     'room_prices': room_prices,
                                                     'ambulance' : ambulance_info,
                                                     'donations' : donation_info,
                                                     'expenses' : expenses_info,
                                                     'start_date' : start_date,
                                                     'end_date' : end_date})
    return HttpResponse(pdf, content_type='application/pdf')

def today_booking(request):
    booking_info = Booking.objects.filter(booked_on = datetime.datetime.today(),
                                          status = 'Booked')
    return render(request, 'booking_view.html', {'bookings' : booking_info})

def booking_cancel(request, booking_id):
    Booking.objects.filter(pk = booking_id).update(status="Cancelled")
    return render(request, 'booking_cancel.html')


