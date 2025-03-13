import frappe
import json


@frappe.whitelist()
def get_remark(self):
    self = json.loads(self)
    
    if self['user_remark']:
        return self['user_remark']