from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
        'fieldname': 'tenancy_contract',
		'transactions': [
            {
				'label': _('Move Checklist'),
				'items': ['Move Checklist']
			},
			{
				'label': _('Cheque Receipt'),
				'items': ['Cheque Receipt']
			},
			{
				'label': _('Sales Invoice'),
				'items': ['Sales Invoice']
			},
			
						
			
		]
	}