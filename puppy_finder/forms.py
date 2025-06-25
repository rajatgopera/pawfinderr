from django import forms
from .models import Puppy, Message, CustomUser, Reunion
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class LostPuppyForm(forms.ModelForm):
    class Meta:
        model = Puppy
        fields = [
            'name', 'breed', 'color', 'age', 'size', 'gender',
            'last_seen_location', 'last_seen_date', 'description',
            'image', 'model_3d', 'model_texture'
        ]
        widgets = {
            'last_seen_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('breed', css_class='col-md-6'),
            ),
            Row(
                Column('color', css_class='col-md-4'),
                Column('age', css_class='col-md-4'),
                Column('size', css_class='col-md-4'),
            ),
            'gender',
            'last_seen_location',
            Row(
                Column('last_seen_date', css_class='col-md-6'),
                Column('image', css_class='col-md-6'),
            ),
            'description',
            Row(
                Column('model_3d', css_class='col-md-6'),
                Column('model_texture', css_class='col-md-6'),
            ),
            Submit('submit', 'Submit Lost Report', css_class='btn-primary')
        )

class FoundPuppyForm(forms.ModelForm):
    class Meta:
        model = Puppy
        fields = [
            'breed', 'color', 'age', 'size', 'gender',
            'last_seen_location', 'last_seen_date', 'description',
            'image', 'model_3d', 'model_texture'
        ]
        widgets = {
            'last_seen_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('breed', css_class='col-md-6'),
                Column('color', css_class='col-md-6'),
            ),
            Row(
                Column('age', css_class='col-md-4'),
                Column('size', css_class='col-md-4'),
                Column('gender', css_class='col-md-4'),
            ),
            'last_seen_location',
            Row(
                Column('last_seen_date', css_class='col-md-6'),
                Column('image', css_class='col-md-6'),
            ),
            'description',
            Row(
                Column('model_3d', css_class='col-md-6'),
                Column('model_texture', css_class='col-md-6'),
            ),
            Submit('submit', 'Submit Found Report', css_class='btn-primary')
        )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'email',
            'phone_number',
            'address',
            'profile_picture',
            Submit('submit', 'Update Profile', css_class='btn-primary')
        )

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Send Message', css_class='btn-primary'))

class SearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Search')
    breed = forms.CharField(required=False)
    color = forms.CharField(required=False)
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + Puppy.STATUS_CHOICES,
        label='Status'
    )
    location = forms.CharField(required=False, label='Location')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('search_query', css_class='col-md-6'),
                Column('location', css_class='col-md-6'),
            ),
            Row(
                Column('breed', css_class='col-md-3'),
                Column('color', css_class='col-md-3'),
                Column('status', css_class='col-md-3'),
                Column(Submit('submit', 'Search', css_class='btn-primary'), css_class='col-md-3 d-flex align-items-end'),
            )
        )

class ReunionForm(forms.ModelForm):
    class Meta:
        model = Reunion
        fields = ['finder', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['finder'].queryset = CustomUser.objects.none()
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Mark as Reunited', css_class='btn-success'))