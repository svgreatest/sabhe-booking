from django import forms
from .models import Rooms, Booking, Donations, Ambulance, Expenses
import datetime

class RoomsAddForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'

class BookingAddForm(forms.ModelForm):
    readonly_fields = ('start', 'end', 'room')
    def __init__(self, *args, **kwargs):
        super(BookingAddForm, self).__init__(*args, **kwargs)
        for field in self.readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
    class Meta:
        model = Booking
        exclude = ['status']


class DonationsAddForm(forms.ModelForm):
    class Meta:
        model = Donations
        fields = '__all__'

class AmbulanceAddForm(forms.ModelForm):
    class Meta:
        model = Ambulance
        fields = '__all__'

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start', 'end']
        widgets = {
            'start' : forms.SelectDateWidget(),
            'end'   : forms.SelectDateWidget()
        }

class ReportForm(forms.Form):
    start = forms.DateField(widget = forms.SelectDateWidget())
    end   = forms.DateField(widget = forms.SelectDateWidget())

class ExpenseAddForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'
# ''' Get this to work correctly '''
#     def clean(self):
#         print("calling clean")
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get("start")
#         end_date = cleaned_data.get("end")
#         if end_date < start_date:
#             print("Entered condition")
#             raise forms.ValidationError("End date should be greater than start date.")
