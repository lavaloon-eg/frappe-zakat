# Copyright (c) 2025, amr ashraf and contributors
# For license information, please see license.txt

import frappe
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
		total_cash_zakat_amount: DF.Currency
		total_gold_zakat_amount: DF.Currency
		total_silver_amount: DF.Currency
		total_silver_grams: DF.Float
		total_silver_zakat_amount: DF.Currency
		total_zakat_amount_for_each_entered_type: DF.TextEditor | None
	# end: auto-generated types
	pass

	@staticmethod
	def get_html_table_view(amounts_dict: dict) -> str:
		total_amount_eligible_for_zakat = 0
		total_zakat_amount = 0
		table = (f"""
			<table>
			<tr>
			<th>Zakat Type</th>
			<th>Amount Eligible for Zakat</th>
			<th>Zakat Amount</th>
			</tr>
			""")
		for key, value in amounts_dict.items():
			zakat_type = " ".join([w.capitalize() for w in key.split("_")])
			amount = frappe.format(value['amount'], {'fieldtype': 'Currency'})
			zakat_amount = frappe.format(value['zakat_amount'], {'fieldtype': 'Currency'}) 
			if value['zakat_amount']:
				total_amount_eligible_for_zakat += value['amount']
				total_zakat_amount += value['zakat_amount']
				table += f"""
					<tr>
					<td>{zakat_type}</td>
					<td>{amount}</td>
					<td>{zakat_amount}</td>
					</tr>
					"""
		table += f"""
			<tr>
			<th>Total</th>
			<th>{frappe.format(total_amount_eligible_for_zakat, {'fieldtype': 'Currency'})}</th>
			<th>{frappe.format(total_zakat_amount, {'fieldtype': 'Currency'})}</th>
			</tr>
			</table>
			"""
		return table

	def validate(self):
		self.validate_fiscal_year()

	def on_update(self):
		self.set_nisab_threshold()
		self.set_cash_and_bank_zakat_amounts()
		self.set_total_gold_zakat_amount()
		self.set_total_silver_zakat_amount()
		self.set_total_business_assets_zakat_amount()
		self.generate_total_zakat_amount_table()

	def validate_fiscal_year(self):
		if self.start_fiscal_year >= self.end_fiscal_year:
			frappe.throw("Start Fiscal Year should be less than End Fiscal Year.")

	def set_nisab_threshold(self):
		if self.current_24k_gold_price_for_1_gm:
			self.nisab_threshold = 85 * self.current_24k_gold_price_for_1_gm
		else:
			frappe.throw("Current Gold Price is not set in Settings.")

	def set_cash_and_bank_zakat_amounts(self):
		if self.total_cash_amount > self.nisab_threshold:
			self.total_cash_zakat_amount = self.total_cash_amount * 0.025
		else:
			self.total_cash_zakat_amount = 0

	def set_total_gold_zakat_amount(self):
		total_gold_amount = 0
		for gold in self.gold_holdings:
			if gold.grams:
				gold.equivalent_value_to_24k = gold.grams * (
					int(gold.gold_karat) / 24)
				gold.gold_amount = gold.equivalent_value_to_24k * self.current_24k_gold_price_for_1_gm
				if gold.gold_amount > self.nisab_threshold:
					gold.zakat_amount = gold.gold_amount * 0.025
					total_gold_amount += gold.zakat_amount
				else:
					gold.zakat_amount = 0

		self.total_gold_zakat_amount = total_gold_amount

	def set_total_silver_zakat_amount(self):
		if self.total_silver_grams:
			self.total_silver_amount = self.total_silver_grams * self.current_silver_price_for_1_gm
			if self.total_silver_amount > self.nisab_threshold:
				self.total_silver_zakat_amount = self.total_silver_amount * 0.025
			else:
				self.total_silver_zakat_amount = 0

	def set_total_business_assets_zakat_amount(self):
		self.amount_eligible_for_zakat = (
			self.inventory_value
			+ self.receivables
			- self.liabilities
		)

		if self.amount_eligible_for_zakat < 0:
			frappe.throw("Inventory Value, Receivables, and Liabilities cannot be negative.")

		if self.amount_eligible_for_zakat > self.nisab_threshold:
			self.business_assets_zakat_amount = self.amount_eligible_for_zakat * 0.025
		else:
			self.business_assets_zakat_amount = 0

	def generate_total_zakat_amount_table(self):
		amounts_dict = {
			"cash": {
				"amount": self.total_cash_amount,
				"zakat_amount": self.total_cash_zakat_amount
			},
			"gold": {
				"amount": self.total_gold_zakat_amount,
				"zakat_amount": self.total_gold_zakat_amount
			},
			"silver": {
				"amount": self.total_silver_amount,
				"zakat_amount": self.total_silver_zakat_amount
			},
			"business_assets": {
				"amount": self.amount_eligible_for_zakat,
				"zakat_amount": self.business_assets_zakat_amount
			}
		}

		self.total_zakat_amount_for_each_entered_type = self.get_html_table_view(amounts_dict)
