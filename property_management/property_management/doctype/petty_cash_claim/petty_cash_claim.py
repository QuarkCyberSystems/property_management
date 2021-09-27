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


class PettyCashClaim(Document):
	def validate(self):
		self.total = 0
		for item in self.get("table_5"):
			self.total += item.amount
			
	def on_submit(self):
		jv = frappe.new_doc("Journal Entry")
		jv.company = self.company
		jv.posting_date = self.posting_date
		jv.naming_series = "AUTO-JV-.MM.-.YY.-.###"
		total = 0
		for item in self.get("table_5"):
			total += item.amount
			jv.append("accounts",{
                        "account":item.account,
                        "project":item.project,
                        "bill_no":item.bill_no,
                        "bill_date":item.bill_date,
                        "user_remark": item.description,
						"debit_in_account_currency":item.amount
                        })
		if total > 0:
			jv.append("accounts",{
				"account": self.petty_cash_account,
				"credit_in_account_currency": total
			})
			jv.petty_cash_claim = self.name
			jv.save()	



