from django import forms

class BookForm(forms.Form):
    book_name = forms.CharField(widget=forms.TextInput(
        attrs={"class":"form-control",
        "placeholder":"Start typing here your favorite book...",
        "id":"book-search"} ))