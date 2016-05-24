# -*- coding: utf-8 -*-
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
{
    'name': "Partner Extension Name Fields",
    'version': "0.1.4_Rev.23876",
    'author': "Klaus-D. Hagemann",
    'license': 'AGPL-3',
    'website': "http://www.hagemann-do.de",
    'category': "Custom Modules/Partner",
    'depends': [
        'base', 
        'account_report_company',
        ],
    'data': [
        'views/res_partner_view.xml',
        ],
    'description': """
Extends the Partner form/treeview/kanban by two new name fields.
  - Form View:
    - Name 2
    - Name 3  
  - Tree View:
    - Name 2
  - Kanban View:
    - Name 2 (included in Kanban Box Heading)
    """,
    'update_xml': [
        'views/res_partner_view.xml'],
    'installable': True,
    'auto_install': False,
    'certificate': None,
 }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
