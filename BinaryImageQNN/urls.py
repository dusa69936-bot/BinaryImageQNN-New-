"""
BinaryImageQNN URL Configuration
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# IMPORT VIEWS
from BinaryImageQNN import views as mainView
from users import views as userViews


urlpatterns = [

    # =========================
    # DJANGO ADMIN PANEL
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # MAIN PAGES
    # =========================
    path('', mainView.index, name="index"),
    path('AdminLogin/', mainView.AdminLogin, name="AdminLogin"),
    path('UserLogin/', mainView.UserLogin, name="UserLogin"),
    path('UserRegister/', mainView.UserRegister, name="UserRegister"),

    # =========================
    # ADMIN MODULE
    # =========================
    path('AdminLoginCheck/', mainView.AdminLoginCheck, name="AdminLoginCheck"),
    path('AdminHome/', mainView.AdminHome, name="AdminHome"),
    path('AdminLogout/', mainView.AdminLogout, name="AdminLogout"),

    # =========================
    # USER AUTH
    # =========================
    path('UserRegisterActions/', userViews.UserRegisterActions, name="UserRegisterActions"),
    path('UserLoginCheck/', userViews.UserLoginCheck, name="UserLoginCheck"),
    path('UserLogout/', userViews.UserLogout, name="UserLogout"),

    # =========================
    # USER PAGES
    # =========================
    path('UserHome/', userViews.UserHome, name="UserHome"),
    path('UserViewDataset/', userViews.UserViewDataset, name="UserViewDataset"),
    path('eda_analysis/', userViews.eda_analysis, name="eda_analysis"),
    path('QNNAccuracy/', userViews.QNNAccuracy, name="QNNAccuracy"),
    path('UserTestCanvasMNIST/', userViews.UserTestCanvasMNIST, name="UserTestCanvasMNIST"),
    path('UserRealWorldExample/', userViews.UserRealWorldExample, name="UserRealWorldExample"),

    # =========================
    # QNN / MNIST
    # =========================
    path('MnistTorchQNN/', userViews.MnistTorchQNN, name="MnistTorchQNN"),

    # =========================
    # 🔥 NEW ADMIN USER MANAGEMENT
    # =========================
    path('ViewUsers/', userViews.ViewUsers, name='view_users'),
    path('activate_user/<int:id>/', userViews.ActivateUser, name='activate_user'),
    path('delete_user/<int:id>/', userViews.DeleteUser, name='delete_user'),
]


# =========================
# STATIC + MEDIA
# =========================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / 'assets' / 'static'
    )