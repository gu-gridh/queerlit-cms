from django.urls import path
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def matomo_dashboard(request):
    return render(request, "matomo/dashboard.html", {})


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [path("matomo/", matomo_dashboard, name="matomo_dashboard")]


@hooks.register("construct_main_menu")
def add_matomo_item(request, menu_items):
    menu_items.append(MenuItem("Matomo", "/admin/matomo/", icon_name="site"))