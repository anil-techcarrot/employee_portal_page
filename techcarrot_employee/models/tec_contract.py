# -*- coding: utf-8 -*-

from odoo import api, models, _, fields
from odoo.exceptions import ValidationError
from datetime import datetime
import re
import phonenumbers


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    @api.depends('structure_id', 'department_id', 'structure_type_id', 'job_id')
    def _compute_employee_ids(self):
        for wizard in self:
            structure_type_id=''
            if wizard.structure_id:
                structure_type_id = wizard.structure_id.type_id.id
            elif wizard.structure_type_id:
                structure_type_id=wizard.structure_type_id.id

            domain = wizard.get_employees_domain()
            emp_objs=self.env['hr.employee'].search(domain)
            employee_objs=[]
            if structure_type_id:
                for emp_obj in emp_objs:
                    if emp_obj.structure_type_id.id == structure_type_id:
                        employee_objs.append(emp_obj.id)
            else:
                for emp_obj in emp_objs:
                    employee_objs.append(emp_obj.id)
            wizard.employee_ids = employee_objs

class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    aat_allowance = fields.Monetary('MI Allowance', copy=False)
    sub_total = fields.Monetary('Sub Total', copy=False)
    emp_code = fields.Char('Employee Code', copy=False)
    #

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'emp_code' in vals and not vals.get('employee_id') and vals['emp_code'] != False:
                emp_code = vals['emp_code']
                employee = self.env['hr.employee'].search([('emp_code', '=', emp_code)], limit=1)
                if employee:
                    vals['employee_id'] = employee.id
                else:
                    raise ValidationError(_('Employee master not found. Employee ID: %s', emp_code))
        return super(HrContractInherit, self).create(vals_list)



class HrSalaryInherit(models.Model):
    _inherit = 'hr.salary.attachment'

    emp_code = fields.Char('Employee Code', copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'emp_code' in vals and not vals.get('employee_ids') and vals['emp_code'] != False:
                emp_code = vals['emp_code']
                employee = self.env['hr.employee'].search([('emp_code', '=', emp_code)], limit=1)
                if employee:
                    vals['employee_ids'] = employee.ids
                else:
                    raise ValidationError(_('Employee master not found. Employee ID: %s', emp_code))
        return super(HrSalaryInherit, self).create(vals_list)


class HrLeaveInherit(models.Model):
    _inherit = 'hr.leave'

    emp_code = fields.Char('Employee Code', copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'emp_code' in vals and not vals.get('employee_id') and vals['emp_code'] != False:
                emp_code = vals['emp_code']
                employee = self.env['hr.employee'].search([('emp_code', '=', emp_code)], limit=1)
                if employee:
                    vals['employee_id'] = employee.id
                else:
                    raise ValidationError(_('Employee master not found. Employee ID: %s', emp_code))
        return super(HrLeaveInherit, self).create(vals_list)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    emp_code = fields.Char('Employee Code', copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'emp_code' in vals and not vals.get('employee_id') and vals['emp_code'] != False:
                emp_code = vals['emp_code']
                employee = self.env['hr.employee'].search([('emp_code', '=', emp_code)], limit=1)
                if employee:
                    vals['employee_id'] = employee.id
                else:
                    raise ValidationError(_('Employee master not found. Employee ID: %s', emp_code))
        return super(HrAttendance, self).create(vals_list)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _order = 'number desc'


    def _prepare_line_values(self, line, account_id, date, debit, credit):
        # if not self.company_id.batch_payroll_move_lines and line.code == "NET":
        #     partner = self.employee_id.work_contact_id
        # else:
        #     partner = line.partner_id
        partner = self.employee_id.work_contact_id
        product = self.env['product.product'].sudo().search([('employee_id', '=', self.employee_id.id)], limit=1)
        return {
            'name': line.name if line.salary_rule_id.split_move_lines else line.salary_rule_id.name,
            'partner_id': partner.id,
            'product_id': product.id,
            'emp_code': self.employee_id.emp_code,
            'account_id': account_id,
            'journal_id': line.slip_id.struct_id.journal_id.id,
            'date': date,
            'debit': debit,
            'credit': credit,
            'analytic_distribution': (line.salary_rule_id.analytic_account_id and {line.salary_rule_id.analytic_account_id.id: 100}) or
                                     (line.slip_id.contract_id.analytic_account_id.id and {line.slip_id.contract_id.analytic_account_id.id: 100}),
            'tax_tag_ids': line.debit_tag_ids.ids if account_id == line.salary_rule_id.account_debit.id else line.credit_tag_ids.ids,
        }


    def _get_report_name(self):
        formated_date_cache = {}
        report_name = ''
        for slip in self.filtered(lambda p: p.employee_id and p.date_from and p.date_to):
            lang = slip.employee_id.lang or self.env.user.lang
            context = {'lang': lang}
            payslip_name = slip.struct_id.payslip_name or _('Salary Slip')
            del context

            report_name = '%(employee_name)s - %(dates)s' % {
                'employee_name': slip.employee_id.legal_name,
                'dates': slip._get_period_name(formated_date_cache),
            }
        return report_name


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    def _are_payslips_ready(self):
        to_process = self.env["hr.payroll"]
        # self.env.cr.commit()
        for slip in self.mapped('slip_ids'):
            if slip.state in ['done'] and not slip.entry_id:
                to_process += slip
        return all(to_process)

