
# OpenERP 7.0 module: 
# Authenticate with (Google Authenticator compatible) TOTP

  
This AddOn provides a feature for a __Two-Factor Authentication__ via a __T__ imebased __O__ n __t__ ime __P__ assword for OpenERP 7.0.

It computes and validates Time-Based OneTimePasswords (TOTP) compatible with i.e. Google Autenticator.

You can specify if a TOTP is required for login based on rules for IP-Adresses / IP-Networks.
Hence it is i.e. possible to allow all your local subnet hosts to login WITHOUT a TOTP, while all the field engineers (accessing OpenERP from outside your LAN) must authenticate WITH their PASSWORD AND a TOTP.

## Important Note

The TOTP is created based on a certain time interval (every 30sec.).
In case you decide to use an authenticator App on your smartphone (highly recommended), it is essential, that the time difference between your smartphone and the server time is as minimal as possible (at least less than the validity interval for a TOTP=30sec). Thus you are highly encouraged to run an ntp client on your OpenERP server.

## Prerequisites
  1. install python package 'ipaddr-py' (see [ipaddr-py project] ) or use `$ apt-get install python-ipaddr`
  2. install python package 'pyqrcode' (see [pyqrcode project] ); thus install it as a python module using `$ python setup.py install` after download. For details see also [pyqrcode homepage]
  3. module 'onetimepass' is shipped with this package, and is also available on [onetimepass project page] . For well explained details on 'onetimepass' see also [this Stack Overflow post] 
  4. module 'six' is shipped with this package, and is also available on [six project homepage]

## Optional, but recommended
  * Check your AppStore for the Google Authenticator App and install it on your smartphone. This AddOn supports the generation of a QRCode which can be sanned by the smartphone app for a super-easy configuration.
    * Google Authenticator for Android is available here: [Google Authenticator for Android] 
    * Google Authenticator for iOS is available here: [Google Authenticator for iOS] 
  * Make your OpenERP server listening to a ntp server (ie `$ apt-get install ntp`).

## Configuration
  1. By default, all hosts are allowed to log in WITHOUT TOTP authentication. The installation adds an automatic rule to the IP configuration table with sequence 999.
  2. Go to General Settings / Configuration / TOTP IP Addresses and add the rules and ranges as per your requirements.
  3. Go to the General Setting / Users and on the notebok-tab 'TOTP Secret Code' generate a code for those users, which needs to be able to access your OpenERP server via TOTP-Authentication.
  4. Scan the QR-Code with your smartphone app (ie. Google Authenticator).

## ToDo
  * make fixed values for secret-length (16 chars) and time interval (30 sec) dynamic and configurable

## Licence notes
  * module 'ontimepass' is created by [Tomasz Jaskowski] and published under the MIT license.
  * module 'six' is created by [Benjamin Peterson] and published under the MIT license.
  * Concept, development and maintenance of this AddOn by Hagemann EDV Service, Dipl.-Ing. Klaus-D. Hagemann, Dortmund, Germany.
  * All rights reserved by their respective owners.

Copyright (c) 2016 <mailto:kdhagema@gmx.de> All rights reserved.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


[ipaddr-py project]: https://github.com/google/ipaddr-py
[pyqrcode project]: https://pypi.python.org/pypi/PyQRCode
[pyqrcode homepage]: http://pythonhosted.org/PyQRCode/
[onetimepass project page]: https://github.com/tadeck/onetimepass
[this Stack Overflow post]: http://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python
[Tomasz Jaskowski]: http://github.com/tadeck
[six project homepage]: https://pythonhosted.org/six/
[Benjamin Peterson]: https://benjamin.pe
[Google Authenticator for Android]: https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en
[Google Authenticator for iOS]: https://itunes.apple.com/en/app/google-authenticator/id388497605?mt=8
