/////////////Calculation Fields/////////////////Start Code
frappe.ui.form.on("Purchase Order Item", {
  qty: function(frm, cdt, cdn) {
      calc_rate_per_unit(frm, cdt, cdn);
      calc_carton_capacity(frm, cdt, cdn);
  },
  rate: function(frm, cdt, cdn) {
      calc_rate_per_unit(frm, cdt, cdn);
      calc_carton_capacity(frm, cdt, cdn);
  },
  uom: function(frm, cdt, cdn) {
      calc_rate_per_unit(frm, cdt, cdn);
      calc_carton_capacity(frm, cdt, cdn);
  }
});

function calc_rate_per_unit(frm, cdt, cdn) {
  var d = locals[cdt][cdn];
  if (d.item_code) {
      var uomNumericValue;
      if (d.uom.toLowerCase() === "lt" || d.uom.toLowerCase() === "kg" || d.uom.toLowerCase() === "gallon") {
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

function calc_carton_capacity(frm, cdt, cdn) {
  var d = locals[cdt][cdn];
  if (d.item_code && d.custom_carton_capacity) {
      d.custom_no_cartron = flt(d.qty / d.custom_carton_capacity);
      cur_frm.refresh_field("custom_no_cartron");
  }
}

/////////////Calculation Fields/////////////////End Code

/////////////Fetching Data/////////////////Start Code
frappe.ui.form.on('Purchase Order', {
  refresh: function(frm) {
      frm.fields_dict['items'].grid.on('add', function(doc) {
          fetch_carton_capacity(frm, doc);
      });
  }
});

frappe.ui.form.on('Purchase Order Item', {
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
              }
          }
      });
  }
}

/////////////Fetching Data/////////////////End Code