import frappe


def validate(self, method):
    calc_landed_cost(self)
    validate_percentage(self)


def calc_landed_cost(self):
    if self.custom_include_additional_charges:
        pr_no = None
        for pr in self.purchase_receipts:
            pr_no = pr.receipt_document
            break
            
        # Fetch previous landed cost from PR
        if pr_no:    
            pr_sql = frappe.db.sql("""
                    SELECT 
                        tpri.item_code AS `item_code`, tpri.landed_cost_voucher_amount AS `landed_cost_amount`, tpri.base_amount AS `amount`
                    FROM 
                        `tabPurchase Receipt Item` tpri
                    WHERE 
                        tpri.parent = %s
                """,(pr_no,), as_dict=True)
        
        pr_items_map = {row["item_code"]: row for row in pr_sql}
        
        # frappe.throw(str(pr_item_map))
        for item in self.items:     ##### Update Amount 
            if item.item_code in pr_items_map:
                item.amount = 0
                pr_item = pr_items_map[item.item_code]
                item.amount = pr_item["amount"] + pr_item["landed_cost_amount"]
                # item.amount = row.amount + row.landed_cost_amount
            
        if len(self.taxes) != 0 and self.custom_include_percentage: ### Calculate applicable charges based on percentage
            for item in self.items:
                if item.custom_percentage:
                    item.applicable_charges = (item.custom_percentage / 100) * self.total_taxes_and_charges
                    
def validate_percentage(self):
    if self.custom_include_percentage:
        total_percentage = 0
        for item in self.items:
            total_percentage += item.custom_percentage
        if total_percentage != 100:
            frappe.throw(f"Total percentage must be exactly 100%. Current total: {total_percentage}%")