# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
{
    'name': 'Fixed Asset',
    'version': '1.0',
    'description': """
    Este módulo permite la administración de activos fijos bajo la norma
    de contabilidad boliviana.
    """,
    "author": "SisCruz,"
              "Business Consulting Solution",
    'website': 'http://www.siscruz.com',
    "depends": ['account_asset'],
    "category": "Generic Modules",
    "data": ['views/account_asset_view.xml',
            #This will link to a file in the folder data. This file, defaultdata.xml will contain the data that is automatically installed when the module is installed.
            'data/default_data.xml',
             ],
    "installable": True,
    "auto_install": True,
}
