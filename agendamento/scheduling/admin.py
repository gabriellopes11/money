from django.contrib import admin
from .models import Servico, Profissional, Agendamento, Configuracao

@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('nome_negocio', 'whatsapp')

    def has_add_permission(self, request):
        return not Configuracao.objects.exists()

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao', 'preco')


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        'nome_cliente',
        'servico',
        'data',
        'hora',
        'status'
    )
    list_filter = ('status', 'data')
