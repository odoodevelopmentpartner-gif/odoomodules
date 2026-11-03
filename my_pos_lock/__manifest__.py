# -*- coding: utf-8 -*-
{
    "name": "POS Auto Lock - Employee & Common Timeout",
    "version": "20.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Auto-lock POS by idle time: common timeout for all + optional per-employee timeout; unlock with employee PIN",
    "description": """
POS Auto Lock (my_pos_lock)
===========================

Secure open POS registers with automatic lock after inactivity.

**Timeouts**

* **Common timeout** – set once on the Point of Sale configuration (applies to all employees).
* **Employee timeout** – optional override on each employee (Attendance / Point of Sale).
  Leave **0** on the employee to use the common timeout.

**Unlock**

* Uses standard **Log in with Employees** (pos_hr): employee PIN or badge.
* Session stays open; only the UI is locked.

**Configuration**

1. Enable **Log in with Employees** on the POS and set employee PIN codes.
2. Enable **POS Auto Lock** and set **Common timeout (seconds)** on the POS config or Settings.
3. Optionally set **POS Auto Lock Timeout** on individual employees.
    """,
    "author": "Mayank",
    'support': 'odoodevelopmentpartner@gmail.com',
    "license": "LGPL-3",
    "depends": [
        "point_of_sale",
        "pos_hr",
        "hr",
    ],
    "data": [
        "views/pos_config_views.xml",
        "views/res_config_settings_views.xml",
        "views/hr_employee_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "my_pos_lock/static/src/app/**/*",
        ],
    },
    "images": [
        "static/description/banner.png",
        "static/description/icon.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
