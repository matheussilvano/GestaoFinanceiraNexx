from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView
from clientes.views import ClienteViewSet
from transacoes.views import TransacaoViewSet
from relatorios.views import RelatorioViewSet

# Configuração do Swagger/OpenAPI
schema_view = get_schema_view(
   openapi.Info(
      title="API de Gestão Financeira",
      default_version='v1',
      description="Sistema de gestão de transações financeiras",
   ),
   public=True,
)

# Configuração do Router
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'transacoes', TransacaoViewSet)
router.register(r'relatorios', RelatorioViewSet, basename='relatorio')

urlpatterns = [
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title='API de Gestão Financeira')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]