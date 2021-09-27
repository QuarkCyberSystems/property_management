# Copyright (c) 2021, QCS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
import frappe, requests, urllib3, json, datetime, dateutil.parser, urllib, dateutil.relativedelta
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import flt, add_days, date_diff, get_request_site_address, formatdate, getdate, month_diff, today
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.accounts.utils import get_balance_on
from json import dumps
from datetime import date, timedelta
from frappe.utils.response import json_handler
from dateutil.relativedelta import relativedelta

class ChequeReceipt(Document):
	def on_submit(self):
		
		dep_total = 0
		rent_total = 0
		other_total = 0
		dp_account = ""
		for item in self.get("cr_table"):
			if item.line_type == "Deposit":
				#dep_total += item.amount
				dp_account = item.account
				jv = frappe.new_doc("Journal Entry")
				jv.company = self.company
				jv.posting_date = item.cheque_date
				jv.naming_series = "AUTO-JV-.MM.-.YY.-.###"
				jv.append("accounts",{
                        "account":dp_account,
                        "party_type":"Customer",
						"party": self.tenant_name,
                        "credit_in_account_currency":item.amount
                        })
				jv.append("accounts",{
                        "account":frappe.get_value("Company", self.company, "default_bank_account"),
                        "debit_in_account_currency":item.amount
                        })
				jv.save()
			if item.line_type == "Rental Invoice":
				rent_total += item.amount
				jv = frappe.new_doc("Journal Entry")
				jv.company = self.company
				jv.posting_date = item.cheque_date
				jv.naming_series = "AUTO-JV-.MM.-.YY.-.###"
				jv.append("accounts",{
                        "account":frappe.get_value("Company", self.company, "default_receivable_account"),
                        "party_type":"Customer",
						"party": self.tenant_name,
                        "debit_in_account_currency":item.amount
                        })
				jv.append("accounts",{
                        "account":item.account,
                        "credit_in_account_currency":item.amount
                        })
				jv.save()

			if item.line_type == "Other Invoice":
				other_total += item.amount
		if rent_total > 0:
			si = frappe.new_doc("Sales Invoice")
			si.naming_series = "ACC-SINV-.YYYY.-"
			si.due_date = self.transaction_date
			si.posting_date = self.transaction_date
			si.company = self.company
			si.customer = self.tenant_name
			si.tenancy_contract = self.tenancy_contract
			si.contract_start = self.contract_start
			si.contract_end = self.contract_end
			si.append("items",{
				"item_code":"Rental-TNP",
				"qty": 1,
				"uom": "Nos",
				"rate":self.rent_amount,
				"cost_center": frappe.get_value("Company", self.company, "cost_center")
			})
			si.save()

		

		
			


