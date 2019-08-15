from .views import RunViewSet
from rest_framework.routers import SimpleRouter

app_name = 'runs'

router = SimpleRouter()
router.register(r'runs', RunViewSet, basename='run')

urlpatterns = router.urls
