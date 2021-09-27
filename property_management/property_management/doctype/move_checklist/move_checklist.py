# Copyright (c) 2021, QCS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class MoveChecklist(Document):
	def validate(self):
		self.total = 0
		for item in self.get("check"):
			self.total += item.cost

	
