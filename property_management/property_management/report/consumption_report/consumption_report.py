# Copyright (c) 2024, QCS and contributors
# For license information, please see license.txt

import frappe


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
			"options": "Consumption",
			"width": 200,
		},
		{
			"label": "Rental Unit",
			"fieldname": "rental_unit",
			"fieldtype": "Link",
			"options": "Rental Units",
			"width": 200,
		},
		{
			"label": "Posting Date",
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 200,
		},
		{
			"label": "Owner Name",
			"fieldname": "owner_name",
			"fieldtype": "Link",
			"options": "Owners and Landlords",
			"width": 200,
		},
		{
			"label": "Location",
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Property Type",
			"fieldname": "property_type",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Building Name",
			"fieldname": "building_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Property No",
			"fieldname": "property_no",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Plot No",
			"fieldname": "plot_no",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Water Consumption",
			"fieldname": "water_consumption",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Hot Water Consumption",
			"fieldname": "hot_water_consumption",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": "Electricity Consumption",
			"fieldname": "electricity_consumption",
			"fieldtype": "Data",
			"width": 200,
		},
	]
	return columns
	
	
def get_data(filters):
	query_filters = []
	if filters.get("rental_unit"):
		query_filters.append(["rental_unit", "=", filters.get("rental_unit")])
	query_filters.append(["date", ">=", filters.get("from_date")])
	query_filters.append(["date", "<=", filters.get("to_date")])
	if filters.get("property_type"):
		query_filters.append(["property_type", "=", filters.get("property_type")])
	if filters.get("owner_name"):
		query_filters.append(["owner_name", "=", filters.get("owner_name")])

	data = []
	cons_doc = frappe.get_all("Consumption", filters=query_filters, fields=["name", "owner_name"])
	if cons_doc:
		for i in cons_doc:
			doc = frappe.get_doc("Consumption", i)
			data.append({"name": doc.name, "rental_unit": doc.rental_unit, "date": doc.date, "owner_name": doc.owner_name, "location": doc.location, "property_type": doc.property_type, "building_name": doc.building_name, "property_no": doc.property_no, "plot_no": doc.plot_no, "water_consumption": doc.water_consumption, "electricity_consumption": doc.electricity_consumption, "hot_water_consumption": doc.hot_water_consumption})
   
	return data
