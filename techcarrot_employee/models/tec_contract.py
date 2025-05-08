# -*- coding: utf-8 -*-

from odoo import api, models, _, fields
from odoo.exceptions import ValidationError
from datetime import datetime
import re
import phonenumbers

class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    aat_allowance = fields.Monetary('AAT Allowance', copy=False)
    sub_total = fields.Monetary('Sub Total', copy=False)
