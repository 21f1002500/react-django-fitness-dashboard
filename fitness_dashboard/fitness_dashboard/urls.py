"""
URL configuration for fitness_dashboard project.

The `urlpatterns` list routes URLs to views. 

"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import ClientViewSet, CoachViewSet, UserViewSet
from core.views import AppConfigurationViewSet, AnalyticsViewSet, CoachModuleAccessViewSet, ModuleViewSet
from diet.views import DietPlanViewSet
from fitness.views import FitnessPlanViewSet
from subscription.views import SubscriptionViewSet
from tracker.views import TrackerViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'coaches', CoachViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'coach-module-access', CoachModuleAccessViewSet)
router.register(r'app-configurations', AppConfigurationViewSet)
router.register(r'analytics', AnalyticsViewSet)
router.register(r'diet-plans', DietPlanViewSet)
router.register(r'fitness-plans', FitnessPlanViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'tracker-records', TrackerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
]


