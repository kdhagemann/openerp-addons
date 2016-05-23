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

from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class TOTP_Config_IP(osv.osv):
    _name = 'totp.config_ip'
    _description = 'TOTP IP Configuration'
    _order = 'sequence'
    _columns = {
        'sequence': fields.integer('Sequence', required=True, select=True, help="The IP definitions are elaborated in sequential order."),
        'ip_type': fields.selection([('host', 'Host'), ('network', 'Network')], 'IP Type', required=True, help="Specify, whether the given IP is a network or host address."),
        'ip_value': fields.char('IP Address Definition', required=True, size=64, help="Use IP address specifications in the following format:\n - xxx.xxx.xxx.xxx  for a single host\n - xxx.xxx.xxx.xxx/24  for a network\n - xxx.xxx.xxx.xxx/255.255.255.0  for a network."),
        'login_mode': fields.selection([('nototp', 'without TOTP'), ('usetotp', 'with TOTP')], 'Login mode', required=True, help="Select, if the TOTP is mandatory to login or not."),
    }
    _defaults = {
        'ip_type': 'host',
        'ip_value': '*',
        'login_mode': 'nototp',
    }
    
    def onchange_ip_value(self, cr, uid, ids, ip_value, ip_type, context=None):
        ret = {}
        if ip_value != '*':
            if ip_type == 'host':
                try:
                    ip_obj = ipaddr.IPAddress(ip_value)
                    _logger.debug("************************************************ ip_obj: " + str(ip_obj))
                except:
                    ret = {'warning': {'title': 'Warning!', 'message': 'The given value  does not appear to be an IPv4 or IPv6 host address!'},}
            elif ip_type == 'network':
                try:
                    ip_obj = ipaddr.IPNetwork(ip_value)
                    _logger.debug("************************************************ ip_obj: " + str(ip_obj))
                except:
                    ret = {'warning': {'title': 'Warning!', 'message': 'The given value  does not appear to be an IPv4 or IPv6 network address!'},}

        return ret
        
    _logger.debug("Class 'TOTP_Config_IP' loaded.")
        
TOTP_Config_IP()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
