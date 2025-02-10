// frappe.ui.form.on("Landed Cost Voucher", {
//     validate: function(frm) {
//         if (frm.doc.custom_include_additional_charges){
//             calcLandedCost(frm);
//         }
//     }
// });



// function calcLandedCost(frm) {
//     // var receipt_doc = null
//     // frm.doc.purchase_receipts.forEach(row => {
//     //     receipt_doc = row.receipt_document
//     // });
//     // console.log(receipt_doc);
//     // let total_amount = 0;
//     // frappe.call({
//     //     method: "masar_wpaintech.custom.landed_cost_voucher.landed_cost_voucher.calc_landed_cost",
//     //     args: {
//     //         pr_no: receipt_doc
//     //     },
//     //     callback: function (r) {
//     //         console.log(r.message);
//     //         r.message.forEach(item => {
//     //             total_amount += flt(item.landed_cost_amount);
//     //             console.log(total_amount);
//     //         });
//     //     }
//     // })
//     // console.log(total_amount);
// }