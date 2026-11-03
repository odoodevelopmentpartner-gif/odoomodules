# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_auto_lock = fields.Boolean(
        related="pos_config_id.pos_auto_lock",
        readonly=False,
    )
    pos_auto_lock_use_common = fields.Boolean(
        related="pos_config_id.pos_auto_lock_use_common",
        readonly=False,
    )
    pos_auto_lock_timeout = fields.Integer(
        related="pos_config_id.pos_auto_lock_timeout",
        readonly=False,
    )
