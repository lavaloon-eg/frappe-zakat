# Copyright (c) 2025, amr ashraf and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ZAKATCalculation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from frappe_zakat.frappe_zakat.doctype.zakat_gold_item.zakat_gold_item import ZakatGoldItem

		amount_eligible_for_zakat: DF.Currency
		business_assets_zakat_amount: DF.Currency
		company: DF.Link
		current_24k_gold_price_for_1_gm: DF.Currency
		current_silver_price_for_1_gm: DF.Currency
		end_fiscal_year: DF.Date
		gold_holdings: DF.Table[ZakatGoldItem]
		inventory_value: DF.Currency
		liabilities: DF.Currency
		nisab_threshold: DF.Currency
		receivables: DF.Currency
		start_fiscal_year: DF.Date
		total_cash_amount: DF.Currency
		total_gold_zakat_amount: DF.Currency
		total_silver_amount: DF.Currency
		total_silver_grams: DF.Float
		total_silver_zakat_amount: DF.Currency
		total_zakat_amount: DF.Currency
	# end: auto-generated types
	pass
