frappe.ui.form.on('Quotation', {
	validate(frm) {
		let tax_template = frm.doc.taxes_and_charges;
		console.log(tax_template);

		for (let i = 0; i < frm.doc.items.length; i++) {
			let item = frm.doc.items[i];  

			if (tax_template === "Jordan Tax - WP") {
				item.item_tax_template = "Jordan Tax - WP";
			} else {
				item.item_tax_template = "Exapted - WP"; 
			}
		}

		frm.refresh_field("items");
	},
})