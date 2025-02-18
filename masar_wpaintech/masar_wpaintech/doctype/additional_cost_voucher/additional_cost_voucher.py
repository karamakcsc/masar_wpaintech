# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class AdditionalCostVoucher(Document):
    def on_submit(self):
        self.create_lc()

    def validate(self):
        self.calc_cnf_customs()

    def calc_cnf_customs(self):
        total_charges = 0
        total_cnf = 0
        total_cost = 0
        shipping_cost = self.shipping_charges if self.shipping_charges else None

        for char in self.charges:
            total_charges += char.amount

        self.total_charges = total_charges + shipping_cost if shipping_cost else total_charges

        for item in self.items:
            tariff_rate = item.customs_percentage if item.customs_percentage else None

            if self.shipping_terms in ["EXW", "FOB"] and shipping_cost:
                item.cnf = (shipping_cost / self.purchase_receipt_total) * item.rate + item.rate
            else:
                item.cnf = item.rate

            if shipping_cost and tariff_rate:
                item.total_cost = (total_charges / (self.purchase_receipt_total + shipping_cost) + (tariff_rate / 100)) * item.cnf + item.cnf
            elif shipping_cost and not tariff_rate:
                item.total_cost = (total_charges / (self.purchase_receipt_total + shipping_cost)) * item.cnf + item.cnf
            elif tariff_rate and not shipping_cost:
                item.total_cost = (tariff_rate / 100) * item.cnf + item.cnf
            elif not shipping_cost and not tariff_rate:
                item.total_cost = (total_charges / (self.purchase_receipt_total)) * item.cnf + item.cnf

            item.total_amount = item.qty * item.total_cost
            total_cost += item.total_cost
            total_cnf += item.cnf
            item.applicable_charges = item.total_amount - item.amount

        # self.total_cost = total_cost
        # self.total_cnf = total_cnf
        
    def create_lc(self):
        new_lc = frappe.new_doc("Landed Cost Voucher")        
        new_lc.append("purchase_receipts", {
            "receipt_document_type": "Purchase Receipt",
            "receipt_document": self.purchase_receipt,
            "custom_reference_number": self.reference_no,
            "grand_total": self.purchase_receipt_total,
            "supplier": self.supplier
        })
        
        new_lc.distribute_charges_based_on = "Distribute Manually"
        
        total_charge_amount = 0
        combined_description = []

        for charge in self.charges:
            # total_charge_amount += charge.amount
            combined_description.append(charge.description)

        total_applicable_charges = sum(flt(d.applicable_charges) for d in self.get("items"))
            
        new_lc.append("taxes", {
            "expense_account": self.charges[0].expense_account if self.charges else "",
            "description": "All Charges",
            "amount": total_applicable_charges
        })
        
        for item in self.items:
            new_lc.append("items", {
                "item_code": item.item_code,
                "description": item.description,
                "qty": item.qty,
                "rate": item.rate,
                "amount": item.amount,
                "custom_cnf": item.cnf,
                "custom_percentage": item.customs_percentage,
                "custom_total_cost": item.total_cost,
                "custom_total_amount": item.total_amount,
                "applicable_charges": item.applicable_charges,
                "receipt_document_type": "Purchase Receipt",
                "receipt_document": self.purchase_receipt,
                "cost_center": "Main - WP",
                "purchase_receipt_item": item.purchase_receipt_item
            })
        
        # total_applicable_charges = sum(flt(d.applicable_charges) for d in self.get("items"))
        
        # new_lc.total_taxes_and_charges = total_applicable_charges
        
        new_lc.save()
        new_lc.submit()

    @frappe.whitelist()
    def get_items_from_purchase_receipts(self):
        self.set("items", [])
        pr_items = get_pr_items(self.purchase_receipt)

        for d in pr_items:
            item = self.append("items")
            item.item_code = d.item_code
            item.description = d.description
            item.qty = d.qty
            item.rate = d.base_rate
            item.amount = d.base_amount
            item.purchase_receipt_item = d.name

        return 1

def get_pr_items(purchase_receipt):
    item = frappe.qb.DocType("Item")
    pr_item = frappe.qb.DocType("Purchase Receipt Item")
    return (
        frappe.qb.from_(pr_item)
        .inner_join(item)
        .on(item.name == pr_item.item_code)
        .select(
            pr_item.item_code,
            pr_item.description,
            pr_item.qty,
            pr_item.base_rate,
            pr_item.base_amount,
            pr_item.name,
        )
        .where(
            (pr_item.parent == purchase_receipt)
            & ((item.is_stock_item == 1) | (item.is_fixed_asset == 1))
        )
        .run(as_dict=True)
    )
