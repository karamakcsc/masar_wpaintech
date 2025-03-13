frappe.ui.form.on("Journal Entry", {
    validate: function(frm, cdt, cdn) {
        console.log("Test");
        var d = locals[cdt][cdn];
        frappe.call({
            method: "masar_wpaintech.custom.journal_entry.journal_entry.get_remark",
            args: {
                self: frm.doc
            },
            callback: function(r) {
                if (r.message) {
                    console.log("Message", r.message);
                    d.user_remark = r.message;
                    d.refresh_field("user_remark");
                }
            }
        })
    }
});//