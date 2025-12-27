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


def filtrar_por_funcionamento(data, horarios):
    """
    Filtra horários com base no horário de funcionamento
    configurado no sistema.
    """
    from .models import HorarioFuncionamento

    dia_semana = data.weekday()  # 0 = segunda

    try:
        funcionamento = HorarioFuncionamento.objects.get(
            dia_semana=dia_semana
        )
    except HorarioFuncionamento.DoesNotExist:
        return []

    if not funcionamento.ativo:
        return []

    horarios_filtrados = []

    for h in horarios:
        if funcionamento.abertura <= h < funcionamento.fechamento:

            # Intervalo (almoço, pausa, etc)
            if (
                funcionamento.intervalo_inicio
                and funcionamento.intervalo_fim
                and funcionamento.intervalo_inicio <= h < funcionamento.intervalo_fim
            ):
                continue

            horarios_filtrados.append(h)

    return horarios_filtrados
