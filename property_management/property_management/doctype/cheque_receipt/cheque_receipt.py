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

	def validate(self):
		self.cheque_receipt_total = 0
		for item in self.get("cr_table"):
			
			self.cheque_receipt_total += item.amount

	def on_submit(self):
		
		dep_total = 0
		rent_total = 0
		other_total = 0
		dp_account = ""
		vat = 0
		vat_amount = 0
		vat_acc = ""
		for item in self.get("cr_table"):
			if item.line_type == "Deposit":
				#dep_total += item.amount
				dp_account = item.account
				jv = frappe.new_doc("Journal Entry")
				jv.cheque_no = item.cheque_no
				jv.cheque_date = item.cheque_date
				jv.user_remark = item.description
				jv.company = self.company
				jv.posting_date = self.transaction_date
				jv.naming_series = "AJV-.YY.-.serial_abbr.-.####"
				m_payment = frappe.get_doc("Mode of Payment", item.mode_of_payment)
				acc = ""
				for x in m_payment.accounts:
					if x.company == self.company:
						acc = x.default_account
				jv.append("accounts",{
						"account":dp_account,
						"party_type":"Customer",
						"party": self.tenant_name,
						"credit_in_account_currency":item.amount,
						"cost_center": frappe.get_value("Company", self.company, "cost_center"),
						})
				
				jv.append("accounts",{
						"account":acc,
						"debit_in_account_currency":item.amount,
						"cost_center": frappe.get_value("Company", self.company, "cost_center")
						})
				jv.cheque_receipt = self.name		
				jv.save()
				#jv.submit()
			if item.line_type == "Rental Invoice":
				rent_total += item.amount

			if item.line_type == "VAT":
				vat = 1
				vat_amount += item.amount
				vat_acc = item.account
				

			if item.line_type == "Other Invoice":
				other_total += item.amount
		if rent_total > 0:
			si = frappe.new_doc("Sales Invoice")
			si.naming_series = "ACC-SINV-.YYYY.-"
			si.set_posting_time = 1
			si.due_date = self.transaction_date
			si.posting_date = self.transaction_date
	
			#frappe.errprint(self.transaction_date)

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
			if vat == 1:
				si.append("taxes",{
				"charge_type":"Actual",
				"account_head": vat_acc,
				"description": "VAT",
				"tax_amount": vat_amount,
				"cost_center": frappe.get_value("Company", self.company, "cost_center")
			})
			si.cheque_receipt = self.name
			si.save()
			#si.submit()

			for item in self.get("cr_table"):
				if item.line_type == "Rental Invoice":
					jv = frappe.new_doc("Journal Entry")
					jv.company = self.company
					jv.posting_date = self.transaction_date
					jv.naming_series = "AJV-.YY.-.serial_abbr.-.####"
					#frappe.errprint(frappe.get_value("Company", self.company, "default_receivable_account"))
					jv.cheque_no = item.cheque_no
					jv.cheque_date = item.cheque_date
					jv.user_remark = item.description
					jv.append("accounts",{
							"account":frappe.get_value("Company", self.company, "default_receivable_account"),
							"party_type":"Customer",
							"party": self.tenant_name,
							"credit_in_account_currency":item.amount,
							#"reference_type":"Sales Invoice",
							#"reference_name":si.name,
							"cost_center": frappe.get_value("Company", self.company, "cost_center")

							
							})
					jv.append("accounts",{
							"account":item.account,
							"debit_in_account_currency":item.amount,
							"cost_center": frappe.get_value("Company", self.company, "cost_center")
							})
					jv.cheque_receipt = self.name		
					jv.save()
					#jv.submit()

		

		
			


