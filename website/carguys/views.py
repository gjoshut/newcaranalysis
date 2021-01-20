from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from .models import Postsales, Presale
from .scripts import presale_list_grabber,regression_dictionary_maker, to_database_presale, add_new_to_database, database_update, to_database_postsale
from pandas.io.parsers import ParserError
import numpy as np



def home(request):
    if not Postsales.objects.all():
        data = database_update()
        to_database_postsale(data)
    else:
        add_new_to_database(Postsales)
    return render(request, 'carguys/base.html')

def presale_set_up(request):
    #render(request, 'carguys/presale_set_up.html')
    # presale_list = price_estimator()
    # to_database_presale(presale_list)
    presale_list_grabber()
    return HttpResponseRedirect(reverse('presale_choice'))

def presale_choice(request):
    car_models = Presale.objects.order_by().values('Model').distinct().all()
    context = {'car_models':car_models}
    return render(request, 'carguys/presale_choice.html', context)


def presale_analysis(request):
    selected_model = Presale.objects.filter(Model = request.POST['selected_car']).all()
    regression_dictionary = regression_dictionary_maker()
    list_of_results = [int(np.round(regression_dictionary[car.Model].predict([[car.Year, car.Odometer]]), 2)**2) for car in selected_model]
    # equation = regression_dictionary[selected_model]
    #context = {'equation':equation}
    return render(request, 'carguys/presale_analysis.html', {'selected_model': selected_model, 'list_of_results': list_of_results})

    # # Create your views here.
