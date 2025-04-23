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
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "company_name" && data && data.company_id) {
			value = `<a href="/app/company/${data.company_id}" 
				data-doctype="Company" 
				data-name="${data.company_id}" 
				data-value="${data.company_id}">${value}</a>`;
		}

		return value;
	}
};
