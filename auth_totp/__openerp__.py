#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Klaus-D. Hagemann (<http://www.hagemann-do.de>).
#    @author Klaus-D. Hagemann
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# #############################################################################
# 2016-05-13, kdhagema@gmx.de                                                 #
# (c) Klaus-D. Hagemann, Dortmund, Germany                                    #
# #############################################################################
{
    'name': "Authentication via TOTP Login",
    'version': "0.1.001_Rev.24061",
    'author': "Klaus-D. Hagemann, Dortmund, Germany",
    'website': "http://www.hagemann-do.de",
    'maintainer': "Klaus-D. Hagemann, Dortmund, Germany",
    'category': "Authentication",
    'depends': [
        'base', 
        'web', 
    ],
    'data': [
        'res_users_view.xml',
        'totp_config_ip_view.xml',
        'data/totp_config_ip_default.xml',
        'security/ir.model.access.csv',
    ],
    'js': [
        'static/src/js/chrome.js',
        'static/src/js/coresetup.js',
    ],
    'qweb' : [
        'static/src/xml/*.xml',
    ],
    'description': """
Authentication via TOTP Login
=============================

This AddOn provides a feature for a Two-Factor Authentication in OpenERP.

It computes and validates Time-Based OneTimePasswords (TOTP) compatible with i.e. Google Autenticator.

You can specify if a TOTP is required for login based on rules for IP-Adresses / IP-Networks.
Hence it is i.e. possible to allow all your local subnet hosts to login WITHOUT a TOTP, while 
all the field engineers (accessing OpenERP from outside your LAN) must authenticate WITH their PASSWORD AND a TOTP.

Important Note
--------------
The TOTP is created based on a certain time interval (every 30sec.).
In case you decide to use an authenticator App on your smartphone (highly recommended), it is essential, that 
the time difference between your smartphone and the server time is as minimal as possible (at least less than
the validity interval for a TOTP=30sec). Thus you are highly encouraged to run an ntp client on your OpenERP server.

Prerequisites
-------------
* install python package 'ipaddr' (see https://github.com/google/ipaddr-py) or use "$ apt-get install python-ipaddr"
* install python package 'pyqrcode' (see https://pypi.python.org/pypi/PyQRCode) via pypi or use "$ python setup.py install" after download. For details see also http://pythonhosted.org/PyQRCode/
* install python package 'pypng' (see https://pypi.python.org/pypi/pypng/) via pypi or use "$ python setup.py install" after download.

* module 'onetimepass' is shipped with this package, and is also available on https://github.com/tadeck/onetimepass . For details on 'onetimepass' see also http://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python
* module 'six' is shipped with this package, and is also available on https://pythonhosted.org/six/

Optional, but recommended
-------------------------
* Check your AppStore for the Google Authenticator App and install it on your smartphone. This AddOn supports the generation of a QRCode which can be sanned by the smartphone app for a super-easy configuration.
* Google Authenticator for Android is available here: https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en
* Google Authenticator for iOS is available here: https://itunes.apple.com/en/app/google-authenticator/id388497605?mt=8
* Make your OpenERP server listening to a ntp server (ie "$ apt-get install ntp").

Configuration
-------------
* By default, all hosts are allowed to log in WITHOUT TOTP authentication. The installation adds an automatic rule to the IP configuration table with sequence 999.
* Go to General Settings / Configuration / TOTP IP Addresses and add the rules and ranges as per your requirements.
* Go to the General Setting / Users and on the notebok-tab 'TOTP Secret Code' generate a code for those users, which needs to be able to access your OpenERP server via TOTP-Authentication.
* Scan the QR-Code with your smartphone app (ie. Google Authenticator).

Licence notes
-------------
* module 'ontimepass' is created by Tomasz Jaskowski (contact http://github.com/tadeck) and published under the MIT license.
* module 'six' is created by Benjamin Peterson (contact https://benjamin.pe) and published under the MIT license.
* Concept, development and maintenance of this AddOn by Hagemann EDV Service, Dipl.-Ing. Klaus-D. Hagemann, Dortmund, Germany.
* All rights reserved by their respective owners.

ToDo
----
* make fixed values for secret-length (16 chars) and time interval (30 sec) dynamic and configurable

    """,
    'init_xml': [],
    'demo_xml': [],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'certificate': None,
    'external_dependencies' : {
        'python' : ['ipaddr'],
        'python' : ['pyqrcode'],
    }
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
