from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    name.widget.attrs['class'] = 'form-control'
    email.widget.attrs['class'] = 'form-control'
    message.widget.attrs['class'] = 'form-control'
