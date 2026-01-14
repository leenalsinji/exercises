from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer" 
    _description = "Property Offer"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property")

    # This MUST be indented (4 spaces)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False,
        default=False,
    )