// Copyright (c) 2025, Lavaloon and contributors
// For license information, please see license.txt

frappe.query_reports["Annual Zakat"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": "Company",
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 0
		},
		{
			"fieldname": "fiscal_year",
			"label": "Fiscal Year",
			"fieldtype": "Date",
			"reqd": 0
		}
	]
};
