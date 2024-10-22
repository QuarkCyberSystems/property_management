// Copyright (c) 2024, QCS and contributors
// For license information, please see license.txt

frappe.query_reports["Tenancy Contract Expiring Report"] = {
	"filters": [
		{
			fieldname: "name",
			label: __("Tenancy Contract"),
			fieldtype: "Link",
			options: "Tenancy Contract",
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "building",
			label: __("Buildings"),
			fieldtype: "Link",
			options: "Building",
		},
	]
};
