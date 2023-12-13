
from django import forms

class PostcardForm(forms.Form):
    paragraph = forms.CharField(widget=forms.Textarea)

class ChristmasForm(forms.Form):
    num_people = forms.IntegerField(label='Number of People', min_value=1)

    def __init__(self, *args, **kwargs):
        super(ChristmasForm, self).__init__(*args, **kwargs)
        for i in range(self.initial.get('num_people', 1)):
            self.fields[f'receiver_name_{i+1}'] = forms.CharField(label=f'Receiver\'s Name {i+1}', max_length=100)
            self.fields[f'email_{i+1}'] = forms.EmailField(label=f'Email {i+1}')