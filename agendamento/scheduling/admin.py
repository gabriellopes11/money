from django.contrib import admin
from .models import (
    Servico,
    Profissional,
    Agendamento,
    Configuracao,
    HorarioFuncionamento
)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao', 'preco')
    search_fields = ('nome',)


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        'nome_cliente',
        'servico',
        'profissional',
        'data',
        'hora',
        'status'
    )
    list_filter = ('status', 'data', 'profissional')
    search_fields = ('nome_cliente', 'telefone')


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('whatsapp',)


@admin.register(HorarioFuncionamento)
class HorarioFuncionamentoAdmin(admin.ModelAdmin):
    list_display = (
        'get_dia_semana',
        'abertura',
        'fechamento',
        'intervalo_inicio',
        'intervalo_fim',
        'ativo'
    )
    list_filter = ('ativo',)

    def get_dia_semana(self, obj):
        return obj.get_dia_semana_display()

    get_dia_semana.short_description = 'Dia da Semana'
