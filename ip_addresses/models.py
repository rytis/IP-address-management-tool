from django.db import models
from django.forms import ModelForm
import socket

# Create your models here.

class NetworkAddress(models.Model):
    address = models.IPAddressField()
    network_size = models.PositiveIntegerField()
    description = models.CharField(max_length=400)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return "%s/%d" % (self.address, self.network_size)

    @models.permalink
    def get_absolute_url(self):
        return ('networkaddress-display', (), {'address': '%s/%s' % (self.address, self.network_size)})

    def get_hostname(self):
        try:
            fqdn = socket.gethostbyaddr(str(self.address))[0]
        except:
            fqdn = ''
        return fqdn

    def get_formated_address(self):
        return str(self.address).replace('.', '_')

    def get_netmask(self):
        bit_netmask = 0;
        bit_netmask = pow(2, self.network_size) - 1
        bit_netmask = bit_netmask << (32 - self.network_size)
        nmask_array = []
        for c in range(4):
            dec = bit_netmask & 255
            bit_netmask = bit_netmask >> 8
            nmask_array.insert(0, str(dec))
        return ".".join(nmask_array)



class NetworkAddressAddForm(ModelForm):
    class Meta:
        model = NetworkAddress
        exclude = ('parent', )

class NetworkAddressModifyForm(ModelForm):
    class Meta:
        model = NetworkAddress
        fields = ('description',)


class DNSServer(models.Model):
    address = models.IPAddressField()
    comment = models.CharField(max_length=400)

    def __unicode__(self):
        return "%s (%s)" % (self.address, self.comment[:20])

class DomainName(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=400)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.comment[:20])

class DHCPNetwork(models.Model):
    physical_net = models.OneToOneField(NetworkAddress)
    router = models.IPAddressField()
    dns_server = models.ForeignKey(DNSServer)
    domain_name = models.ForeignKey(DomainName)

    def __unicode__(self):
        return "%s/%s" % (self.physical_net.address, self.physical_net.network_size)

    @models.permalink
    def get_absolute_url(self):
        return ('dhcpnetwork-display', (), {'address': '%s/%s' % (self.physical_net.address, self.physical_net.network_size)})

class DHCPNetworkAddForm(ModelForm):
    class Meta:
        model = DHCPNetwork
        exclude = ('physical_net',)

class ClassRule(models.Model):
    rule = models.TextField()
    description = models.CharField(max_length=400)

    def __unicode__(self):
        return self.description[:20]

    @models.permalink
    def get_absolute_url(self):
        return ('classrule-display', (), {'object_id': self.id})

class ClassRuleForm(ModelForm):
    class Meta:
        model = ClassRule

class DHCPAddressPool(models.Model):
    dhcp_network = models.ForeignKey(DHCPNetwork)
    class_rule = models.ForeignKey(ClassRule, null=True, blank=True)
    range_start  = models.IPAddressField()
    range_finish = models.IPAddressField()

    def __unicode__(self):
        return "%s/%s" % (self.range_start, self.range_finish)

    def __str__(self):
        return "%s/%s" % (self.range_start, self.range_finish)

    @models.permalink
    def get_absolute_url(self):
        return ('dhcpaddresspool-display', (), {'range_start': self.range_start, 'range_finish': self.range_finish})
    
class DHCPAddressPoolForm(ModelForm):
    class Meta:
        model = DHCPAddressPool
        exclude = ('dhcp_network',)

