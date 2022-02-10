"""dm_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views as views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/shared/', include('shared_models.api.urls')),
    path('api/tracking/', include('tracking.api.urls')),
]

# Add application APIs
if settings.INSTALLED_APPS.count("ppt"):
    urlpatterns.append(
        path('api/', include('ppt.api.urls')),
    )
if settings.INSTALLED_APPS.count("travel"):
    urlpatterns.append(
        path('api/', include('travel.api.urls')),
    )
if settings.INSTALLED_APPS.count("csas2"):
    urlpatterns.append(
        path('api/', include('csas2.api.urls')),
    )
if settings.INSTALLED_APPS.count("res"):
    urlpatterns.append(
        path('api/', include('res.api.urls')),
    )
if settings.INSTALLED_APPS.count("scuba"):
    urlpatterns.append(
        path('api/', include('scuba.api.urls')),
    )
if settings.INSTALLED_APPS.count("trapnet"):
    urlpatterns.append(
        path('api/', include('trapnet.api.urls')),
    )
if settings.INSTALLED_APPS.count("edna"):
    urlpatterns.append(
        path('api/', include('edna.api.urls')),
    )
if settings.INSTALLED_APPS.count("grais"):
    urlpatterns.append(
        path('api/', include('grais.api.urls')),
    )
if settings.INSTALLED_APPS.count("bio_diversity"):
    urlpatterns.append(
        path('api/', include('bio_diversity.api.urls')),
    )
if settings.INSTALLED_APPS.count("publications"):
    urlpatterns.append(
        path('api/', include('publications.api.urls')),
    )
if settings.INSTALLED_APPS.count("ihub"):
    urlpatterns.append(
        path('api/', include('ihub.api.urls')),
    )

urlpatterns += i18n_patterns(
    path('', views.IndexView.as_view(), name="index"),
    path('accounts/', include('accounts.urls')),
    path('shared/', include('shared_models.urls')),
    path('tracking/', include('tracking.urls')),
    prefix_default_language=True)

if settings.INSTALLED_APPS.count("inventory"):
    urlpatterns += i18n_patterns(path('inventory/', include('inventory.urls')), prefix_default_language=True)
else:
    print("not connecting inventory app")

if settings.INSTALLED_APPS.count("tickets"):
    urlpatterns += i18n_patterns(path('dm-tickets/', include('tickets.urls')), prefix_default_language=True)
else:
    print("not connecting ticket app")

if settings.INSTALLED_APPS.count("cruises"):
    urlpatterns += i18n_patterns(path('cruises/', include('cruises.urls')), prefix_default_language=True)
else:
    print("not connecting cruises app")

if settings.INSTALLED_APPS.count("grais"):
    urlpatterns += i18n_patterns(path('grais/', include('grais.urls')), prefix_default_language=True)
else:
    print("not connecting grais app")

if settings.INSTALLED_APPS.count("herring"):
    urlpatterns += i18n_patterns(path('herman/', include('herring.urls')), prefix_default_language=True)
else:
    print("not connecting herman app")

if settings.INSTALLED_APPS.count("camp"):
    urlpatterns += i18n_patterns(path('camp/', include('camp.urls')), prefix_default_language=True)
else:
    print("not connecting camp app")

if settings.INSTALLED_APPS.count("scuba"):
    urlpatterns += i18n_patterns(path('scuba/', include('scuba.urls')), prefix_default_language=True)
else:
    print("not connecting Scuba app")

if settings.INSTALLED_APPS.count("edna"):
    urlpatterns += i18n_patterns(path('edna/', include('edna.urls')), prefix_default_language=True)
else:
    print("not connecting eDNA app")

if settings.INSTALLED_APPS.count("diets"):
    urlpatterns += i18n_patterns(path('diets/', include('diets.urls')), prefix_default_language=True)
else:
    print("not connecting diets app")

if settings.INSTALLED_APPS.count("ppt"):
    urlpatterns += i18n_patterns(path('ppt/', include('ppt.urls')), prefix_default_language=True)
else:
    print("not connecting ppt app")

if settings.INSTALLED_APPS.count("ihub"):
    urlpatterns += i18n_patterns(path('ihub/', include('ihub.urls')), prefix_default_language=True)
else:
    print("not connecting ihub app")

if settings.INSTALLED_APPS.count("shares"):
    urlpatterns += i18n_patterns(path('gulf-shares/', include('shares.urls')), prefix_default_language=True)
else:
    print("not connecting shares app")

if settings.INSTALLED_APPS.count("travel") and not settings.FAKE_TRAVEL_APP:
    urlpatterns += i18n_patterns(path('travel-plans/', include('travel.urls')), prefix_default_language=True)
else:
    print("not connecting travel app")

if settings.INSTALLED_APPS.count("ios2"):
    urlpatterns += i18n_patterns(path('ios2/', include('ios2.urls')), prefix_default_language=True)
else:
    print("not connecting ios2")

if settings.INSTALLED_APPS.count("spot"):
    urlpatterns += i18n_patterns(path('grants-and-contributions/', include('spot.urls')), prefix_default_language=True)
else:
    print("not connecting spot")

if settings.INSTALLED_APPS.count("publications"):
    urlpatterns += i18n_patterns(path('publications/', include('publications.urls')), prefix_default_language=True)
else:
    print("not connecting publications app")

if settings.INSTALLED_APPS.count("staff"):
    urlpatterns += i18n_patterns(path('staff/', include('staff.urls')), prefix_default_language=True)
else:
    print("not connecting staff app")

if settings.INSTALLED_APPS.count("whalesdb"):
    urlpatterns += i18n_patterns(path('whalesdb/', include('whalesdb.urls')), prefix_default_language=True)
else:
    print("not connecting whalesdb app")

if settings.INSTALLED_APPS.count("trapnet"):
    urlpatterns += i18n_patterns(path('trapnet/', include('trapnet.urls')), prefix_default_language=True)
else:
    print("not connecting TrapNet")

if settings.INSTALLED_APPS.count("sar_search"):
    urlpatterns += i18n_patterns(path('sar-search/', include('sar_search.urls')), prefix_default_language=True)
else:
    print("not connecting SAR Search")

if settings.INSTALLED_APPS.count("vault"):
    urlpatterns += i18n_patterns(path('vault/', include('vault.urls')), prefix_default_language=True)
else:
    print("not connecting vault app")

if settings.INSTALLED_APPS.count("whalebrary"):
    urlpatterns += i18n_patterns(path('whalebrary/', include('whalebrary.urls')), prefix_default_language=True)
else:
    print("not connecting whalebrary app")

if settings.INSTALLED_APPS.count("spring_cleanup"):
    urlpatterns += i18n_patterns(path('spring-cleanup/', include('spring_cleanup.urls')), prefix_default_language=True)
else:
    print("not connecting spring_cleanup app")

if settings.INSTALLED_APPS.count("shiny"):
    urlpatterns += i18n_patterns(path('shiny-apps/', include('shiny.urls')), prefix_default_language=True)
else:
    print("not connecting shiny app repo")

if settings.INSTALLED_APPS.count("csas2"):
    urlpatterns += i18n_patterns(path('csas-sccs/', include('csas2.urls')), prefix_default_language=True)
else:
    print("not connecting csas2 app")

if settings.INSTALLED_APPS.count("bio_diversity"):
    urlpatterns += i18n_patterns(path('bio_diversity/', include('bio_diversity.urls')), prefix_default_language=True)
else:
    print("not connecting bio_diversity app")

if settings.INSTALLED_APPS.count("maret"):
    urlpatterns += i18n_patterns(path('maret/', include('maret.urls')), prefix_default_language=True)
else:
    print("not connecting maret app")

if settings.INSTALLED_APPS.count("fisheriescape"):
    urlpatterns += i18n_patterns(path('fisheriescape/', include('fisheriescape.urls')),
                                 prefix_default_language=True)
else:
    print("not connecting fisheriescape app")

if settings.INSTALLED_APPS.count("res"):
    urlpatterns += i18n_patterns(path('res-sub/', include('res.urls')),
                                 prefix_default_language=True)
else:
    print("not connecting res app")

if settings.INSTALLED_APPS.count("lengths"):
    urlpatterns += i18n_patterns(path('lengths/', include('lengths.urls')),
                                 prefix_default_language=True)
else:
    print("not connecting res app")

if settings.AZURE_STORAGE_ACCOUNT_NAME == "":
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                            document_root=settings.MEDIA_ROOT)
# print(urlpatterns)
