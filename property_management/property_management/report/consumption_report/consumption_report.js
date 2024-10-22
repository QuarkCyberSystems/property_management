// Copyright (c) 2024, QCS and contributors
// For license information, please see license.txt

frappe.query_reports["Consumption Report"] = {
	"filters": [
		{
			fieldname: "rental_unit",
			label: __("Rental Unit"),
			fieldtype: "Link",
			options: "Rental Units",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "property_type",
			label: __("Property Type"),
			fieldtype: "Select",
			options: ["Commercial, Warehouse, Office", "Town House Villas", "Labor Accommodation", "Retail Shops", "Commercial, Residential", "Commercial, Retail Shops", "Residential", "Commercial", "Warehouse", "Central Store"],
		},
		{
			fieldname: "owner_name",
			label: __("Owner Name"),
			fieldtype: "Link",
			options: "Owners and Landlords",
		},

	]
};
