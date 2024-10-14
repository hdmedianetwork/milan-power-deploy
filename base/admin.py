from django.contrib import admin
from .models import vendorTable, requestTable, requestRemarks, requestImages, rejectedRequestTable, urgentRequestTable, invoiceTable, requestNotificationTable

# Register your models here.
class vendorTableAdmin(admin.ModelAdmin):
    list_display = ['vid', 'salesman_name', 'company_name', 'address', 'phone_number', 'total_requests']

class requestTableAdmin(admin.ModelAdmin):
    list_display = ['rid', 'raised_by', 'vid', 'refund_type', 'request_status','uid', 'urgency_status', 'iid']

class requestRemarksAdmin(admin.ModelAdmin):
    list_display = ['mid', 'request_id', 'remarks_salesman', 'remarks_receiver', 'remarks_checker']

class requestImagesAdmin(admin.ModelAdmin):
    list_display = ['iid', 'request_id', 'image_salesman', 'image_checker_1', 'image_checker_2']

class rejectedRequestAdmin(admin.ModelAdmin):
    list_display = ['rejid', 'rid', 'rejected_by', 'rejection_reason']

class urgentRequestAdmin(admin.ModelAdmin):
    list_display = ['uid', 'rid', 'urgency_reason', 'urgency_status', 'denial_reason']

class invoiceTableAdmin(admin.ModelAdmin):
    list_display = ['iid', 'rid', 'invoice']

class requestNotificationTableAdmin(admin.ModelAdmin):
    list_display = ['nid', 'rid', 'user', 'notification_by', 'message', 'message_type']

admin.site.register(vendorTable, vendorTableAdmin)
admin.site.register(requestTable, requestTableAdmin)
admin.site.register(requestRemarks, requestRemarksAdmin)
admin.site.register(requestImages, requestImagesAdmin)
admin.site.register(rejectedRequestTable, rejectedRequestAdmin) 
admin.site.register(urgentRequestTable, urgentRequestAdmin) 
admin.site.register(invoiceTable, invoiceTableAdmin)
admin.site.register(requestNotificationTable, requestNotificationTableAdmin)