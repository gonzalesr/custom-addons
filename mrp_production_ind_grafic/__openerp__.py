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
    "name": "MRP - Production Printing Industry",
    "version": "8.0",
    "author": "Siscruz,"
              "Consulting Business Solution - Rolando Gonzales L.",
    "website": "http://www.siscruz.com",
    "contributors": [
        "Rolando Gonzales <rgonzales@siscruz.com>"
    ],
    "category": "Manufacturing",
    "depends": [
        "sale",
        "mrp",
        "stock",
    ],
    "data": [
        "views/mrp_production_view.xml",
        "security/ir.model.access.csv",
        "views/mrp_workflow.xml"
    ],
    "installable": True
}
