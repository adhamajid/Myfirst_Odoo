from odoo import api, fields, models


class ArkanaPropertyType(models.Model):
    _name = "arkana.property.type"
    _description = "Arkana Property Type"

    name= fields.Char(required=True)

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The type name must be unique.'),
    ]