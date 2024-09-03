from odoo import api, fields, models


class ArkanaPropertyOffer(models.Model):
    _name = "arkana.property.offer"
    _description = "Arkana Property Offer"

    price = fields.Float()
    state = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("arkana.property", required=True)