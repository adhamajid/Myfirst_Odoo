from odoo import models, fields
from dateutil.relativedelta import relativedelta

class ArkanaProperty(models.Model):
    _name = 'arkana.property'
    _description = "Arkana Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )

    # Five values : New, Offer Received, Offer Accepted, Sold and Canceled
    status = fields.Selection(
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('canceled', 'Canceled')
        ],
        required= True,
        copy= False,
        default='new',
    )

    active = fields.Boolean(default=False)