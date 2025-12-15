from django.shortcuts import render, redirect
from .models import Servico, Profissional, Agendamento

def agendar(request):
    servicos = Servico.objects.all()
    profissionais = Profissional.objects.all()

    if request.method == 'POST':
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
        'profissionais': profissionais
    })


def sucesso(request):
    return render(request, 'sucesso.html')
