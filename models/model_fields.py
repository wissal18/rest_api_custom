from odoo import models

class ModelFields(models.Model):
    _inherit='ir.model.fields'

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s' % (field.field_description)))
        return res