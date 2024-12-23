///////// Calculation Fields /////////////////

frappe.ui.form.on("Purchase Receipt", {
    onload: function(frm) {
        calculate_all_items(frm);
        calc_total_landed_cost(frm);
    }
    // before_save: function(frm) {
    //     calculate_all_items(frm);
    // },
});

function calculate_all_items(frm) {
    frm.doc.items.forEach(row => {
        calc_rate_per_unit(frm, row.doctype, row.name);
        calc_carton_capacity(frm, row.doctype, row.name);
    });
    frm.refresh_field("items");
}

function calc_rate_per_unit(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.item_code) {
        var uomNumericValue;
        if (d.uom.toLowerCase() === "lt" || d.uom.toLowerCase() === "kg" || d.uom.toLowerCase() === "gallon") {
            uomNumericValue = 1; // Set a default value for "LT" if needed
        } else {
            var match = d.uom.match(/\d+(\.\d+)?/);
            uomNumericValue = match ? parseFloat(match[0]) : NaN;
        }

        if (!isNaN(uomNumericValue)) {
            d.custom_rate_per_unit = flt(d.rate / uomNumericValue);
        } else {
            d.custom_rate_per_unit = flt(d.rate);
        }
    }
}

function calc_carton_capacity(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.item_code && d.custom_carton_capacity) {
        no_carton = flt(d.qty / d.custom_carton_capacity);
        d.custom_no_carton = flt(d.qty / d.custom_carton_capacity);
        frm.refresh_field("items");
    }
}

function calc_total_landed_cost(frm) {
    let total_landed_cost = 0;

    frm.doc.items.forEach(row => {
        if (row.landed_cost_voucher_amount) {
            total_landed_cost += flt(row.landed_cost_voucher_amount);
        }
    });

    if (total_landed_cost > 0) {
        frappe.call({
            method: "masar_wpaintech.custom.purchase_receipt.purchase_receipt.calc_landed_cost",
            args: {
                name: frm.doc.name,

            },
            callback: function(r) {
                if (r.message) {
                    frm.refresh_field("custom_total_landed_cost_amount");
                }
            }
        })
    }
}
