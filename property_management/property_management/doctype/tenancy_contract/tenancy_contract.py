# Copyright (c) 2021, QCS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TenancyContract(Document):
	def validate(self):
		if self.status == "Active":
			for item in self.rental_units_table:
				ru = frappe.get_doc("Rental Units", item.rental_units)
				ru.status = "Occupied"
				ru.save()
		if self.status == "Inactive":
			for item in self.rental_units_table:
				ru = frappe.get_doc("Rental Units", item.rental_units)
				ru.status = "Occupied"
				ru.save()
		#Adding the fist table item from rental units
		for item in self.rental_units_table:
			ru = frappe.get_doc("Rental Units", item.rental_units)
			self.location = ru.location
			self.property_no = ru.property_no
			self.premise_no = ru.premise_no
			self.property_size = ru.area
			self.plot_no = ru.plot_no
			self.property_type = ru.property_type		


