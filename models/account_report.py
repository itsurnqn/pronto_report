from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

class ProntoAccountReportCobrosTarjeta(models.Model):
        _name = 'pronto.account.report.cobros.tarjeta'
        _description = 'pronto.account.report.cobros.tarjeta'
        _auto = False

        date = fields.Date('Fecha')
        move_id = fields.Many2one('account.move', string='Asiento contable')
        etiqueta = fields.Char('Etiqueta')
        cuenta_contable = fields.Char('Cuenta contable')
        partner_id = fields.Many2one('res.partner', string='Cliente')
        debit = fields.Float('Importe')
        plan_tarjeta_id = fields.Many2one('account.payment.plan.tarjeta',string='Plan Tarjeta')
        nro_lote = fields.Integer('Nro lote')
        nro_cupon = fields.Char('Nro Cupon')
        journal_id = fields.Many2one('account.journal','Diario')

        # full_reconcile_id = fields.Integer('Asiento de conciliación')
        full_reconcile_id = fields.Many2one('account.full.reconcile','Asiento de conciliación')
        balance = fields.Float('Saldo pendiente')
        reconcile = fields.Boolean('Permitir conciliación')

        @api.model_cr
        def init(self):
                tools.drop_view_if_exists(self._cr,'pronto_account_report_cobros_tarjeta')
                self._cr.execute(""" create view pronto_account_report_cobros_tarjeta as (
                        select aml.id, aa."name" as cuenta_contable, aml.name as etiqueta, aml.full_reconcile_id, aa.reconcile, aml.date, 
                        aml.move_id, aml.journal_id, aml.partner_id, aml.credit, aml.debit, 
                        ap.plan_tarjeta_id, ap.nro_lote, ap.nro_cupon, aml.balance
                        from account_move_line aml
                        left join account_payment ap on ap.id = aml.payment_id
                        left join account_account aa on aml.account_id = aa.id
                        left join account_journal aj on aj.id = ap.journal_id
                        where aj.is_credit_card = true
                        and aml.debit > 0
                        order by id
                        ) """)
