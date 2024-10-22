// Copyright (c) 2024, QCS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Consumption", {
	refresh(frm) {
        if(frm.is_new()){
            frm.set_value("date", frappe.datetime.nowdate());
        }
	},
});
