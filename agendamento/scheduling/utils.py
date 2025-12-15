from datetime import time, timedelta, datetime

def gerar_horarios(inicio, fim, duracao):
    horarios = []
    atual = datetime.combine(datetime.today(), inicio)

    fim = datetime.combine(datetime.today(), fim)

    while atual + timedelta(minutes=duracao) <= fim:
        horarios.append(atual.time())
        atual += timedelta(minutes=duracao)

    return horarios
