/////////////Calculation Fields/////////////////Start Code
frappe.ui.form.on("Purchase Order Item", {
    qty: function(frm, cdt, cdn) {
      updateCalculations(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
      updateCalculations(frm, cdt, cdn);
    },
    uom: function(frm, cdt, cdn) {
      updateCalculations(frm, cdt, cdn);
    }
  });
  
  function updateCalculations(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    calc_rate_per_unit(d);
    calc_carton_capacity(d);
    cur_frm.refresh_fields();
  }
  
  function calc_rate_per_unit(d) {
    if (d.item_code) {
      var uomNumericValue = getUomNumericValue(d.uom);
      if (!isNaN(uomNumericValue)) {
        d.custom_rate_per_unit = flt(d.rate / uomNumericValue);
      } else {
        frappe.msgprint(__("Invalid numeric value in UOM"));
      }
    }
  }
  
  function getUomNumericValue(uom) {
    var uomLower = uom.toLowerCase();
    if (["lt", "kg", "gallon"].includes(uomLower)) {
      return 1; // Default value for these UOMs
    } else {
      var match = uom.match(/\d+(\.\d+)?/);
      return match ? parseFloat(match[0]) : NaN;
    }
  }
  
  function calc_carton_capacity(d) {
    if (d.item_code && d.custom_carton_capacity) {
      d.custom_no_cartron = flt(d.qty / d.custom_carton_capacity);
    }
  }
  /////////////Calculation Fields/////////////////End Code
  
  /////////////Fetching Data/////////////////Start Code
  frappe.ui.form.on('Purchase Order', {
    refresh: function(frm) {
      frm.fields_dict['items'].grid.on('add', function(doc) {
        fetch_carton_capacity(doc);
      });
    }
  });
  
  frappe.ui.form.on('Purchase Order Item', {
    item_code: function(frm, cdt, cdn) {
      fetch_carton_capacity(locals[cdt][cdn]);
    }
  });
  
  function fetch_carton_capacity(doc) {
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
  