# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.fields import Command
from odoo.tools import format_datetime, format_time, date_utils
from odoo.tools import get_lang, SQL
from odoo.exceptions import ValidationError
from datetime import datetime
# from dateutil import relativedelta


class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'


    quantity_amount = fields.Float('Amount', copy=False)



