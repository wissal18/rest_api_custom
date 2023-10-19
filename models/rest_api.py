from odoo import models, fields, api, http
from odoo.http import request


class RestAPI(models.Model):
    _name = 'rest.api'
    _rec_name = 'model_name'

    _sql_constraints = [
        ('unique_api', 'UNIQUE(method,model_id,name)', 'You already have created an api with these method and model')
    ]
    name = fields.Char('Name')
    method = fields.Selection([('get', 'GET'), ('post', 'POST'), ('put', 'PUT'), ('delete', 'DELETE')])
    model_id = fields.Many2one('ir.model', string='Model')
    model_name = fields.Char(related='model_id.model')
    fields_list = fields.Many2many('ir.model.fields')

    @api.onchange('model_id')
    def _onchange_model(self):
        for record in self:
            if record.model_id:
                record.fields_list = None

    def action(self, method, model, fields=None):

        modelAPI = self.env[model]
        model_fields = fields.mapped('name')
        res = request.get_json_data()

        if method == 'get':
            result = modelAPI.search([]).read(model_fields if fields else [])

        if method == 'post':
            obj = {}
            if model_fields:
                for key in model_fields:
                    obj[key] = res[key]
                res = obj
            # if model_fields is empty the record will be created using the json data else it will be created using only the fields founded in model_fields
            result = modelAPI.create(res)

        if method == 'put':
            if model_fields:
                print(model_fields)
                obj = {}
                for key, value in res.items():
                    if key in model_fields:
                        obj[key] = value

            # the id of the record is obtained from the json data
            result = modelAPI.browse(res['id']).update(obj if model_fields else res)

        if method == 'delete':
            result = modelAPI.browse(res['id']).unlink()
        return {
            'method': method,
            'model': model,
            'result': result
        }

    def action_confirm(self):
        return
