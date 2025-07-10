from __future__ import unicode_literals
from frappe.model.document import Document
import frappe, requests, urllib3, json, datetime, dateutil.parser, urllib, dateutil.relativedelta
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import flt, add_days, date_diff, get_request_site_address, formatdate, getdate, month_diff, today
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.accounts.utils import get_balance_on
from json import dumps
from datetime import date, timedelta
from frappe.utils.response import json_handler
from dateutil.relativedelta import relativedelta


def so_actuals_calculation(sales_order, method):
    #frappe.errprint("test")
    for item in sales_order.items:
        #frappe.errprint("test_loop")
        item.actual_amount = item.actual_qty_big * item.rate
        #item.pi_amount = item.pi_qty * item.pi_rate
        item.variance_qty = item.qty - item.actual_qty_big
        #item.variance_rate = item.actual_rate_big - item.rate
        item.variance_amt = item.net_amount - item.actual_amount
        item.pi_variance_amount = item.net_amount - item.pi_amount
        if item.actual_amount > 0:
            item.completion_percent = (item.actual_amount / item.net_amount) * 100
        if item.pi_amount > 0:
            item.progress_percent = item.pi_amount / item.net_amount * 100

def add_pi_items_so(purchase_invoice, method):
    for item in purchase_invoice.items:
        if item.so_bom and item.line_no:
            si_item = frappe.get_doc("Sales Order", item.so_bom)
            for siitem in si_item.items:
                if siitem.line_no == item.line_no:
                    if siitem.pi_amount == 0:
                        siitem.pi_amount += item.net_amount
                    else:
                        siitem.pi_amount += item.net_amount
            si_item.save()            
                  

            #frappe.errprint(si_item.item_code)
            

