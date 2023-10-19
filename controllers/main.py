from odoo import http
from odoo.http import request
import json


class RestAPICustomController(http.Controller):


    @http.route(['/get/<name>'], auth='public', methods=['GET'],
                type='json')
    def get_method(self, name):

        try:
            result = request.env['rest.api'].search([('name', '=', name), ('method', '=', 'get')])

        except:
            return 'Can\'t Access'
        if result:
            return result[0].action('get', result.model_name,result.fields_list)
        else:
            return "the URL entered not found"



    @http.route(['/post/<name>'], auth='public', methods=['POST'],
                type='json')
    def post_method(self, name):

        try:
            result = request.env['rest.api'].search([('name', '=', name), ('method', '=', 'post')])

        except:
            return 'Can\'t Access'
        if result:
            return result[0].action('post', result.model_name,result.fields_list)
        else:
            return "the URL entered not found"

    @http.route(['/put/<name>'], auth='public', methods=['PUT'],
                type='json')
    def put_method(self, name):

        try:
            result = request.env['rest.api'].search([('name', '=', name), ('method', '=', 'put')])

        except:
            return 'Can\'t Access'
        if result:
            return result[0].action('put', result.model_name,result.fields_list)
        else:
            return "the URL entered not found"

    @http.route(['/delete/<name>'], auth='public', methods=['DELETE'],
                type='json')
    def delete_method(self, name):

        try:
            result = request.env['rest.api'].search([('name', '=', name), ('method', '=', 'delete')])

        except:
            return 'Can\'t Access'

        if result:
            return result[0].action('delete', result.model_name,result.fields_list)
        else:
            return "the URL entered not found"



    # @http.route('/rest_api_custom/partners', auth='public', methods=['GET'])
    # def display_partners(selfself, **kw):
    #     try:
    #         partners = request.env['res.partner'].search([])
    #     except:
    #         return 'Can\'t Access'
    #     output = "<h1> Partners</h1><ul>"
    #     for partner in partners:
    #         output += '<li>' + partner.name + '</li>'
    #     output += '</ul>'
    #     # return request.render("rest_api_custom.partners_page_customized",{'partners': partners})
    #
    # @http.route('/rest_api_custom/partners/<model("res.partner"):p>/', auth='public')
    # def display_partner(self, p):
    #     print(p)
    #     # return request.render('rest_api_custom.partner_page',{'partner':p})
