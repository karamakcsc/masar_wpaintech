///////// Calculation Fields /////////////////

frappe.ui.form.on("Purchase Receipt Item", {
    qty: function(frm, cdt, cdn) {
        calc_carton_capacity(frm, cdt, cdn);
        calc_rate_per_unit(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calc_carton_capacity(frm, cdt, cdn);
        calc_rate_per_unit(frm, cdt, cdn);
    },
    uom: function(frm, cdt, cdn) {
        calc_carton_capacity(frm, cdt, cdn);
        calc_rate_per_unit(frm, cdt, cdn);
    }
});

frappe.ui.form.on("Purchase Receipt", {
    onload: function(frm) {
        calculate_all_items(frm);
        calc_total_landed_cost(frm);
    },
    refresh: function(frm) {
        calculate_all_items(frm);
        calc_total_landed_cost(frm);
    },
    before_save: function(frm) {
        calculate_all_items(frm);
    },
});

function calculate_all_items(frm) {
    frm.doc.items.forEach(row => {
        fetch_carton_capacity(frm, row);
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
            frm.refresh_field("items");
        } else {
            d.custom_rate_per_unit = flt(d.rate);
            frm.refresh_field("items");
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
                    console.log(r.message);
                    frm.refresh_field("custom_total_landed_cost_amount");
                }
            }
        })
    }
}

/////////// Fetching Data /////////////////

frappe.ui.form.on('Purchase Receipt', {
    refresh: function(frm) {
        frm.fields_dict['items'].grid.wrapper.on('grid-row-render', function(e, grid_row) {
            var doc = grid_row.doc;
            fetch_carton_capacity(frm, doc);
        });
    },
});



frappe.ui.form.on('Purchase Receipt Item', {
    item_code: function(frm, cdt, cdn) {
        var doc = locals[cdt][cdn];
        fetch_carton_capacity(frm, doc);
    }
});

function fetch_carton_capacity(frm, doc) {
    if (doc.item_code) {
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Item',
                filters: { 'item_code': doc.item_code },
                fieldname: 'custom_carton_capacity'
            },
            callback: function(r) {
                if (r.message && r.message.custom_carton_capacity) {
                    frappe.model.set_value(doc.doctype, doc.name, 'custom_carton_capacity', r.message.custom_carton_capacity);
                    calc_carton_capacity(frm, doc.doctype, doc.name);
                }
            }
        });
    }
}