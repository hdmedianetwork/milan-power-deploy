from django.db import models
from shortuuidfield import ShortUUIDField

from userauth.models import User

request_status = (
    ('in_review', 'In Review'),
    ('accepted', 'Accepted'),
    ('checked', 'Checked'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded'),
    ('rejected', 'Rejected'),
)

urgency_status = (
    ('in_review', 'In Review'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)

message_type = (
    ('success', 'success'),
    ('warning', 'warning'),
    ('danger', 'danger'),
)
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user/{filename}'

# Create your models here.
class vendorTable(models.Model):
    vid = ShortUUIDField(unique=True, max_length=20)
    salesman_name = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    proprietor_name = models.CharField(max_length=100, default="Proprietor Name")
    company_name = models.CharField(max_length=100, default="Company Name")
    address = models.CharField(max_length=200, default="Address")
    phone_number = models.PositiveIntegerField()
    total_requests = models.PositiveIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True) 


class requestTable(models.Model):
    rid = ShortUUIDField(unique=True, max_length=20)
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    vid = models.ForeignKey(vendorTable, on_delete=models.CASCADE, null=False)
    refund_type = models.CharField(max_length=15)
    request_status = models.CharField(choices=request_status, max_length=15)
    uid = models.CharField(max_length=100, default="random")
    urgency_status = models.CharField(max_length=100, default="in_review")
    iid = models.CharField(max_length=100, default="random")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 


class requestRemarks(models.Model):
    mid = ShortUUIDField(unique=True, max_length=20)
    request_id = models.ForeignKey(requestTable, on_delete=models.CASCADE, null=False)
    remarks_salesman = models.CharField(max_length=250)
    remarks_receiver = models.CharField(max_length=250)
    remarks_checker = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True) 

class requestImages(models.Model):
    iid = ShortUUIDField(unique=True, max_length=20)
    request_id = models.ForeignKey(requestTable, on_delete=models.CASCADE, null=False)
    image_salesman = models.ImageField(upload_to = user_directory_path, default="product.jpg")
    image_checker_1 = models.ImageField(upload_to = user_directory_path, default="product.jpg")
    image_checker_2 = models.ImageField(upload_to = user_directory_path, default="product.jpg")
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True) 

class urgentRequestTable(models.Model):
    uid = ShortUUIDField(unique=True, max_length=20)
    rid = models.ForeignKey(requestTable, on_delete=models.CASCADE, null=False)
    urgency_reason = models.CharField(max_length=250)    
    urgency_status = models.CharField(choices=urgency_status, max_length=15)
    denial_reason = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True) 

class rejectedRequestTable(models.Model):
    rejid = ShortUUIDField(unique=True, max_length=20)
    rid = models.ForeignKey(requestTable, on_delete=models.CASCADE, null=False)
    rejected_by = models.CharField(max_length=250)
    rejection_reason = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True) 

class invoiceTable(models.Model):
    iid = ShortUUIDField(unique=True, max_length=20)
    rid = models.ForeignKey(requestTable, on_delete=models.CASCADE, null=False)
    invoice = models.ImageField(upload_to = user_directory_path, default="product.jpg")
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True) 

class requestNotificationTable(models.Model):
    nid = ShortUUIDField(unique=True, max_length=20)
    rid = models.ForeignKey(requestTable, on_delete=models.CASCADE, null=False)
    user = models.CharField(max_length=30, default='Email')
    notification_by = models.CharField(max_length=20)
    message = models.CharField(max_length=250)
    message_type = models.CharField(choices=message_type, max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
