from .models import Configuracao

def configuracao(request):
    return {
        'config': Configuracao.objects.first()
    }
