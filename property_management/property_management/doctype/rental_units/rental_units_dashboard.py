from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
        'fieldname': 'rental_units',
		'transactions': [
			{
				'label': _('Contracts'),
				'items': ['Tenancy Contract']
			},
			{
				'label': _('Maintainance'),
				'items': ['Issue']
			},
			
						
			
		]
	}