from django.contrib import admin
from .models import (
    Servico,
    Profissional,
    Agendamento,
    Configuracao,
    HorarioFuncionamento,
    HorarioProfissional
)


# 🔹 SERVIÇOS
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao', 'preco')
    search_fields = ('nome',)


# 🔹 PROFISSIONAIS
@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


# 🔹 AGENDAMENTOS
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


# 🔹 CONFIGURAÇÃO DO SISTEMA
@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('nome_negocio', 'whatsapp')


# 🔹 HORÁRIO GLOBAL (fallback)
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
    list_filter = ('dia_semana', 'ativo')
    ordering = ('dia_semana',)

    def get_dia_semana(self, obj):
        return obj.get_dia_semana_display()

    get_dia_semana.short_description = 'Dia da Semana'


# 🔥 HORÁRIO POR PROFISSIONAL
@admin.register(HorarioProfissional)
class HorarioProfissionalAdmin(admin.ModelAdmin):
    list_display = (
        'profissional',
        'get_dia_semana',
        'abertura',
        'fechamento',
        'ativo'
    )
    list_filter = ('profissional', 'dia_semana', 'ativo')
    ordering = ('profissional', 'dia_semana')

    def get_dia_semana(self, obj):
        return obj.get_dia_semana_display()

    get_dia_semana.short_description = 'Dia da Semana'
