from odoo import models, fields, api, http
from odoo.http import request


class RestAPI(models.Model):
    _name = 'rest.api'
    _rec_name = 'model_name'

    _sql_constraints = [
        ('unique_api', 'UNIQUE(method,model_id, name)', 'You already have created an api with these method and model')
    ]
    name = fields.Char('Name')
    method = fields.Selection([('get', 'GET'), ('post', 'POST'), ('put', 'PUT'), ('delete', 'DELETE')])
    model_id = fields.Many2one('ir.model', string='Model')
    fields_list = fields.Many2many('ir.model.fields')

    @api.onchange('model_id')
    def _onchange_model(self):
        for record in self:
            if record.model_id:
                record.fields_list = None

    def action(self, method,id=None, vals=None):
        modelObj = self.model_id.model
        model_fields = self.fields_list.mapped('name')
        if vals:
            vals = {key: vals[key] for key in model_fields if vals.get(key)}
        if method == 'get':
            if id:
                return modelObj.browse(id).read(model_fields)
            return modelObj.search([]).read(model_fields)
        if method == 'post':
            return {'id': modelObj.create(vals).id }        
        if method == 'put':
            modelObj.browse(id).update(vals)
            return {'id':id}
        if method == 'delete':
            modelObj.browse(id).unlink()
            return {'id':id}
        
    def action_confirm(self):
        return
