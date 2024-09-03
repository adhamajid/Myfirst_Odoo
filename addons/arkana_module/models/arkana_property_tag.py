from odoo import api, fields, models


class ArkanaPropertyTag(models.Model):
    _name = "arkana.property.tag"
    _description = "Arkana Property Tag"

    name= fields.Char(required=True)

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The tag name must be unique.'),
    ]