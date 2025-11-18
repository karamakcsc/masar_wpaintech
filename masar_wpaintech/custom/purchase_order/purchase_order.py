import frappe


def validate(self, method):
    clear_tax(self)
    

def clear_tax(self):
    for item in self.items:
        item.item_tax_template = None

    self.taxes_and_charges = None
    self.taxes = []
    self.run_method("calculate_taxes_and_totals")
