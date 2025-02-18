# import frappe


# def validate(self, method):
#     calc_landed_cost(self)


# def calc_landed_cost(self):
#     if self.custom_include_additional_charges:
#         pr_no = None
#         for pr in self.purchase_receipts:
#             pr_no = pr.receipt_document
#             break
            
#         # Fetch previous landed cost from PR
#         if pr_no:    
#             pr_sql = frappe.db.sql("""
#                     SELECT 
#                         tpri.item_code AS `item_code`, tpri.landed_cost_voucher_amount AS `landed_cost_amount`, tpri.base_amount AS `amount`
#                     FROM 
#                         `tabPurchase Receipt Item` tpri
#                     WHERE 
#                         tpri.parent = %s
#                 """,(pr_no,), as_dict=True)
        
#         pr_items_map = {row["item_code"]: row for row in pr_sql}
        
#         # frappe.throw(str(pr_item_map))
#         for item in self.items:     ##### Update Amount 
#             if item.item_code in pr_items_map:
#                 item.amount = 0
#                 pr_item = pr_items_map[item.item_code]
#                 item.amount = pr_item["amount"] + pr_item["landed_cost_amount"]
#                 # item.amount = row.amount + row.landed_cost_amount
            
