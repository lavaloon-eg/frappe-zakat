# Copyright (c) 2025, amr ashraf and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ZakatGoldItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		equivalent_value_to_24k: DF.Float
		gold_amount: DF.Currency
		gold_karat: DF.Literal["24", "22", "21", "20", "18", "14", "12", "10"]
		grams: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		zakat_amount: DF.Currency
	# end: auto-generated types
	pass
