from datetime import datetime, timedelta


def gerar_horarios(inicio, fim, duracao):
    """
    Gera uma lista de horários entre inicio e fim
    com intervalo baseado na duração do serviço.
    """
    horarios = []

    atual = datetime.combine(datetime.today(), inicio)
    limite = datetime.combine(datetime.today(), fim)

    while atual + timedelta(minutes=duracao) <= limite:
        horarios.append(atual.time())
        atual += timedelta(minutes=duracao)

    return horarios


def filtrar_por_funcionamento(data, horarios, profissional=None):
    """
    Filtra horários com base:
    1️⃣ no horário do profissional (se existir)
    2️⃣ no horário global (fallback)
    """
    from .models import HorarioFuncionamento, HorarioProfissional

    dia_semana = data.weekday()  # 0 = segunda-feira

    funcionamento = None

    # 🔥 1. Tenta buscar horário do profissional
    if profissional:
        funcionamento = HorarioProfissional.objects.filter(
            profissional=profissional,
            dia_semana=dia_semana,
            ativo=True
        ).first()

    # 🔁 2. Fallback: horário global
    if not funcionamento:
        funcionamento = HorarioFuncionamento.objects.filter(
            dia_semana=dia_semana,
            ativo=True
        ).first()

    # ❌ Nenhum horário configurado
    if not funcionamento:
        return []

    horarios_filtrados = []

    for h in horarios:
        if funcionamento.abertura <= h < funcionamento.fechamento:

            # ⛔ Intervalo (almoço / pausa)
            if (
                funcionamento.intervalo_inicio
                and funcionamento.intervalo_fim
                and funcionamento.intervalo_inicio <= h < funcionamento.intervalo_fim
            ):
                continue

            horarios_filtrados.append(h)

    return horarios_filtrados
