from django.urls import include, path
from rest_framework.routers import DefaultRouter
from groceries.api.views import GreengrocerViewSet, PostViewSet, LogoutVieSet

router = DefaultRouter()
router.register(r"nearby", GreengrocerViewSet)
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("logout/", LogoutVieSet.as_view()),
    path("", include(router.urls)),
]