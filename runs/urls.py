from .views import RunViewSet, GearViewSet
from rest_framework.routers import SimpleRouter

app_name = 'runs'

router = SimpleRouter()
router.register(r'runs', RunViewSet, basename='run')
router.register(r'gear', GearViewSet, basename='gear')

urlpatterns = router.urls
