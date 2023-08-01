from django import forms
from .models import Hashtag, Picture
from multiupload.fields import MultiFileField

class PictureForm(forms.ModelForm):
    """Form to upload multiple images using django-multiupload library,
      this will load the pictures that the user wish, with a limit of 10"""
    multi_pictures = MultiFileField( 
        max_num=10, 
        label="",
    )

    class Meta:
        model = Picture
        fields = ['multi_pictures']

class HashtagForm(forms.Form):
    hashtag = forms.ModelChoiceField(
        queryset=Hashtag.objects.all().order_by('hashtag'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='All',
        initial = 'All',
        required=False, 
        label='Tags: ', 
        )
    

class PictureDataForm(forms.ModelForm):
    """Fill or edit data of uploaded pictures """
    class Meta:
        model = Picture
        exclude = ['image', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'uploaded_at': forms.DateInput(attrs={'class': 'form-control'}),
            'hashtags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, *args, **kwargs):
        super(PictureDataForm, self).__init__(*args, **kwargs)
        self.fields['hashtags'].queryset = Hashtag.objects.all().order_by('hashtag')
