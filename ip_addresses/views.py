from www_example_com.ip_addresses.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
import subprocess

# NETWORKADDRESS view functions

def networkaddress_display(request, address=None):
    parent = get_network_object_from_address(address)
    addr_list = NetworkAddress.objects.filter(parent=parent)
    has_subnets = False
    for address in addr_list:
        if address.network_size != 32:
            has_subnets = True
    try:
        dhcp_net = DHCPNetwork.objects.get(physical_net=parent)
    except:
        dhcp_net = None
    return render_to_response('display.html', {'parent': parent, 
                                               'addresses_list': addr_list, 
                                               'has_subnets': has_subnets,
                                               'dhcp_net': dhcp_net,})

def networkaddress_delete(request, address=None):
    address_obj = get_network_object_from_address(address)
    parent = address_obj.parent
    address_obj.delete()
    redirect_to = '../../../'
    if parent:
        redirect_to = parent.get_absolute_url()
    return HttpResponseRedirect(redirect_to)

def networkaddress_add(request, address=None):
    if request.method == 'POST':
        parent = get_network_object_from_address(address)
        new_address = NetworkAddress(parent=parent)
        form = NetworkAddressAddForm(request.POST, instance=new_address)
        if form.is_valid():
            form.save()
            url = parent.get_absolute_url() if parent else reverse('networkaddress-displaytop')
            return HttpResponseRedirect(url)
    else:
        form = NetworkAddressAddForm()
    return render_to_response('add.html', {'form': form,})    

def networkaddress_modify(request, address=None):
    address_obj = get_network_object_from_address(address)
    if request.method == 'POST':
        # submitting changes
        form = NetworkAddressModifyForm(request.POST, instance=address_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(address_obj.parent.get_absolute_url())
    else:
        # first time display
        form = NetworkAddressModifyForm(initial={ 'description': address_obj.description, })
    return render_to_response('add.html', {'form': form,})

# DHCPNETWORK view functions

def dhcpnetwork_add(request, address=None):
    if request.method == 'POST':
        network_addr = get_network_object_from_address(address)
        dhcp_net = DHCPNetwork(physical_net=network_addr)
        form = DHCPNetworkAddForm(request.POST, instance=dhcp_net)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(network_addr.get_absolute_url())
    else:
        form = DHCPNetworkAddForm()
    return render_to_response('add.html', {'form': form,})

def dhcpnetwork_delete(request, address=None):
    network_addr = get_network_object_from_address(address)
    get_dhcp_object_from_address(address).delete()
    return HttpResponseRedirect(network_addr.get_absolute_url())

def dhcpnetwork_modify(request, address=None):
    ip, net_size = address.split('/')
    network_addr = NetworkAddress.objects.get(address=ip, network_size=int(net_size))
    dhcp_net = DHCPNetwork.objects.get(physical_net=network_addr)
    if request.method == 'POST':
        # submiting changes
        form = DHCPNetworkAddForm(request.POST, instance=dhcp_net)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(dhcp_net.get_absolute_url())
    else:
        # first time display
        form = DHCPNetworkAddForm(instance=dhcp_net)
    return render_to_response('add.html', {'form': form,})

def dhcpnetwork_display(request, address=None):
    dhcp_net = get_dhcp_object_from_address(address)
    dhcp_pools = DHCPAddressPool.objects.filter(dhcp_network=dhcp_net)
    class_rules = ClassRule.objects.all()
    return render_to_response('display_dhcp.html', {'dhcp_net': dhcp_net,
                                                    'dhcp_pools': dhcp_pools,
                                                    'class_rules': class_rules,})

# DHCPADDRESSPOOL views

def dhcpaddresspool_display(request, range_start=None, range_finish=None):
    return HttpResponse('not implemented')

def dhcpaddresspool_add(request, address=None):
    if request.method == 'POST':
        dhcp_net = get_dhcp_object_from_address(address)
        pool = DHCPAddressPool(dhcp_network=dhcp_net)
        form = DHCPAddressPoolForm(request.POST, instance=pool)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(dhcp_net.get_absolute_url())
    else:
        form = DHCPAddressPoolForm()
    return render_to_response('add.html', {'form': form,})

def dhcpaddresspool_delete(request, range=None):
    range_start, range_finish = range.split('/')
    pool_obj = DHCPAddressPool.objects.get(range_start=range_start, range_finish=range_finish)
    dhcp_net = pool_obj.dhcp_network
    pool_obj.delete()
    return HttpResponseRedirect(dhcp_net.get_absolute_url())

# CLASSRULE views

def classrule_display(request, rule_id=None):
    class_rules = ClassRule.objects.all()
    return render_to_response('display_classrules.html')

def classrule_add(request):
    if request.method == 'POST':
        form = ClassRuleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        form = ClassRuleForm()
    return render_to_response('add.html', {'form': form,})


def networkaddress_ping(request, address=None):
    if responding_to_ping(address):
        msg = "Ping OK"
    else:
        msg = "No response"
    return HttpResponse(msg)

def dhcpd_conf_generate(request):
    class_rules = ClassRule.objects.all()
    networks = []
    for net in DHCPNetwork.objects.all():
        networks.append( { 'dhcp_net': net,
                           'pools': DHCPAddressPool.objects.filter(dhcp_network=net),
                         } )

    return render_to_response('dhcpd.conf.txt', 
                              {'class_rules': class_rules,
                               'networks': networks,
                              }, 
                              mimetype='text/plain')


############################################################################
# helper functions

def get_network_object_from_address(address):
    if address:
        ip, net_size = address.split('/')
        object = NetworkAddress.objects.get(address=ip, network_size=int(net_size))
    else:
        object = None
    return object

def get_dhcp_object_from_address(address):
    if address:
        object = DHCPNetwork.objects.get(physical_net=get_network_object_from_address(address))
    else:
        object = None
    return object

def responding_to_ping(address, timeout=1):
    rc = subprocess.call("ping -c 1 -W %d %s" % (timeout, address), 
                         shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
    if rc == 0:
        return True
    else:
        return False


