from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

class ProntoSaleReportOrder(models.Model):
        _name = 'pronto.sale.report.order'
        _description = 'pronto.sale.report.order'
        _auto = False

        partner_id = fields.Many2one('res.partner', string='Cliente')
        date_order = fields.Datetime('Fecha pedido')
        state = fields.Char('Estado')
        
        @api.model_cr
        def init(self):
                tools.drop_view_if_exists(self._cr,'pronto_sale_report_order')
                self._cr.execute(""" create view pronto_sale_report_order as (
                            select id, partner_id, date_order, state from sale_order order by id
                        ) """)
