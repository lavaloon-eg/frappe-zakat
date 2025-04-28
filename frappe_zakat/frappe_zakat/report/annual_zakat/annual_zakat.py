# Copyright (c) 2025, Lavaloon and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.utils import fmt_money
from frappe import _
from pypika.terms import Case


def execute(filters: dict = None) -> tuple:
	columns, data = [], []

	data = get_data(filters)
	columns = get_columns()
	summary = get_summary(data)
	return columns, data, None, None, summary


def get_data(filters: dict) -> list:
	zakat_calculation = DocType("ZAKAT Calculation")
	company = DocType("Company")
	cash_case = (
		Case()
		.when(zakat_calculation.total_cash_zakat_amount > 0, zakat_calculation.total_cash_amount)
		.else_(0)
	)

	gold_case = (
		Case()
		.when(zakat_calculation.total_gold_zakat_amount > 0, zakat_calculation.total_gold_amount_eligible_for_zakat)
		.else_(0)
	)

	silver_case = (
		Case()
		.when(zakat_calculation.total_silver_zakat_amount > 0, zakat_calculation.total_silver_amount)
		.else_(0)
	)

	business_assets_case = (
		Case()
		.when(zakat_calculation.business_assets_zakat_amount > 0, zakat_calculation.amount_eligible_for_zakat)
		.else_(0)
	)

	total_amount_eligible_for_zakat = cash_case + gold_case + silver_case + business_assets_case

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
            cash_case,
            gold_case,
            silver_case,
            business_assets_case,
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

def get_summary(data):
    if not data:
        return [
            {
				"label": _("Total Zakat Amount"),
                "value": fmt_money(0.0)
			},
            {
				"label": _("Total Amount Eligible for Zakat"),
                "value": fmt_money(0.0)
			},
            {
				"label": _("Average Gold Price"),
                "value": fmt_money(0.0)
			},
            {
				"label": _("Average Nisab Threshold"),
                "value": fmt_money(0.0)
			},
        ]

    total_zakat_amount = sum(d.get("total_zakat_amount", 0) for d in data)
    total_amount_eligible_for_zakat = sum(d.get("total_amount_eligible_for_zakat", 0) for d in data)
    avg_gold_price = sum(d.get("gold_price", 0) for d in data) / len(data)
    avg_nisab = sum(d.get("nisab_threshold", 0) for d in data) / len(data)

    return [
        {
			"label": _("Total Zakat Amount"),
            "value": fmt_money(total_zakat_amount)
		},
        {
			"label": _("Total Amount Eligible for Zakat"),
            "value": fmt_money(total_amount_eligible_for_zakat)
		},
        {
			"label": _("Average Gold Price"),
            "value": fmt_money(avg_gold_price)
		},
        {
			"label": _("Average Nisab Threshold"),
            "value": fmt_money(avg_nisab)
		},
    ]
