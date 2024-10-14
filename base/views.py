from django.shortcuts import render, redirect
from userauth.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import vendorTable, requestTable, requestRemarks, requestImages, urgentRequestTable, rejectedRequestTable, invoiceTable, requestNotificationTable
from django.http.response import HttpResponse
from django.db.models import Q
from userauth.models import User
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your views here.
def home(request):
    if request.user.is_authenticated == False:
        return redirect('userLogin')
    
    if(request.user.role == 'salesman'):
        return redirect('salesman_dashboard')
    
    elif(request.user.role == 'receiver'):
        return redirect('receiver_dashboard')  
    
    elif(request.user.role == 'checker'):
        return redirect('checker_dashboard')  
    
    elif(request.user.role == 'accountant'):
        return redirect('accountant_dashboard') 
    
    else:
        return redirect('admin_dashboard') 
    
    return render(request, 'salesman_board.html')


def userRegistration(request):

    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(f"Form {form}")
        if form.is_valid():
            print("True")
            new_user = form.save(commit=False)
            role = form.cleaned_data['role'] 
            new_user.role = role
            new_user.save() 
            username = form.cleaned_data['username']
            new_user = authenticate(username = form.cleaned_data['email'],
                                    password = form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('home')
        else:
            messages.error(request, 'Some error')

    context = {
        'page': 'register',
        'form': form,
    }


    return render(request, 'auth.html', context)

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
            messages.success(request, user)

        except Exception as e:
            messages.error(request, 'User doesn\'t exist.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('home')
        
        else:
            messages.error(request, "No such user exits.")
    
    return render(request, 'auth.html')


def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url=userLogin)
def addNotification(request, rid, message, message_type):
    new_notificaation = requestNotificationTable(
        rid = rid,
        notification_by = request.user.username + f'({request.user.role})',
        user = request.user.email,
        message = message,
        message_type = message_type,
    )
    new_notificaation.save()
    return True

@login_required(login_url=userLogin)
def viewNotifications(request):
    notification_object = requestNotificationTable.objects.filter(user = request.user.email).order_by('created').select_related('rid')
    page_object = universal_pagination(request, notification_object)

    context = {
        'requests': page_object
    }

    return render(request, 'notification_table.html', context)

@login_required(login_url=userLogin)
def salesman_dashboard(request):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')

    t_vendors = vendorTable.objects.filter(salesman_name = request.user)
    total_vendors = t_vendors.count()

    t_requests = requestTable.objects.filter(raised_by=request.user)
    total_requests = t_requests.count()

    a_requests = requestTable.objects.filter((Q(request_status='checked') | Q(request_status='accepted')) & Q(raised_by=request.user))
    active_requests = a_requests.count()

    u_requests = requestTable.objects.filter(Q(raised_by=request.user))
    urgent_requests = u_requests.count()

    au_requests = requestTable.objects.filter(Q(urgency_status = 'accepted') & Q(raised_by=request.user))
    accepted_urgent_requests = au_requests.count()

    c_requests = requestTable.objects.filter(Q(request_status = 'refunded') & Q(raised_by=request.user))
    completed_requests = c_requests.count()

    context = {
        'vendors': t_vendors,
        'total_vendors': total_vendors,
        'total_requests': total_requests,
        'active_requests': active_requests,
        'urgent_requests': urgent_requests,
        'completed_requests': completed_requests,
        'accepted_urgent_requests': accepted_urgent_requests,
    }

    return render(request, 'salesman_board.html', context)

def universal_pagination(request, query_name):
    paginator = Paginator(query_name, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return page_object

@login_required(login_url=userLogin)
def viewVendors(request):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    vendors = vendorTable.objects.filter(salesman_name = request.user)
    page_object = universal_pagination(request, vendors)

    context = {
        'vendors': page_object
    }

    return render(request, 'vendor_data.html', context)


@login_required(login_url=userLogin)
def addParty(request):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    if request.method == 'POST':
        proprietor_name = request.POST.get('proprietor_name')
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        phone_number = request.POST.get('phone_number')

        new_vendor = vendorTable(salesman_name = request.user, 
                                 proprietor_name = proprietor_name, 
                                 company_name = company_name,
                                 address = company_address, 
                                 phone_number = phone_number)
        
        new_vendor.save()
        text = f'Party Added: {proprietor_name}'
        messages.success(request, text)
        

        return render(request, 'add_party.html')

    return render(request, 'add_party.html')

@login_required(login_url=userLogin)
def deleteParty(request):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    if request.method == 'POST': 
        vendorIds = request.POST.get('vendorIds')
        vendorIds = vendorIds.split(',')
        
        for item in vendorIds:
            deleteQuery = vendorTable.objects.get(vid = item)
            deleteQuery.delete()

        return HttpResponse('Data Deleted')

    return render(request, 'viewVendors')

@login_required(login_url=userLogin)
def addRequest(request):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    vendors = vendorTable.objects.filter(salesman_name = request.user)

    context = {
        'vendors': vendors,
    }

    if request.method == 'POST':
        vendor_id = request.POST.get('vendor_id')
        refund_type = request.POST.get('refund_type')
        salesman_remarks = request.POST.get('salesman_remarks')
        image_salesman = request.FILES['image_salesman'] 

        # Get VEndor Instance
        vendor_instance = vendorTable.objects.get(vid = vendor_id)

        # Save in Request Table
        new_request = requestTable(
            raised_by = request.user, 
            vid =  vendor_instance, 
            refund_type = refund_type,
            request_status = 'pending',
            )
        
        new_request.save()

        # Get Request Instance
        request_instance = requestTable.objects.get(rid = new_request.rid)

        # Save in Remarks Table
        new_remark = requestRemarks(
            request_id = request_instance,
            remarks_salesman = salesman_remarks,
        )

        new_remark.save()

        new_image = requestImages(
            request_id = request_instance,
            image_salesman = image_salesman,
        )

        new_image.save()

        context['message'] = f'Request Raised Successfully!'

        addNotification(request, request_instance, 'Request Raised Successfully', 'success')

        return render(request, 'add_request.html', context)
        
    return render(request, 'add_request.html', context)

@login_required(login_url=userLogin)
def viewRequests(request):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    requests = requestTable.objects.filter(raised_by=request.user).select_related('vid')
    page_object = universal_pagination(request, requests)

    context = {
        'requests': page_object, 
    }

    return render(request, 'request_data.html', context)

@login_required(login_url=userLogin)
def viewActiveRequests(request):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    a_requests = requestTable.objects.filter((Q(request_status='checked') | Q(request_status='accepted')) & Q(raised_by = request.user))
    page_object = universal_pagination(request, a_requests)

    context = { 
        'requests':page_object, 
    }

    return render(request, 'request_data.html', context)

@login_required(login_url=userLogin)
def deleteRequests(request):
    if request.method == 'POST': 
        requestIds = request.POST.get('requestIds')
        requestIds = requestIds.split(',')
        print(requestIds)
        
        for item in requestIds:
            deleteQuery = requestTable.objects.get(rid = item)
            addNotification(request, deleteQuery, 'Request Deleted Successfully', 'danger')
            deleteQuery.delete()

        return HttpResponse('Data Deleted')

    return render(request, 'viewRequests')

@login_required(login_url=userLogin)
def viewSingleRequest(request, rid):
    
    single_request = requestTable.objects.filter(rid=rid).first()
    request_object = requestTable.objects.get(rid = rid)
    remark_object = requestRemarks.objects.get(request_id = request_object)
    image_object = requestImages.objects.get(request_id = request_object)

    salesman_remark = remark_object.remarks_salesman
    salesman_image = image_object.image_salesman

    print(salesman_remark)
    print(salesman_image)
    
    context = {
        'single_request': single_request, 
        'salesman_remark': salesman_remark,
        'salesman_image': salesman_image,
    } 

    receiver_remarks = remark_object.remarks_receiver
    print(receiver_remarks)

    if(receiver_remarks):
        context['receiver_remarks'] = receiver_remarks

    checker_remarks = remark_object.remarks_checker
    print(checker_remarks)

    if(checker_remarks):
        context['checker_remarks'] = checker_remarks

    checker_image_1 = image_object.image_checker_1

    if (checker_image_1):
        context['checker_image_1'] = checker_image_1
        
    checker_image_2 = image_object.image_checker_2

    if (checker_image_2):
        context['checker_image_2'] = checker_image_2

    return render(request, 'request_view_universal.html', context)

@login_required(login_url=userLogin)
def updateSalesmanRemark(request, rid):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    request_object = requestTable.objects.get(rid = rid)
    remark_object = requestRemarks.objects.get(request_id = request_object)

    if request.method == 'POST':
        updated_remark = request.POST.get('updated_remark')
        remark_object.remarks_salesman = updated_remark
        remark_object.save()

        addNotification(request, request_object, 'Request Updated Successfully', 'success')

        return HttpResponse('Done')
    
    return HttpResponse('Error')

@login_required(login_url=userLogin)
def updateSalesmanImage(request, rid):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    request_object = requestTable.objects.get(rid = rid)
    image_object = requestImages.objects.get(request_id = request_object)

    if request.method == 'POST':
        updated_image_salesman = request.FILES.get('updated_image_salesman')
        image_object.image_salesman = updated_image_salesman
        image_object.save()

        addNotification(request, request_object, 'Request Updated Successfully', 'success')

        return HttpResponse('Done')
    
    return HttpResponse('Error')


@login_required(login_url=userLogin)
def receiver_dashboard(request):
    if (request.user.role != 'receiver'):
        return render(request, 'accessDenied.html')
    
    t_requests = requestTable.objects.all()
    total_requests = t_requests.count()

    pu_requests = urgentRequestTable.objects.filter(urgency_status = 'in_review')
    pending_urgent_requests = pu_requests.count()

    au_requests = urgentRequestTable.objects.filter(urgency_status = 'accepted')
    accepted_urgent_requests = au_requests.count()

    ru_requests = urgentRequestTable.objects.filter(urgency_status = 'rejected')
    rejected_urgent_requests = ru_requests.count()

    a_requests = requestTable.objects.filter(request_status = 'accepted')
    accepted_requests = a_requests.count()
    
    r_requests = requestTable.objects.filter(request_status = 'rejected')
    rejected_requests = r_requests.count()

    ref_requests = requestTable.objects.filter(request_status = 'refunded')
    refunded_requests = ref_requests.count()


    context = {
        'total_requests': total_requests,
        'pending_urgent_requests': pending_urgent_requests,
        'accepted_urgent_requests': accepted_urgent_requests,
        'rejected_urgent_requests': rejected_urgent_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests,
        'refunded_requests': refunded_requests,
    }

    return render(request, 'receiver_board.html', context)

@login_required(login_url=userLogin)
def receiverViewRequests(request):
    if (request.user.role != 'receiver'):
        return render(request, 'accessDenied.html')
    
    requests = requestTable.objects.all().select_related('vid')
    page_object = universal_pagination(request, requests)

    context = {
        'requests': page_object, 
    }

    return render(request, 'receiver_all_requests.html', context)

@login_required(login_url=userLogin)
def receiverViewRequestsConditional(request, status):
    if (request.user.role != 'receiver'):
        return render(request, 'accessDenied.html')
    
    requests = requestTable.objects.filter(request_status = str(status)).select_related('vid')
    page_object = universal_pagination(request, requests)

    context = {
        'requests': page_object, 
    }

    return render(request, 'receiver_all_requests.html', context)

@login_required(login_url=userLogin)
def receiverViewUrgentRequests(request,):
    if (request.user.role != 'receiver'):
        return render(request, 'accessDenied.html')
    
    urgent_requests = urgentRequestTable.objects.filter(urgency_status = 'in_review').select_related('rid__vid')
    page_object = universal_pagination(request, urgent_requests)

    context = {
        'urgent_requests': page_object, 
    }

    return render(request, 'urgency_request.html', context)


@login_required(login_url=userLogin)
def updateReceiverRemark(request, rid):
    if (request.user.role != 'receiver'):
        return render(request, 'accessDenied.html')
    
    request_object = requestTable.objects.get(rid = rid)
    remark_object = requestRemarks.objects.get(request_id = request_object)

    if request.method == 'POST':
        updated_remark = request.POST.get('updated_remark')
        remark_object.remarks_receiver = updated_remark
        remark_object.save()

        addNotification(request, request_object, 'Request Updated Successfully', 'success')

        return HttpResponse('Done')
    
    return HttpResponse('Error')

@login_required(login_url=userLogin)
def rejectRequest(request, rid):

    request_object = requestTable.objects.get(rid = rid)

    context = {
        'request_object': request_object,
    }

    try:
        reject_object = rejectedRequestTable.objects.get(rid = request_object)
        rejection_reason = reject_object.rejection_reason
        print(rejection_reason)

        context['rejection_reason'] = rejection_reason

    except Exception as e:
        print(e)

    if request.method == 'POST':
        request_object.request_status = 'rejected'
        request_object.save()

        rejection_object = rejectedRequestTable(
            rid = request_object,
            rejected_by = f'{request.user} + ({request.user.role})',
            rejection_reason = request.POST.get('rejection_reason')
        )

        rejection_object.save()
        addNotification(request, request_object, 'Request Rejected Successfully', 'success')
        return redirect('receiverViewRequests')
        
    return render(request, 'reject_request.html', context)

@login_required(login_url=userLogin)
def acceptRequest(request, rid):
    request_object = requestTable.objects.get(rid = rid)

    if request.user.role == 'receiver':
        request_object.request_status = 'accepted'
        addNotification(request, request_object, 'Request Accepted Successfully', 'success')
    elif request.user.role == 'checker':
        request_object.request_status = 'checked'
        addNotification(request, request_object, 'Request Checked Successfully', 'success')
    
    request_object.save()

    return HttpResponse('Works')

@login_required(login_url=userLogin)     
def checker_dashboard(request):
    if (request.user.role != 'checker'):
        return render(request, 'accessDenied.html')
    
    t_requests = requestTable.objects.filter(request_status = 'accepted')
    total_requests = t_requests.count()

    a_requests = urgentRequestTable.objects.filter(urgency_status = 'accepted')
    accepted_urgent_requests = a_requests.count()

    p_requests = requestTable.objects.filter(request_status = 'checked')
    passed_requests = p_requests.count()

    f_requests = requestTable.objects.filter(request_status = 'failed')
    failed_requests = f_requests.count()


    context = {
        'total_requests': total_requests,
        'accepted_urgent_requests': accepted_urgent_requests,
        'passed_requests': passed_requests,
        'failed_requests': failed_requests,
    }

    return render(request, 'checker_board.html', context)

@login_required(login_url=userLogin)
def checkerViewRequests(request):
    if (request.user.role != 'checker'):
        return render(request, 'accessDenied.html')
    
    requests = requestTable.objects.filter(request_status = 'accepted').select_related('vid')
    page_object = universal_pagination(request, requests)

    context = {
        'requests': page_object, 
    }

    return render(request, 'checker_all_requests.html', context)

@login_required(login_url=userLogin)
def checkerViewPassedRequest(request):
    if (request.user.role != 'checker'):
        return render(request, 'accessDenied.html')
    
    requests = requestTable.objects.filter(request_status = 'checked').select_related('vid')
    page_object = universal_pagination(request, requests)

    context = {
        'requests': page_object, 
    }

    return render(request, 'checker_all_requests.html', context)

@login_required(login_url=userLogin)
def checkerViewFailedRequest(request):
    if (request.user.role != 'checker'):
        return render(request, 'accessDenied.html')
    
    requests = requestTable.objects.filter(request_status = 'failed').select_related('vid')
    page_object = universal_pagination(request, requests)

    context = {
        'requests': page_object,
    }

    return render(request, 'checker_all_requests.html', context)

@login_required(login_url=userLogin)
def updateCheckerRemark(request, rid):
    if (request.user.role != 'checker'):
        return render(request, 'accessDenied.html')
    
    request_object = requestTable.objects.get(rid = rid)
    remark_object = requestRemarks.objects.get(request_id = request_object)

    if request.method == 'POST':
        updated_remark = request.POST.get('updated_remark')
        remark_object.remarks_checker = updated_remark
        remark_object.save()

        addNotification(request, request_object, 'Checker Remarks Updated Successfully', 'success')
        return HttpResponse('Done')
    
    return HttpResponse('Error')

@login_required(login_url=userLogin)
def updateCheckerImage(request, rid):
    if (request.user.role != 'checker'):
        return render(request, 'accessDenied.html')
    
    request_object = requestTable.objects.get(rid = rid)
    image_object = requestImages.objects.get(request_id = request_object)
    
    print(request.method)

    if request.method == 'POST':
        try:
            updated_image_checker_1 = request.FILES.get('updated_image_checker_1')
        except Exception as e:
            print(e)
        else:
            updated_image_checker_2 = request.FILES.get('updated_image_checker_2')
        
        if(updated_image_checker_1):
            image_object.image_checker_1 = updated_image_checker_1
            image_object.save()
            addNotification(request, request_object, 'Checker Image1 Updated Successfully', 'success')
        elif(updated_image_checker_2):
            image_object.image_checker_2 = updated_image_checker_2
            image_object.save()
            addNotification(request, request_object, 'Checker Image2 Updated Successfully', 'success')
        
        return HttpResponse('Done')
    
    return HttpResponse('Error')

@login_required(login_url=userLogin)
def updateCheckerImageBoth(request, rid):
    if (request.user.role != 'checker'):
        return render(request, 'accessDenied.html')
    
    request_object = requestTable.objects.get(rid = rid)
    image_object = requestImages.objects.get(request_id = request_object)
    
    print(request.method)

    if request.method == 'POST': 
        updated_image_checker_1 = request.FILES.get('updated_image_checker_1')
        print(updated_image_checker_1)
        updated_image_checker_2 = request.FILES.get('updated_image_checker_2')
        print(updated_image_checker_2)
            
        image_object.image_checker_1 = updated_image_checker_1
        
        image_object.image_checker_2 = updated_image_checker_2
        image_object.save()
        
        addNotification(request, request_object, 'Checker Images Updated Successfully', 'success')
        return HttpResponse('Done')
    
    return HttpResponse('Error')

@login_required(login_url=userLogin)
def raiseUrgent(request):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    requests = requestTable.objects.filter(Q(raised_by=request.user) & ~Q(urgency_status='accepted'))

    context = {
        'requests':requests,
    }

    return render(request, 'raise_urgent.html', context)

@login_required(login_url=userLogin)
def raiseReason(request, rid):
    if (request.user.role != 'salesman'):
        return render(request, 'accessDenied.html')
    
    single_request = requestTable.objects.get(rid = rid)
    uid = single_request.uid
    print(uid)

    context = {
        'single_request': single_request,
    }

    try:
        if(uid != 'random'):
            urgency_object = urgentRequestTable.objects.get(uid = uid)
            urgency_reason = urgency_object.urgency_reason
            context['urgency_reason'] = urgency_reason

    except Exception as e:
        print(e)

    if request.method == 'POST':
        try:
            urgency_object = urgentRequestTable.objects.get(uid = uid)
            urgency_object.urgency_reason = request.POST.get('urgency_reason')
            urgency_object.save()

        except Exception as e:
            new_urgent_request = urgentRequestTable(
                rid = single_request,
                urgency_reason = request.POST.get('urgency_reason'),
                urgency_status = 'in_review',
            )

            new_urgent_request.save()

            uid = new_urgent_request.uid
            request_object = requestTable.objects.get(rid = rid)
            request_object.uid = uid
            request_object.save()

            addNotification(request, request_object, 'Urgency Raised Successfully', 'success')

        return redirect('raiseUrgent')

    return render(request, 'raise_reason.html', context)

@login_required(login_url=userLogin)
def allUrgentRequestView(request, status):
    urgent_requests = urgentRequestTable.objects.filter(urgency_status = str(status)).select_related('rid__vid')
    page_object = universal_pagination(request, urgent_requests)
    
    context = { 
        'urgent_requests': page_object,
    }

    return render(request, 'urgent_view_all.html', context)

@login_required(login_url=userLogin)
def viewSingleUrgentRequest(request, uid):
    urgent_object = urgentRequestTable.objects.select_related('rid').get(uid=uid)

    context = {
        'urgent_object': urgent_object,
    }

    return render(request, 'receiver_view_reason.html', context)

@login_required(login_url=userLogin)
def addDenialReason(request, uid):
    urgent_object = urgentRequestTable.objects.select_related('rid').get(uid=uid)
    request_object = requestTable.objects.get(rid = urgent_object.rid.rid)
    
    if request.method == 'POST':
        urgent_object.denial_reason = request.POST.get('denial_reason')
        urgent_object.urgency_status = 'rejected'
        urgent_object.save()
        request_object.urgency_status = 'rejected'
        request_object.save()

        addNotification(request, request_object, 'Urgency Request Denied', 'danger')

        return HttpResponse('DOne')

    return HttpResponse('Works')

@login_required(login_url=userLogin)
def acceptUrgentReason(request, uid):
    urgent_object = urgentRequestTable.objects.select_related('rid').get(uid=uid)
    request_object = requestTable.objects.get(rid = urgent_object.rid.rid)
    
    if request.method == 'POST':
        urgent_object.urgency_status = 'accepted'
        urgent_object.save()
        request_object.urgency_status = 'accepted'
        request_object.refund_type = 'urgent'
        request_object.save()

        addNotification(request, request_object, 'Urgency Reason Accepted', 'success')

        return HttpResponse('Done')

    return HttpResponse('Works')

@login_required(login_url=userLogin)
def viewOngoingUrgentRequests(request):
    ongoing_request = requestTable.objects.filter(Q(urgency_status = 'accepted') & Q(raised_by=request.user))
    page_object = universal_pagination(request, ongoing_request)

    context = {
        'requests': page_object,
    }

    return render(request, 'raise_urgent.html', context)


@login_required(login_url=userLogin)
def accountant_dashboard(request):
    if (request.user.role != 'accountant'):
        return render(request, 'accessDenied.html')
    
    t_requests = requestTable.objects.filter(request_status = 'checked')
    total_requests = t_requests.count()

    a_requests = urgentRequestTable.objects.filter(
        urgency_status='accepted',
        rid__request_status='checked'
    ).select_related('rid')

    accepted_urgent_requests = a_requests.count()

    r_requests = requestTable.objects.filter(request_status = 'refunded')
    refunded_requests = r_requests.count()

    context = {
        'total_requests': total_requests,
        'accepted_urgent_requests': accepted_urgent_requests,
        'refunded_requests': refunded_requests 
    }

    return render(request, 'accountant_dashboard.html', context)

@login_required(login_url=userLogin)
def accountantViewRequests(request):
    if (request.user.role != 'accountant'):
        return render(request, 'accessDenied.html')
    
    t_requests = requestTable.objects.filter(request_status = 'checked')
    page_object = universal_pagination(request, t_requests)

    context = {
        'requests': page_object, 
    }

    return render(request, 'accountant_all_requests.html', context)

@login_required(login_url=userLogin)
def accountantViewRefundRequests(request):
    if (request.user.role != 'accountant'):
        return render(request, 'accessDenied.html')
    
    t_requests = requestTable.objects.filter(request_status = 'refunded')
    page_object = universal_pagination(request, t_requests)

    context = {
        'requests': page_object, 
    }

    return render(request, 'accountant_all_requests.html', context)

@login_required(login_url=userLogin)
def uploadInvoice(request, rid):
    if (request.user.role != 'accountant'):
        return render(request, 'accessDenied.html')
    
    single_request = requestTable.objects.get(rid = rid)

    context = {
        'single_request': single_request,
    }

    try:
        invoice_object = invoiceTable.objects.get(rid = single_request)
        invoice_image = invoice_object.invoice
        iid = invoice_object.iid
        context['iid'] = iid
        context['invoice_image'] = invoice_image

    except Exception as e:
        print(e)

    if request.method == 'POST':
        upload_invoice = request.FILES['upload_invoice'] 
        inovice_object = invoiceTable.objects.create(
            rid = single_request,
            invoice = upload_invoice
        )     

        inovice_object.save()

        iid = inovice_object.iid
        single_request.iid = iid
        single_request.request_status = 'refunded'
        single_request.save()

        addNotification(request, single_request, 'Request Refunded Successfully', 'success')

        return HttpResponse('Works')


    return render(request, 'upload_invoice.html', context)

@login_required(login_url=userLogin)
def updateInvoice(request, iid):
    if (request.user.role != 'accountant'):
        return render(request, 'accessDenied.html')
    
    invoice_object = invoiceTable.objects.get(iid = iid)
    request_object = invoice_object.rid

    if request.method == 'POST':
        upload_invoice = request.FILES['upload_invoice'] 
        invoice_object.invoice = upload_invoice

        invoice_object.save()

        addNotification(request, request_object, 'Request Refunded Successfully', 'success')

        return HttpResponse('Works')


    return render(request, 'upload_invoice.html')

@login_required(login_url=userLogin)
def admin_dashboard(request):
    if (request.user.role != 'admin'):
        return render(request, 'accessDenied.html')
    
    User = get_user_model()
    salesman_object = User.objects.filter(role = 'salesman')
    salesman_count = salesman_object.count()

    receiver_object = User.objects.filter(role = 'receiver')
    receiver_count = receiver_object.count()

    checker_object = User.objects.filter(role = 'checker')
    checker_count = checker_object.count()

    accountant_object = User.objects.filter(role = 'accountant')
    accountant_count = accountant_object.count()

    request_object = requestTable.objects.all()
    request_count = request_object.count()

    context = {
        'salesman_count':salesman_count,
        'receiver_count':receiver_count,
        'checker_count':checker_count,
        'accountant_count':accountant_count,
        'request_count':request_count,
    }

    return render(request, 'admin_dashboard.html', context)

@login_required(login_url=userLogin)
def viewSalesman(request):
    if (request.user.role != 'admin'):
        return render(request, 'accessDenied.html')
        
    User = get_user_model()
    salesman_object = User.objects.filter(role = 'salesman')
    page_object = universal_pagination(request, salesman_object)

    context = {
        'requests':  page_object,
        'role': 'Salesmen'
    }

    return render(request, 'view_users.html', context)

@login_required(login_url=userLogin)
def viewReceiver(request):
    if (request.user.role != 'admin'):
        return render(request, 'accessDenied.html')
        
    User = get_user_model()
    receiver_object = User.objects.filter(role = 'receiver')
    page_object = universal_pagination(request, receiver_object)

    context = {
        'requests':  page_object,
        'role': 'Receivers'
    }

    return render(request, 'view_users.html', context)

@login_required(login_url=userLogin)
def viewCheckers(request):
    if (request.user.role != 'admin'):
        return render(request, 'accessDenied.html')
        
    User = get_user_model()
    checker_object = User.objects.filter(role = 'checker')
    page_object = universal_pagination(request, checker_object)

    context = {
        'requests':  page_object,
        'role': 'Checkers'
    }

    return render(request, 'view_users.html', context)

@login_required(login_url=userLogin)
def viewAccountant(request):
    if (request.user.role != 'admin'):
        return render(request, 'accessDenied.html')
        
    User = get_user_model()
    accountant_object = User.objects.filter(role = 'accountant')
    page_object = universal_pagination(request, accountant_object)

    context = {
        'requests':  page_object,
        'role': 'Receivers'
    }

    return render(request, 'view_users.html', context)

@login_required(login_url=userLogin)
def editUser(request, pk):
    if (request.user.role != 'admin'):
        return render(request, 'accessDenied.html')
        
    User = get_user_model()
    user_object = User.objects.get(pk = pk)
    form = UserRegisterForm(instance = user_object)

    context = {
        'form': form,
        'user_object': user_object,
    }

    if request.method == 'POST':
        user_object.username = request.POST.get('username')
        user_object.email = request.POST.get('email')
        user_object.role = request.POST.get('role')

        user_object.save()

        return render(request, 'edit_user.html', context)

    return render(request, 'edit_user.html', context)

@login_required(login_url=userLogin)
def adminViewAllRequests(request):
    if (request.user.role != 'admin'):
        return render(request, 'accessDenied.html')
        
    requests = requestTable.objects.all().select_related('vid')
    page_object = universal_pagination(request, requests)

    context = {
        'requests':page_object,
    }

    return render(request, 'request_data.html', context)

@login_required(login_url=userLogin)
def deleteUser(request, pk):
    if (request.user.role != 'admin'):
        return render(request, 'accessDenied.html')
        
    User = get_user_model()
    user_object = User.objects.get(pk = pk)

    user_object.delete()

    return HttpResponse('Works')
