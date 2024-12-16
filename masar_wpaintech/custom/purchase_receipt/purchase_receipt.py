import frappe


@frappe.whitelist()
def calc_landed_cost(name):
    self = frappe.get_doc("Purchase Receipt", name)
    landed_cost_total = 0
    if len(self.items) != 0:
        for item in self.items:
            if item.landed_cost_voucher_amount:
                landed_cost_total += item.landed_cost_voucher_amount

    frappe.db.set_value("Purchase Receipt", name, "custom_total_landed_cost_amount", landed_cost_total)
    frappe.db.commit()
    return True
###
###