from www_example_com.ip_addresses.models import *
from django.contrib import admin

class NetworkAddressAdmin(admin.ModelAdmin):
    pass

class DHCPNetworkAdmin(admin.ModelAdmin):
    pass

class DNSServerAdmin(admin.ModelAdmin):
    pass

class DomainNameAdmin(admin.ModelAdmin):
    pass

class DHCPAddressPoolAdmin(admin.ModelAdmin):
    pass

class ClassRuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(NetworkAddress, NetworkAddressAdmin)
admin.site.register(DHCPNetwork, DHCPNetworkAdmin)
admin.site.register(DHCPAddressPool, DHCPAddressPoolAdmin)
admin.site.register(DNSServer, DNSServerAdmin)
admin.site.register(DomainName, DomainNameAdmin)
admin.site.register(ClassRule, ClassRuleAdmin)
