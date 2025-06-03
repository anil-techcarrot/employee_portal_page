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
