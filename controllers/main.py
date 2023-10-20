from odoo import http
from odoo.http import request
import json


class RestAPICustomController(http.Controller):

    @http.route(['api/<name>','api/<name>/<int:id>'], auth='public', type='json')
    def rest_api(self, name, id=None):
        res = {
            'success':False,
            'error': '',
            'data': None
        }
        method = request.httprequest.method
        vals = request.get_json_data()
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            res['error'] = 'Method Not allowed'
            return res
        if method in ['PUT', 'DELETE'] and (not id or not vals):
            res['error'] = 'Invalid data'
            return res
        try:
            result = request.env['rest.api'].search([('name', '=', name), ('method', '=', method)])
        except:
            res['error'] = 'API does not exist'
            return res
        if not result:
            res['error'] = 'API does not exist'
            return res
        try:
            data = result.action(method, result, id, vals)
        except Exeption as e:
            res['error'] = 'Error accrued when calling Api %s'%str(e)
            return res
        res.update({'success': True, 'data': data})
        return res
            

    
    
