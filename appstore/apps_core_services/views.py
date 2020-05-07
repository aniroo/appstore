import json
import logging
from apps_core_services.get_pods import get_pods_services, delete_pods
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from time import sleep
from tycho.context import Principal
from tycho.context import ContextFactory

logger = logging.getLogger(__name__)

"""
Tycho context for application management.
Manages application metadata, discovers and invokes TychoClient, etc.
"""
tycho = ContextFactory.get (
    context_type=settings.TYCHO_MODE,
    product=settings.APPLICATION_BRAND)
    
class ApplicationManager(generic.TemplateView, LoginRequiredMixin):

    """ Application manager controller. """
    template_name = 'apps_pods.html'
    
    def get_context_data(self, *args, **kwargs):
        """
        Query the service manager to determine what services are currently running for this user.
        Create data structures to allow the view to render results.
        """
        context = super(ApplicationManager, self).get_context_data(*args, **kwargs)
        brand = settings.APPLICATION_BRAND
        logger.debug (f"-- running tycho.status() to get running systems.")
        status = tycho.status ({
            'username' : self.request.user.username
        })
        services = []
        logger.debug (f"-- received {len(status.services)} services in tycho response.")
        for service in status.services:
            name = service.name.split("-")[0]
            lname = name.capitalize()
            service_url = f"/private/{service.name}/{self.request.user.username}/{service.identifier}/"
            services.append({
                'full_name'     : service.name,
                'name'          : service_url,
                'lname'         : lname,
                'logo_name'     : f'{lname} Logo',
                'logo_path'     : f'/static/images/{name}-logo.png',
                'ip_address'    : "",
                'port'          : "",
                'identifier'    : service.identifier,
                'creation_time' : service.creation_time
            })
        brand_map = get_brand_details (brand)
        for app_id, app in tycho.apps.items ():
            app['app_id'] = app_id
            logger.debug (f"-- app: {json.dumps(app, indent=2)}")
        apps = sorted(tycho.apps.values (), key=lambda v: v['name'])
        return {
            "brand"        : brand, #brand_map['name'],
            "logo_url"     : f"/static/images/{brand}/{brand_map['logo']}",
            "logo_alt"     : f"{brand_map['name']} Image",
            "svcs_list"    : services,
            "applications" : apps
        }
    
class AppStart(generic.TemplateView, LoginRequiredMixin):

    """ Application manager controller. """
    template_name = 'starting.html'
    
    def get_context_data(self, *args, **kwargs):
        """
        Start an application.
        """
        principal = Principal (self.request.user.username)
        app_id = self.request.GET['app_id']
        system = tycho.start (principal, app_id)
        return {
            "url" : f"/private/{app_id}/{principal.username}/{system.identifier}/"
        }

def list_services(request):
    if request.method == "POST":
        action = request.POST.get("action")
        sid = request.POST.get("id")
        logger.debug (f"-- action: {action} sid: {sid}")
        if action == "delete":
            tycho.delete ({ "name" : sid })
            #delete_pods(request, sid)
            sleep(2)
    return HttpResponseRedirect("/apps/")

def login_whitelist(request):
    full_brand = get_brand_details (settings.APPLICATION_BRAND)['name']
    logger.debug (f"-- login_whitelist: brand: {brand}, full_brand: {full_brand}")
    return render(request, "whitelist.html", {
        "brand"      : brand,
        "full_brand" : full_brand
    })

def get_brand_details (brand):
    """
    Any special reason they can't all just be called logo.png?
    (since they're already in namespaced subdirectories)
    Sure would cut down on unproductive complexity here.
    """
    return {
        "braini"       : {
            "name" : "BRAIN-I",
            "logo" : "braini-lg-gray.png"
        },
        "scidas"       : {
            "name" : "SciDAS",
            "logo" : "scidas-logo-sm.png"
        },
        "catalyst"     : {
            "name" : "BioData Catalyst",
            "logo" : "bdc-logo.svg"
        },
        "commonsshare" : {
            "name" : "CommonsShare",
            "logo" : "logo-lg.png"
        }
    }[brand]
