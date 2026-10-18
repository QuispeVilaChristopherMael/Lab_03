from django.shortcuts import render, get_object_or_404
from .models import Opcion, Pregunta


# Create your views here.
def index(request):
    latest_question_list = Pregunta.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'encuesta/index.html', context)


def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    context = {
        'pregunta': pregunta
    }
    return render(request, 'encuesta/detalle.html', context)


def votar(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        opcionSeleccionada = pregunta.opcion_set.get(pk=request.POST['opcion'])
        opcionSeleccionada.votos += 1
        opcionSeleccionada.save()
    except (KeyError, Opcion.DoesNotExist):
        return render(request, 'encuesta/detalle.html', {
            'pregunta': pregunta,
            'error_message': "No seleccionaste ninguna opción.",
        })
    context = {
        'pregunta': pregunta
    }
    return render(request, 'encuesta/resultados.html', context)
