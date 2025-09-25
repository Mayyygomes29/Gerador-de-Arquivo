from io import BytesIO

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
import matplotlib.pyplot as plt

from .forms import FileForms

plt.close('all')

def error(request):
    """ Retorna um template de erro caso o usuário passar um arquivo que não aceite """

    return render(request, 'error.html', {'error':'Não é aceito esse tipo de arquivo'})


def reading_file(request):
    ''' 
        Pega o arquivo(.json, .txt, .csv, .xml) passado pelo cliente e retonar um arquivo .xlsx 
    '''
    if request.method == "POST":
        form = FileForms(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']  
            ext = uploaded_file.name.split('.')[-1].lower()

            if ext == "json":
                df = pd.read_json(uploaded_file)
            elif ext == "csv":
                df = pd.read_csv(uploaded_file)
            elif ext == "xml":
                df = pd.read_xml(uploaded_file)
            else:
                return redirect('error')
            
            data = pd.DataFrame(df)
            path = BytesIO()
            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                data.to_excel(writer, sheet_name="sheet1", index=False)
                
            path.seek(0)
            response = HttpResponse(path, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") 
            response["Content-Disposition"] = 'attachment; filename="saida.xlsx"'
            return response

    else:
        form = FileForms()
    return render(request, "file.html", {"form": form})



