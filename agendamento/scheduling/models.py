from django.db import models


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    duracao = models.PositiveIntegerField(
        help_text="Duração em minutos"
    )
    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return self.nome


class Profissional(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE
    )
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    nome_cliente = models.CharField(
        max_length=100
    )
    telefone = models.CharField(
        max_length=20
    )
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.nome_cliente} - {self.data.strftime('%d/%m/%Y')} {self.hora.strftime('%H:%M')}"


class Configuracao(models.Model):
    nome_negocio = models.CharField(
        max_length=100,
        default="Sistema de Agendamento"
    )

    whatsapp = models.CharField(
        max_length=20,
        help_text="Formato: 55DDDNUMERO (ex: 5511999999999)"
    )

    mensagem_whatsapp = models.TextField(
        default=(
            "Olá {nome}, gostaria de confirmar meu agendamento:\n"
            "Serviço: {servico}\n"
            "Data: {data}\n"
            "Horário: {hora}"
        ),
        help_text=(
            "Use as variáveis: {nome}, {servico}, {data}, {hora}"
        )
    )

    def __str__(self):
        return "Configuração do Sistema"


    nome_negocio = models.CharField(
        max_length=100,
        default="Sistema de Agendamento"
    )
    whatsapp = models.CharField(
        max_length=20,
        help_text="Formato: 55DDDNUMERO (ex: 5511999999999)"
    )

    def __str__(self):
        return "Configuração do Sistema"
