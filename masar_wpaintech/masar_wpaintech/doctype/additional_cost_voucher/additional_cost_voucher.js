// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Additional Cost Voucher", {
    get_items_from_purchase_receipt: function(frm) {
        if (frm.doc.purchase_receipt){
            console.log("sgsgd");
            get_pr_items(frm);
        }
    }
});



function get_pr_items(frm){
    console.log("stdf");
    frappe.call({
        doc: frm.doc,
        method: "get_items_from_purchase_receipts",
        callback: function(r) {
            if (r.message){
                console.log("Success", r.message);
                refresh_field("items");
            }
        }
    });
}