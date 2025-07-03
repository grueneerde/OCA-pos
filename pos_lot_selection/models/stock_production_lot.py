# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, models
from odoo.tools import float_compare


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.model
    def get_available_lots_for_pos(self, product_id, company_id, src_storage_id):
        lots = self.sudo().search(
            [
                "&",
                ["product_id", "=", product_id],
                "|",
                ["company_id", "=", company_id],
                ["company_id", "=", False],
            ]
        )


        lots = lots.filtered(
            lambda l: float_compare(
                sum(l.quant_ids.filtered(
                lambda q: q.location_id.id == src_storage_id[0] and q.location_id.usage == 'internal' or (q.location_id.usage == 'transit' and q.location_id.company_id)
            ).mapped('quantity')), 0, precision_digits=l.product_uom_id.rounding
            )
            > 0 
        )

        return lots.mapped("name")
