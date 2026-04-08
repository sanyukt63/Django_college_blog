from django import forms
from .models import Comment


# Forms for email sharing and comment submission with Bootstrap styling.

# Form for sharing post via email.
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField(required=False)
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


# ModelForm for comments, auto-linked to post in view.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        # Bootstrap classes for form styling.
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False, empty_value='',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

