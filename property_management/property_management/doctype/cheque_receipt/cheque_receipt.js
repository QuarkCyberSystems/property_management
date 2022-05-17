// Copyright (c) 2021, QCS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cheque Receipt', {
	// refresh: function(frm) {

	// }
});


cur_frm.fields_dict["cr_table"].grid.get_field("account").get_query = function(doc) {
	return {
		filters: {
			'company': doc.company
		}

	}
}