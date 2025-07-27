#!/bin/bash
source .venv/Scripts/activate
python odoo-bin -r Odoo -w buckbeak --addons-path=addons,custom --dev xml --xmlrpc-interface=0.0.0.0 --log-level=error