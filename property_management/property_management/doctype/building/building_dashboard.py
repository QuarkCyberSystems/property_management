from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
        'fieldname': 'building_no',
		'transactions': [
			{
				'label': _('Rental'),
				'items': ['Rental Units']
			},
			{
				'label': _('Maintainance'),
				'items': ['Issue']
			},
			
						
			
		]
	}