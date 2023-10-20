from odoo import models, fields, api, http
from odoo.http import request


class RestAPI(models.Model):
    _name = 'rest.api'
    _rec_name = 'model_name'

    _sql_constraints = [
        ('unique_api', 'UNIQUE(method,model_id,name)', 'You already have created an api with these method and model')
    ]
    name = fields.Char('Name')
    method = fields.Selection([('get', 'GET'), ('post', 'POST'), ('put', 'PUT'), ('delete', 'DELETE'),('report','REPORT')])
    model_id = fields.Many2one('ir.model', string='Model')
    model_name = fields.Char(related='model_id.model')
    fields_list = fields.Many2many('ir.model.fields')
    report = fields.Many2one('ir.actions.report')

    @api.onchange('model_id')
    def _onchange_model(self):
            if self.model_id:
                self.fields_list = None

    @api.onchange('model_id')
    def _onchange_method(self):
        if self.model_id:
            self.report = None

    def action(self, method, model_api, id=None):

        modelAPI = self.env[model_api.model_name]
        model_fields = model_api.fields_list.mapped('name')
        res = request.get_json_data()
        result = 'No result found'

        if method == 'get':
            result = modelAPI.search([]).read(model_fields if fields else [])

        if method == 'post':
            obj = {}
            if model_fields:
                for key in model_fields:
                    obj[key] = res[key]
                res = obj
            # if model_fields is empty the record will be created using the json data else it will be created using only the fields founded in model_fields
            object = modelAPI.create(res)
            result = modelAPI.search([('id', '=', object.id)]).read(model_fields if fields else [])

        if method == 'put':
            obj = {}
            for key, value in res.items():
                if model_fields:
                    if key in model_fields:
                        obj[key] = value
            # the id of the record is obtained from the json data
            modelAPI.browse(res['id']).update(obj if model_fields else res)
            result = modelAPI.search([('id', '=', id)]).read(model_fields if fields else [])

        if method == 'delete':
            result = modelAPI.browse(id).unlink()

        if method == 'report':
            if id:
                ids = id.split(',')
                result = {}
                for i in ids:
                    result[i] = self.report.get_base_url() + '/report/html/' + self.report.report_name + '/' + i
            else :
                result = self.report.get_base_url() + '/report/html/' + self.report.report_name

        return {
            'method': method,
            'model': model_api.model_name,
            'result': result
        }

    def action_confirm(self):
        return
