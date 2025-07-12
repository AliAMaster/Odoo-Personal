#!/bin/bash
source .venv/Scripts/activate
python odoo-bin -r Odoo -w buckbeak --addons-path=addons,custom -u custom_accounting,exercise --dev xml --xmlrpc-interface=0.0.0.0 --log-level=error