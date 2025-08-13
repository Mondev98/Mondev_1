# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date

class CrmLead(models.Model):
    _inherit = "crm.lead"

    x_lead_category = fields.Selection(
        selection=[('residencial', 'Residencial'), ('empresarial', 'Empresarial'), ('gubernamental', 'Gubernamental')],
        string="Categoría del Lead",
        tracking=True
    )
    x_delivery_deadline = fields.Date(string="Fecha límite de entrega", tracking=True)
    x_approved_by = fields.Many2one('res.users', string="Aprobado por", tracking=True, index=True)
    x_approved_date = fields.Date(string="Fecha de aprobación", tracking=True, index=True)
    x_duration_since_approved = fields.Integer(
        string="Días desde la aprobación",
        compute="_compute_x_duration_since_approved",
        help="Días transcurridos desde la fecha de aprobación.",
        readonly=True
    )
    x_installation_required = fields.Boolean(string="Requiere instalación", tracking=True)
    x_installation_date = fields.Date(string="Fecha de instalación", tracking=True)
    x_contract_reference = fields.Char(string="Referencia de contrato", tracking=True)
    x_support_required = fields.Boolean(string="Requiere soporte postventa", tracking=True)

    @api.depends('x_approved_date')
    def _compute_x_duration_since_approved(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.x_approved_date:
                rec.x_duration_since_approved = (today - rec.x_approved_date).days
            else:
                rec.x_duration_since_approved = 0

    def action_approve_lead(self):
        """Marca el lead como aprobado por el usuario actual y registra fechas.
        - x_approved_by = usuario actual
        - x_approved_date = hoy
        - x_delivery_deadline = hoy (según requerimiento del PDF)
        """
        today = fields.Date.context_today(self)
        for rec in self:
            rec.write({
                'x_approved_by': self.env.user.id,
                'x_approved_date': today,
                'x_delivery_deadline': today,
            })
            rec.message_post(
                body=_("Lead aprobado por %s. Fecha: %s") % (self.env.user.display_name, today),
                message_type="comment",
                subtype_xmlid="mail.mt_note",
            )
        return True