IP Address management tool
==========================

This web based application keeps track of allocated IP addresses. It is also capable of
allocating and maintaining DHCP IP ranges. Once the IP ranges are defined it can produce
the ISC DHCP compatible DHCP configuration file.

This is a Django application.

The application was initially developed as an example for one of the
["Pro Python System Administration"](http://apress.com/book/view/9781430226055) book chapters.

You can find more information about the appliaction on [the project website](http://www.sysadminpy.com).

Prerequisites
-------------

You must have a recent installation of Django on your server. You can obtain your copy
from the [official Django website](http://www.djangoproject.com/download/) along with the installation instructions.

Usage
-----

Firstly, deploy the application to a directory on your server. Let's assume the following directory:

    /Users/rytis/IP-address-management-tool

Secondly, update the project name in the `urls.py` and `settings.py` configuration files.
The default setting is `IP-address-management-tool`, but you can change it to any other name.

Thirdly, make sure that the database settings are correct in the `settings.py` configuration file.
The default setting is to use the SQLite3 DB, but this can be changed to suit your needs.

Once the preparation work is done, run the DB synchronisation command to initialise the DB:

    $ python manage.py syncdb
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table ip_addresses_networkaddress
    Creating table ip_addresses_dnsserver
    Creating table ip_addresses_domainname
    Creating table ip_addresses_dhcpnetwork
    Creating table ip_addresses_classrule
    Creating table ip_addresses_dhcpaddresspool
    
    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (Leave blank to use 'rytis'): admin
    E-mail address: admin@example.com
    Password: 
    Password (again): 
    Superuser created successfully.
    Installing index for auth.Permission model
    Installing index for auth.Group_permissions model
    Installing index for auth.User_user_permissions model
    Installing index for auth.User_groups model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    Installing index for ip_addresses.NetworkAddress model
    Installing index for ip_addresses.DHCPNetwork model
    Installing index for ip_addresses.DHCPAddressPool model
    No fixtures found.
    $ 

You can also load initial sample data into the database. You can always remove it later.

    $ python manage.py loaddata sample_data.json 
    Installing json fixture 'sample_data' from absolute path.
    Installed 20 object(s) from 1 fixture(s)
    $

Once the data is loaded, start the Django built-in web server to test that the application is
functioning correctly:

    $ python manage.py runserver 1111
    Validating models...
    0 errors found
    
    Django version 1.2.1, using settings 'IP-address-management-tool.settings'
    Development server is running at http://127.0.0.1:1111/
    Quit the server with CONTROL-C.

If you're happy with the result, you can then integrate this application with your
web server, for example Apache.
