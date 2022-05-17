frappe.ui.form.on('Petty Cash Claim', {
	refresh(frm) {

	}
})



cur_frm.get_field("petty_cash_account").get_query = function(doc) {
	return {
		filters: {
			'company': doc.company
		}

	}
}




cur_frm.fields_dict["table_5"].grid.get_field("account").get_query = function(doc) {
	return {
		filters: {
			'company': doc.company
		}

	}
}