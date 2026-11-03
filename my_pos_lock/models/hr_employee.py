# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    pos_auto_lock_timeout = fields.Integer(
        string="POS Auto Lock Timeout (seconds)",
        default=0,
        help="Idle seconds before this employee's POS session is locked. "
        "Leave 0 to use the common timeout defined on the Point of Sale configuration.",
    )

    @api.model
    def _load_pos_data_fields(self, config):
        # Field is also declared on hr.employee.public (related), so it is safe
        # for POS users who load employees via the public profile path.
        fields_list = list(super()._load_pos_data_fields(config) or [])
        if "pos_auto_lock_timeout" not in fields_list:
            fields_list.append("pos_auto_lock_timeout")
        return fields_list


class HrEmployeePublic(models.Model):
    """Expose timeout on the public employee model.

    Odoo 20: users without full hr.employee read access load employees through
    hr.employee.public. Any field not present there raises:
      AccessError: fields "..." are not available for employee public profiles
    """
    _inherit = "hr.employee.public"

    pos_auto_lock_timeout = fields.Integer(
        string="POS Auto Lock Timeout (seconds)",
        related="employee_id.pos_auto_lock_timeout",
        readonly=True,
        compute_sudo=True,
    )
