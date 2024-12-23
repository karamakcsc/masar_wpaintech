///////// Calculation Fields /////////////////

frappe.ui.form.on("Purchase Order Item", {
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
        d.custom_no_cartron = flt(d.qty / d.custom_carton_capacity);
        frm.refresh_field("items");
    }
}

////////// Filter Fields //////////////////

frappe.ui.form.on('Purchase Order', {
    onload: function(frm) {
        freight_type_filter(frm);
        shipping_terms_filter(frm);
    },
    refresh: function(frm) {
        freight_type_filter(frm);
        shipping_terms_filter(frm);
    },
    setup: function(frm) {
        freight_type_filter(frm);
        shipping_terms_filter(frm);
    }
});

function freight_type_filter(frm) {
    frm.fields_dict['custom_freight_type'].get_query = function() {
        return {
            filters: {
                "disabled": 0
            }
        };
    };
}

function shipping_terms_filter(frm) {
    frm.fields_dict['custom_shipping_terms'].get_query = function() {
        return {
            filters: {
                "disabled": 0
            }
        };
    };
}
