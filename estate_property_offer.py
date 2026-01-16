from datetime import timedelta
from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer" 
    _description = "Property Offer"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property")
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False,
        default=False,
    )

    # Computed field with Inverse
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            # Fallback to today if record isn't saved yet
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            # Updating validity based on the manually picked date
            record.validity = (record.date_deadline - base_date).days

    def action_accept(self):
        for record in self:
        # Business Logic: Set property buyer and price
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.status = "accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    #sql Constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]