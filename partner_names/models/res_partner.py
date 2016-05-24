# encoding: utf-8 -*-
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
import logging
import pdb
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper

DISPLAY_NAME_TRIGGER_FLDS = ['parent_id', 'is_company', 'name', 'x_name2', 'x_name3']

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _order   = 'display_name'

    # below are functions from account_report_company.py which adds the new field display_name to res.partner
    # we need this here to make changes in x_name2/x_name3 fields changing the display_name field
    def _display_name_compute_mc(self, cr, uid, ids, name, args, context=None):
        context = dict(context or {})
        context.pop('show_address', None)
        my_name_get = self.name_get(cr, uid, ids, context=context)
        return dict(my_name_get)

    _display_name_store_triggers_mc = {
        'res.partner': (lambda self,cr,uid,ids,context=None: self.search(cr, uid, [('id','child_of',ids)]), DISPLAY_NAME_TRIGGER_FLDS, 5),
    }

    # indirection to avoid passing a copy of the overridable method when declaring the function field
    _display_name_mc = lambda self, *args, **kwargs: self._display_name_compute_mc(*args, **kwargs)
	
    _columns = {
        'display_name': fields.function(_display_name_mc, type='char', string='Name', store=_display_name_store_triggers_mc, select=1),
        'x_name2': fields.char('Name 2', size=128),
        'x_name3': fields.char('Name 3', size=128),
        }

    _defaults = {
        'x_name2': '',
        'x_name3': '',
        }

    def build_display_name(self, name, x_name2, x_name3, parent_id, is_company, context=None):
    
        if context is None:
            context = {}
        
        ret_name = name
        
        if x_name2:
            ret_name = '%s %s' % (name, x_name2)
        if x_name3:
            if x_name2:
                ret_name = '%s %s %s' % (name, x_name2, x_name3)
            else:
                name = '%s %s' % (name, x_name3)
        if parent_id and not is_company:
            ret_name =  "%s %s - %s" % (parent_id.name, (parent_id.x_name2 or ''), ret_name)

        ret_name = ret_name.replace('  ',' ')
        
        return ret_name
       
    def name_get(self, cr, uid, ids, context=None):
    
        #overrides the name_get method of he inherited object to implement new x_nameY-fields for naming
        
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []

        res = []
        
        # save the value of the original name_get method
        sup_name = super(res_partner, self).name_get(cr, uid, ids, context=context)

        for record in self.browse(cr, uid, ids, context=context):
            #put the business logic for 'name' to a separate function for code reuse
            name = self.build_display_name(record.name, record.x_name2, record.x_name3, record.parent_id, record.is_company, context=context)
                
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
                name = name.replace('\n\n','\n')
                name = name.replace('\n\n','\n')

            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)

            name = name.replace('  ',' ')
            
            res.append((record.id, name))
            
        return res
       
    def _get_display_name(self, unaccent):
        # TODO: simplify this in trunk with `display_name`, once it is stored
        # Perf note: a CTE expression (WITH ...) seems to have an even higher cost
        #            than this query with duplicated CASE expressions. The bulk of
        #            the cost is the ORDER BY, and it is inevitable if we want
        #            relevant results for the next step, otherwise we'd return
        #            a random selection of `limit` results.

        # return """CASE WHEN company.id IS NULL OR res_partner.is_company
        #                THEN {partner_name} 
        #                ELSE {company_name} || ', ' || {partner_name} 
        #            END""".format(partner_name=unaccent('res_partner.name'),
        #                          company_name=unaccent('company.name'))

        return """CASE WHEN company.id IS NULL OR res_partner.is_company THEN
                               CASE WHEN {partner_x_name2} IS NULL AND {partner_x_name3} IS NOT NULL THEN
                                         {partner_name} || ', ' || {partner_x_name3}
                                    WHEN {partner_x_name2} IS NOT NULL AND {partner_x_name3} IS NULL THEN
                                         {partner_name} || ', ' || {partner_x_name2}
                                    WHEN NOT ({partner_x_name2} IS NULL AND {partner_x_name3} IS NULL) THEN
                                         {partner_name} || ', ' || {partner_x_name2} || ', ' || {partner_x_name3}
                                    ELSE {partner_name}
                                    END
                               ELSE CASE WHEN {partner_x_name2} IS NULL AND {partner_x_name3} IS NOT NULL THEN
                                              {company_name} || ', ' || {partner_name} || ', ' || {partner_x_name3}
                                         WHEN {partner_x_name2} IS NOT NULL AND {partner_x_name3} IS NULL THEN
                                              {company_name} || ', ' || {partner_name} || ', ' || {partner_x_name2}
                                         WHEN NOT ({partner_x_name2} IS NULL AND {partner_x_name3} IS NULL) THEN
                                              {company_name} || ', ' || {partner_name} || ', ' || {partner_x_name2} || ', ' || {partner_x_name3}
                                    ELSE {company_name} || ', ' || {partner_name}
                                    END
                               END""".format(partner_name=unaccent('res_partner.name'),
                                             partner_x_name2=unaccent('res_partner.x_name2'),
                                             partner_x_name3=unaccent('res_partner.x_name3'),
                                             company_name=unaccent('company.name'))
                                             
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
            
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):

            self.check_access_rights(cr, uid, 'read')
            where_query = self._where_calc(cr, uid, args, context=context)
            self._apply_ir_rules(cr, uid, where_query, 'read', context=context)
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(cr)
            
            display_name = self._get_display_name(unaccent)

            query = """SELECT res_partner.id
                         FROM res_partner
                    LEFT JOIN res_partner company
                           ON res_partner.parent_id = company.id
                      {where} ({email} {operator} {percent}
                           OR {display_name} {operator} {percent})
                     ORDER BY {display_name}
                    """.format(where=where_str, operator=operator,
                               email=unaccent('res_partner.email'),
                               percent=unaccent('%s'),
                               display_name=display_name)

            where_clause_params += [search_name, search_name]
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            cr.execute(query, where_clause_params)
            ids = map(lambda x: x[0], cr.fetchall())
            
            if ids:
                ret = self.name_get(cr, uid, ids, context)
                logging.getLogger(__name__).debug("*******************************res_partner.name_get() returned: " + str(ret))
                return ret
            else:
                return []
                
        return super(res_partner,self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)

    logging.getLogger(__name__).debug("Class 'res_partner' loaded.")
    
res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
