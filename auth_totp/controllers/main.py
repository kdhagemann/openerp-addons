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


import logging
import ipaddr
import datetime
import openerp
from openerp.modules.registry import RegistryManager
from openerp.exceptions import Warning
from openerp.addons.auth_totp.onetimepass import *
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class Controller(openerp.addons.web.controllers.main.Session):

    @openerp.addons.web.http.jsonrequest
    def authenticate(self, req, db, login, password, totp_pin, base_location=None):
        wsgienv = req.httprequest.environ
        env = dict(
            base_location=base_location,
            HTTP_HOST=wsgienv['HTTP_HOST'],
            REMOTE_ADDR=wsgienv['REMOTE_ADDR'],
        )
        
        # first do the standard authenticate and save the returned uid
        uid = req.session.authenticate(db, login, password, env)
        if uid:
            registry = RegistryManager.get(db)
            need_totp = 'not_defined'
            ids = []
            with registry.cursor() as cr:
                # find the user who attempts a login
                user_obj = registry.get('res.users')
                user_rec = user_obj.browse(cr, uid, uid)
                user_sec = user_rec.totp_login_secret or False
                user_totp = totp_pin or ''
                user_totp = user_totp.replace(' ', '')
                remote_ip = ipaddr.IPAddress(wsgienv['REMOTE_ADDR'])
                # elaborate the ip rule definitions
                totp_ip_def = registry.get('totp.config_ip')
                ip_def_ids = totp_ip_def.search(cr, uid, [])
                for ip_def in totp_ip_def.browse(cr, uid, ip_def_ids):
                    if ip_def.ip_type == 'host':
                        if (ip_def.ip_value == '*') or (remote_ip == ipaddr.IPAddress(ip_def.ip_value)):
                            need_totp = ip_def.login_mode
                            break
                    elif ip_def.ip_type == 'network':
                        if (ip_def.ip_value == '*') or (remote_ip in ipaddr.IPNetwork(ip_def.ip_value)):
                            need_totp = ip_def.login_mode 
                            break
                _logger.debug("******** TOTP authentication rule %s matches for IP %s - procedure '%s' applies.", str(ip_def.sequence), str(remote_ip), ip_def.login_mode)
                
                if need_totp == 'usetotp':
                    if user_sec and totp_pin and valid_totp(user_totp, user_sec):
                        return self.session_info(req)
                    else:
                        _logger.debug("******** TOTP authentication failed because of invalid TOTP!")
                        return False
        
        return self.session_info(req)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
