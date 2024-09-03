from odoo import api, fields, models


class ArkanaPropertyType(models.Model):
    _name = "arkana.property.type"
    _description = "Arkana Property Type"

    name= fields.Char(required=True)