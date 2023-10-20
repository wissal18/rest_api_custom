from odoo import http
from odoo.http import request



class RestAPICustomController(http.Controller):

    @http.route(['/<name>','/<name>/<int:id>'], auth='public',
                type='json')
    def rest_api(self, name, id=None):
        res = {
            'success':False,
            'error': ''
        }
        method = request.httprequest.method
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            res['error'] = 'Method Not allowed'
            return res
        try:
            method = method.lower()
            result = request.env['rest.api'].search([('name', '=', name), ('method', '=', method)])

        except:
            res['error'] = 'API does not exist1'
            return res
        if not result:
            res['error'] = 'API does not exist2'
            return res
        return result[0].action(method, result, id)

    @http.route(['/report/<name>', '/report/<name>/<ids>'], auth='public',
                type='json',methods=['GET'])
    def get_report(self,name,ids=None):
        # http: // localhost: 8016 / report / count_sheet / 1, 2, 3
        res = {
            'success': False,
            'error': ''
        }
        try:
            result = request.env['rest.api'].search([('name', '=', name), ('method', '=', 'report')])
            print("3")
            print(result)
        except:
            res['error'] = 'API does not exist3'
            return res
        if not result:
            res['error'] = 'API does not exist4'
            return res
        return result[0].action('report', result, ids)

    

