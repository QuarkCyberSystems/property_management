# Copyright (c) 2021, QCS and contributors
# For license information, please see license.txt

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



class Cheques(Document):
	def validate(self):
		frappe.errprint("calling clearing")
		if self.status == "Cleared":
			clear_cheque(self.name)


@frappe.whitelist()
def clear_cheque(cheque_name):
	cheque = frappe.get_doc("Cheques", cheque_name)
	if cheque.status=="Cleared":
		jv = frappe.new_doc("Journal Entry")
		jv.company = cheque.company
		jv.posting_date = cheque.cheque_date
		jv.naming_series = "AUTO-JV-.MM.-.YY.-.###"
		jv.cheque_no = cheque.cheque_no
		jv.cheque_date = cheque.cheque_date
		jv.append("accounts", {
				"account": cheque.holding_account,
				"debit_in_account_currency": cheque.amount,
				
				})
		jv.append("accounts",{
				"account": cheque.clearing_account,
				"credit_in_account_currency": cheque.amount,
				
				})
		jv.save()		


@frappe.whitelist()
def make_sales_invoice(tc_name):
	tc = frappe.get_doc("Tenancy Contract", tc_name)
	si = frappe.new_doc("Sales Invoice")
	si.company = tc.company
	si.naming_series = "ACC-SINV-.YYYY.-"
	si.customer = tc.customer
	si.tenancy_contract = tc.name
	si.posting_date = tc.start_date
	si.append("items", {
			"item_code": "Rental",
			"description": "Rent as agreed on contract",
			"qty": "1",
			"rate":tc.annual_rent,
			"enable_deferred_revenue":1,
			"service_start_date": tc.start_date,
			"service_end_date": tc.end_date,
			"service_stop_date": tc.end_date,
			"cost_center": frappe.get_value("Company", tc.company,"cost_center")
		})
	si.save()
	return 1
	
def create_cheque(sales_invoice, method):
	if sales_invoice.tenancy_contract:
		for item in sales_invoice.get("payment_schedule"):
			if item.cheque_no:
				n_chq = frappe.new_doc("Cheques")
				n_chq.company = sales_invoice.company
				n_chq.tenancy_contract = sales_invoice.tenancy_contract
				n_chq.date = sales_invoice.posting_date
				n_chq.cheque_date = item.due_date
				n_chq.cheque_no = item.cheque_no
				n_chq.amount = item.payment_amount
				n_chq.sales_invoice = sales_invoice.name
				n_chq.status = "In Hand"
				n_chq.save()
		frappe.msgprint("Cheques been created as per payment schedule!Please check and verify")			