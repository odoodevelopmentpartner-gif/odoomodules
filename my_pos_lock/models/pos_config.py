# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    pos_auto_lock = fields.Boolean(
        string="POS Auto Lock",
        help="Automatically lock the POS register after inactivity. "
        "Unlock requires an employee PIN (Log in with Employees must be enabled).",
    )
    pos_auto_lock_use_common = fields.Boolean(
        string="Use Common Timeout for All Employees",
        default=True,
        help="If enabled, all employees use the common timeout below. "
        "If disabled, each employee uses their own timeout on the employee form "
        "(0 on the employee falls back to the common timeout).",
    )
    pos_auto_lock_timeout = fields.Integer(
        string="Common Auto Lock Timeout (seconds)",
        default=60,
        help="Idle timeout in seconds. Used for every employee when "
        "'Use Common Timeout for All Employees' is enabled. "
        "When that option is disabled, this value is the fallback if an "
        "employee has timeout 0.",
    )
