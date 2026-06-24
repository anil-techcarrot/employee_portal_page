# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'  # Extend the existing HR Employee model

    # Computed field to store the number of tickets raised by the employee
    ticket_count = fields.Integer('Tickets', compute='_compute_ticket_count')

    def get_it_approval_manager(self):
        """Return the user who should approve this employee's IT tickets.

        Uses the existing 'line_manager_id' field already present on
        hr.employee (a relation to another hr.employee record, set on the
        Work tab as "Line Manager") and resolves it to that employee's
        linked Odoo user — since IT-ticket approval checks are done against
        request.env.user, not against an hr.employee record directly.

        Per explicit instruction, the standard HR 'Manager' field (parent_id)
        is NOT used here — only the dedicated Line Manager field is.
        """
        self.ensure_one()
        try:
            line_manager_emp = self.line_manager_id
        except Exception:
            return self.env['res.users']
        if line_manager_emp and line_manager_emp.user_id:
            return line_manager_emp.user_id
        return self.env['res.users']

    # Compute method to count tickets linked to each employee
    def _compute_ticket_count(self):
        for employee in self:
            employee.ticket_count = self.env['it.ticket'].search_count([
                ('employee_id', '=', employee.id)
            ])

    # Action method to open a list/form view of tickets for the current employee
    def action_view_tickets(self):
        return {
            'name': 'IT Tickets',
            'type': 'ir.actions.act_window',
            'res_model': 'it.ticket',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
        }