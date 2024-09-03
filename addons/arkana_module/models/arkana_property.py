from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero

class ArkanaProperty(models.Model):
    _name = 'arkana.property'
    _description = "Arkana Property"

    name = fields.Char("Title", required=True)
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

    property_type_id = fields.Many2one("arkana.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesman", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)
    tag_ids = fields.Many2many("arkana.property.tag", string="Property Tags")
    offer_ids = fields.One2many("arkana.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = sum([record.living_area, record.garden_area])

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return {'warning': {
                'title': _("Info"),
                'message': ("Kalau pilihan itu dipencet maka akan membuat Garden Area (default: 10) & Orientation (default: North)")}}

        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.status == "canceled":
                raise UserError("Canceled property cannot be sold.")
            record.status = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.status == "sold":
                raise UserError("Sold property cannot be canceled.")
            record.status = "canceled"
        return True
    
    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.')
    ]

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        precision = 2
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=precision):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=precision) < 0:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")