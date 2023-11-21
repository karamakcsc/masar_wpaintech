frappe.ui.form.on("Purchase Order Item", {
  qty: function(frm, cdt, cdn) {
    calculateCustomRatePerUnit(frm, cdt, cdn);
  },
  rate: function(frm, cdt, cdn) {
    calculateCustomRatePerUnit(frm, cdt, cdn);
  },
  uom: function(frm, cdt, cdn) {
    calculateCustomRatePerUnit(frm, cdt, cdn);
  }
});

function calculateCustomRatePerUnit(frm, cdt, cdn) {
  var d = locals[cdt][cdn];
  if (d.item_code) {
    var uomNumericValue;
    if (d.uom.toLowerCase() === "lt" || d.uom.toLowerCase() === "kg" || d.uom.toLowerCase() === "gallon" ) {
      uomNumericValue = 1; // Set a default value for "LT" if needed
    } else {
      uomNumericValue = parseFloat(d.uom.match(/\d+(\.\d+)?/)[0]);
    }

    if (!isNaN(uomNumericValue)) {
      d.custom_rate_per_unit = flt(d.rate / uomNumericValue);
      cur_frm.refresh_field("custom_rate_per_unit");
    } else {
      frappe.msgprint(__("Invalid numeric value in UOM"));
    }
  }
}
