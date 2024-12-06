from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clientes.views import ClienteViewSet
from transacoes.views import TransacaoViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'transacoes', TransacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
