from django.shortcuts import render, redirect
from datetime import time
from urllib.parse import quote

from .models import (
    Servico,
    Profissional,
    Agendamento,
    Configuracao
)
from .utils import gerar_horarios


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

        todos_horarios = gerar_horarios(
            inicio, fim, servico.duracao
        )

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
        agendamento = Agendamento.objects.create(
            servico_id=request.POST['servico'],
            profissional_id=request.POST.get('profissional') or None,
            nome_cliente=request.POST['nome'],
            telefone=request.POST['telefone'],
            data=request.POST['data'],
            hora=request.POST['hora'],
        )

        # ✅ SALVA NA SESSÃO
        request.session['agendamento_id'] = agendamento.id

        return redirect('sucesso')

    return render(request, 'agendar.html', {
        'servicos': servicos,
        'profissionais': profissionais,
        'horarios': horarios_disponiveis
    })


def sucesso(request):
    agendamento_id = request.session.get('agendamento_id')

    if not agendamento_id:
        return render(request, 'sucesso.html')

    agendamento = Agendamento.objects.get(id=agendamento_id)
    config = Configuracao.objects.first()

    whatsapp_link = None

    if config and config.whatsapp:
        mensagem_base = config.mensagem_whatsapp

        mensagem = mensagem_base.format(
            nome=agendamento.nome_cliente,
            servico=agendamento.servico.nome,
            data=agendamento.data.strftime('%d/%m/%Y'),
            hora=agendamento.hora.strftime('%H:%M'),
        )

        whatsapp_link = (
            f"https://wa.me/{config.whatsapp}"
            f"?text={quote(mensagem)}"
        )

    return render(request, 'sucesso.html', {
        'whatsapp_link': whatsapp_link
    })
