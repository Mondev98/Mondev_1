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

    # Calcula el número de días transcurridos desde que un lead fue aprobado
    @api.depends('x_approved_date')  # Se recalcula cada vez que cambia la fecha de aprobación
    def _compute_x_duration_since_approved(self):
        today = fields.Date.context_today(self)  # Obtiene la fecha actual según el contexto del usuario
        for rec in self:
            if rec.x_approved_date:
                # Calcula la diferencia en días entre hoy y la fecha de aprobación
                rec.x_duration_since_approved = (today - rec.x_approved_date).days
            else:
                # Si no hay fecha de aprobación, la duración es 0
                rec.x_duration_since_approved = 0
    
    
    # Acción para aprobar un lead
    def action_approve_lead(self):
        today = fields.Date.context_today(self)  # Obtiene la fecha actual
        for rec in self:
            # Actualiza los campos de aprobación, fecha y plazo de entrega
            rec.write({
                'x_approved_by': self.env.user.id,  # Usuario que aprueba
                'x_approved_date': today,           # Fecha de aprobación
                'x_delivery_deadline': today,       # Fecha límite de entrega (igual al día de aprobación)
            })
            # Publica un mensaje en el chatter del lead
            rec.message_post(
                body=_("Lead aprobado por %s. Fecha: %s") % (self.env.user.display_name, today),
                message_type="comment",            # Tipo de mensaje: comentario
                subtype_xmlid="mail.mt_note",      # Subtipo: nota
            )
        return True
