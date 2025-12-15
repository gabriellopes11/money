from django.shortcuts import render, redirect
from .models import Servico, Profissional, Agendamento
from datetime import time
from .utils import gerar_horarios
from .models import Servico, Profissional, Agendamento

def agendar(request):
    servicos = Servico.objects.all()
    profissionais = Profissional.objects.all()
    horarios_disponiveis = []

    if request.method == 'POST' and 'buscar' in request.POST:
        servico = Servico.objects.get(id=request.POST['servico'])
        data = request.POST['data']
        profissional_id = request.POST.get('profissional')

        inicio = time(9, 0)
        fim = time(18, 0)

        todos_horarios = gerar_horarios(inicio, fim, servico.duracao)

        agendamentos = Agendamento.objects.filter(
            data=data,
            status__in=['pendente', 'confirmado']
        )

        if profissional_id:
            agendamentos = agendamentos.filter(
                profissional_id=profissional_id
            )

        ocupados = [a.hora for a in agendamentos]

        horarios_disponiveis = [
            h for h in todos_horarios if h not in ocupados
        ]

    if request.method == 'POST' and 'agendar' in request.POST:
        Agendamento.objects.create(
            servico_id=request.POST['servico'],
            profissional_id=request.POST.get('profissional') or None,
            nome_cliente=request.POST['nome'],
            telefone=request.POST['telefone'],
            data=request.POST['data'],
            hora=request.POST['hora'],
        )
        return redirect('sucesso')

    return render(request, 'agendar.html', {
        'servicos': servicos,
        'profissionais': profissionais,
        'horarios': horarios_disponiveis
    })



def sucesso(request):
    return render(request, 'sucesso.html')
