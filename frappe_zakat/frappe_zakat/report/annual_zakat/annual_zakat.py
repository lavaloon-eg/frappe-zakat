# Copyright (c) 2025, Lavaloon and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe import _


def execute(filters: dict = None) -> tuple:
	columns, data = [], []

	data = get_data(filters)
	columns = get_columns()
	return columns, data


def get_data(filters: dict) -> list:
	zakat_calculation = DocType("ZAKAT Calculation")
	company = DocType("Company")
	total_amount_eligible_for_zakat = (
		zakat_calculation.total_cash_amount
		+ zakat_calculation.total_gold_zakat_amount
		+ zakat_calculation.total_silver_amount
		+ zakat_calculation.amount_eligible_for_zakat
	)
	zakat_amount = (
		zakat_calculation.total_cash_zakat_amount
		+ zakat_calculation.total_gold_zakat_amount
		+ zakat_calculation.total_silver_zakat_amount
		+ zakat_calculation.business_assets_zakat_amount
	)

	query = (
		frappe.qb.from_(zakat_calculation)
		.select(zakat_calculation.company.as_("company_id"),
            company.company_name.as_("company_name"),
            zakat_calculation.start_fiscal_year.as_("fiscal_year"),
            zakat_calculation.current_24k_gold_price_for_1_gm.as_("gold_price"),
            zakat_calculation.nisab_threshold.as_("nisab_threshold"),
			total_amount_eligible_for_zakat.as_("total_amount_eligible_for_zakat"),
			zakat_amount.as_("total_zakat_amount"))
		.inner_join(company).on(zakat_calculation.company == company.name)
	)

	if filters.get("company"):
		query = query.where(zakat_calculation.company == filters.get("company"))
	if filters.get("fiscal_year"):
		query = query.where(zakat_calculation.start_fiscal_year == filters.get("fiscal_year"))

	data = query.run(as_dict=True)

	return data

def get_columns():
	columns = [
		{
			"fieldname": "company_name",
			"label": _("Company"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "fiscal_year",
			"label": _("Fiscal Year"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "gold_price",
			"label": _("Gold Price"),
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "nisab_threshold",
			"label": _("Nisab Threshold"),
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "total_amount_eligible_for_zakat",
			"label": _("Total Amount Eligible for Zakat"),
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "total_zakat_amount",
			"label": _("Total Zakat Amount"),
			"fieldtype": "Currency",
			"width": 200
		}
	]

	return columns