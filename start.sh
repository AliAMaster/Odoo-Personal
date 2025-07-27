#!/bin/bash
source .venv/Scripts/activate
python odoo-bin -r Odoo -w buckbeak --addons-path=addons,custom -u custom_accounting,main_menu --dev xml --xmlrpc-interface=0.0.0.0 --log-level=error