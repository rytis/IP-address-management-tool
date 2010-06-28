from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from models import *
import views
from django.core.urlresolvers import reverse

classrule_info = {
    'queryset': ClassRule.objects.all(),
    'template_name': 'display_classrule.html',
}

classrule_form = {
    'form_class': ClassRuleForm,
    'template_name': 'add.html',
}

classrule_delete = {
    'model': ClassRule,
    'post_delete_redirect': '../..',
    'template_name': 'delete_confirm_classrule.html',
}

urlpatterns = patterns('',
    url(r'^networkaddress/$', views.networkaddress_display, name='networkaddress-displaytop'),
    url(r'^networkaddress/add/$', views.networkaddress_add, name='networkaddress-addtop'),
    url(r'^networkaddress/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/$', views.networkaddress_display, name='networkaddress-display'),
    url(r'^networkaddress/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/delete/$', views.networkaddress_delete, name='networkaddress-delete'),
    url(r'^networkaddress/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/add/$', views.networkaddress_add, name='networkaddress-add'),
    url(r'^networkaddress/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/modify/$', views.networkaddress_modify, name='networkaddress-modify'),
    url(r'^networkaddress/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/add_dhcp/$', views.dhcpnetwork_add, name='networkaddress-adddhcp'),
    url(r'^networkaddress/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/ping/$', views.networkaddress_ping, name='networkaddress-ping'),
    url(r'^networkaddress/$', views.networkaddress_ping, name='networkaddress-ping-url'),

    url(r'^dhcpnetwork/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/$', views.dhcpnetwork_display, name='dhcpnetwork-display'),
    url(r'^dhcpnetwork/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/delete/$', views.dhcpnetwork_delete, name='dhcpnetwork-delete'),
    url(r'^dhcpnetwork/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/modify/$', views.dhcpnetwork_modify, name='dhcpnetwork-modify'),
    url(r'^dhcpnetwork/(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})/add_dhcppool/$', views.dhcpaddresspool_add, name='dhcpnetwork-addpool'),

    url(r'^dhcpaddresspool/add/$', views.dhcpaddresspool_add),
    url(r'^dhcpaddresspool/(?P<range_start>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(?P<range_finish>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/$', views.dhcpaddresspool_display, name='dhcpaddresspool-display'),
    url(r'^dhcpaddresspool/(?P<range>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/delete/$', views.dhcpaddresspool_delete, name='dhcpaddresspool-delete'),

    url(r'^classrule/$', list_detail.object_list, classrule_info, name='classrule-displaytop'),
    url(r'^classrule/(?P<object_id>\d+)/$', list_detail.object_detail, classrule_info, name='classrule-display'),
    url(r'^classrule/(?P<object_id>\d+)/modify/$', create_update.update_object, classrule_form, name='classrule-modify'),
    url(r'^classrule/(?P<object_id>\d+)/delete/$', create_update.delete_object, classrule_delete, name='classrule-delete'),
    url(r'^classrule/add/$', create_update.create_object, classrule_form, name='classrule-add'),

    url(r'^dhcpd.conf/$', views.dhcpd_conf_generate, name='dhcp-conf-generate'),
)

