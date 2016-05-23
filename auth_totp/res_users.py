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
import string
import random
import pyqrcode

from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _

from openerp.addons.auth_totp.onetimepass import *
_logger = logging.getLogger(__name__)

class res_users(osv.osv):
    _inherit = "res.users"
    
    def secret_generator(self, size=16, chars=string.ascii_uppercase + '234567', context=None):
        ret = ''.join(random.choice(chars) for _ in range(size))
        return ret
    
    _columns = {
        'totp_login_secret': fields.char('TOTP Login Secret', size=64, required=False),
        'totp_login_secret_qr_image': fields.binary('Authenticator QR Image', help='Use your smartphone and scan this image with your authenticator App.'),
        }
        
    def generate_totp_secret(self, cr, uid, id, context=None):
        if not context:
            context = {}
        
        for usr in self.browse(cr, uid, id, context=context):
            uname = usr.login or ''
        prefix = 'otpauth://totp/my_totp:%20' + uname + '@my_domain.com?secret='   #TODO: make this a config parameter
        secret = self.secret_generator()
        
        qr = pyqrcode.create(prefix + secret, error='H', version=10)
        qr_code_image = qr.png_as_base64_str(scale=4)
        
        return self.write(cr, uid, id, {'totp_login_secret': secret, 'totp_login_secret_qr_image': qr_code_image}, context=context)
    
    def generate_totp_pin(self, cr, uid, id, context=None):
        if not context:
            context = {}
        
        for usr in self.browse(cr, uid, id, context=context):
            user_sec = usr.totp_login_secret or False
            _logger.debug("************************************************ res_users.generate_totp_pin() user_sec=" + str(user_sec))
            if user_sec:
                check_token = get_totp(user_sec)
                _logger.debug("************************************************ res_users.generate_totp_pin() check_token=" + "%06d"%check_token)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                       'title': 'Current TOTP',
                       'text': 'The currently valid TOTP is ' + "%06d"%check_token,
                       'sticky': False
                    }
                }                
                
        return False
    
    logging.getLogger(__name__).debug("Class 'res_users' loaded.")
        
res_users()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
