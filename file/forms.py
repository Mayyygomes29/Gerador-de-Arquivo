from django import forms

class FileForms(forms.Form):
    file = forms.FileField(allow_empty_file=False, label= "Selecione um arquivo" ,help_text="Envie um arquivo .json, .csv ou .xml")


    