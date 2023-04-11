from dataclasses import field, fields
from pyexpat import model
from django.forms import ModelForm
from django import forms
from .models import Bid, Category, Listing, Comment

class NewListingForm(ModelForm):
    
    class Meta:
        model = Listing
        
        fields = ('name', 'description', 'starting_price', 'image', 'category')
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Rainbow Striped Cotton Coat'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Describe this item'}),
            'starting_price' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your bidding price'}),
            'image' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Attach image URL'}),
            # 'category' : forms.ModelChoiceField(queryset=Category.objects.all() ),
        }

class NewCommentForm(ModelForm):

    class Meta:
        model = Comment

        fields = {'comment', }
        widgets = {
            'comment' : forms.Textarea(attrs={'rows': 5, 'class' : "form-control", 'placeholder': 'Write your comment'}),

        }


class NewBidForm(ModelForm):
    class Meta:
        model = Bid

        fields = {'bid'}

        widgets = {
            'bid' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter your bid', 'min':20})
        }