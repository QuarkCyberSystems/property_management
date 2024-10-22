# Copyright (c) 2024, QCS and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, getdate
from datetime import datetime


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data



def get_columns(filters):
	columns = [
		{
			"label": "Name",
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Tenancy Contract",
		},
		{
			"label": "Building",
			"fieldname": "building",
			"fieldtype": "Link",
			"options": "Building",
		},
		{
			"label": "Customer",
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
		},
		{
			"label": "Start Date",
			"fieldname": "start_date",
			"fieldtype": "Date",
		},
		{
			"label": "End Date",
			"fieldname": "end_date",
			"fieldtype": "Date",
		},
		{
			"label": "Grace Period",
			"fieldname": "grare",
			"fieldtype": "Date",
		},
		{
			"label": "Owner Name",
			"fieldname": "owner_name",
			"fieldtype": "Link",
			"options": "Owners and Landlords",
		},
		{
			"label": "Location",
			"fieldname": "location",
			"fieldtype": "Data",
		},
		{
			"label": "Expiry Age Count",
			"fieldname": "age_count",
			"fieldtype": "Int",
		},
		{
			"label": "Expiry 0-30",
			"fieldname": "age_30",
			"fieldtype": "Int",
		},
		{
			"label": "Expiry 30-60",
			"fieldname": "age_60",
			"fieldtype": "Int",
		},
		{
			"label": "Expiry 60-90",
			"fieldname": "age_90",
			"fieldtype": "Int",
		},
		{
			"label": "Expiry 90 Above",
			"fieldname": "age_above",
			"fieldtype": "Int",
		},
	]
	return columns


def get_data(filters):
    query_filters = []
    
    if filters.get("name"):
        query_filters.append(["name", "=", filters.get("name")])
    if filters.get("customer"):
        query_filters.append(["customer", "=", filters.get("customer")])
    if filters.get("building"):
        query_filters.append(["building", "=", filters.get("building")])
    query_filters.append(["status", "=", "Active"])

    data = []
    con_doc = frappe.get_all("Tenancy Contract", filters=query_filters, fields=["name", "customer", "building", "start_date", "end_date", "grace_period", "owner_name", "location"])
    if con_doc:
        for i in con_doc:
            doc = frappe.get_doc("Tenancy Contract", i.name)

            expiry_date = doc.end_date
            current_date = getdate(today())

            if expiry_date:
                days_count = (expiry_date - current_date).days

                age_30 = 0
                age_60 = 0
                age_90 = 0
                age_above = 0

                if days_count <= 30:
                    age_30 = days_count
                elif 30 < days_count <= 60:
                    age_60 = days_count
                elif 60 < days_count <= 90:
                    age_90 = days_count
                elif days_count > 90:
                    age_above = days_count

                data.append({
                    "name": doc.name,
                    "building": doc.building,
                    "customer": doc.customer,
                    "start_date": doc.start_date,
                    "end_date": doc.end_date,
                    "grare": doc.grace_period,
                    "owner_name": doc.owner_name,
                    "location": doc.location,
                    "age_count": days_count,
                    "age_30": age_30,
                    "age_60": age_60,
                    "age_90": age_90,
                    "age_above": age_above
                })

    return data

