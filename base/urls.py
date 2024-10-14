from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.userRegistration, name='userRegistration'),
    path('login/', views.userLogin, name='userLogin'),
    path('logout/', views.logoutUser, name='logoutUser'),

    # Salesman Related URLs
    path('salesman/dashboard/', views.salesman_dashboard, name='salesman_dashboard'),
    path('salesman/dashboard/vendors/', views.viewVendors, name='viewVendors'),
    path('salesman/dashboard/add_party/', views.addParty, name='addParty'),
    path('salesman/dashboard/delete_party/', views.deleteParty, name='deleteParty'),
    path('salesman/dashboard/add_request/', views.addRequest, name='addRequest'),
    path('salesman/dashboard/requests/', views.viewRequests, name='viewRequests'),
    path('salesman/dashboard/active_requests/', views.viewActiveRequests, name='viewActiveRequests'),
    path('salesman/dashboard/delete_requests/', views.deleteRequests, name='deleteRequests'),
    path('salesman/dashboard/requests/<str:rid>', views.viewSingleRequest, name='viewSingleRequest'),
    path('salesman/dashboard/update_request/<str:rid>', views.updateSalesmanRemark, name='updateSalesmanRemark'),
    path('salesman/dashboard/update_image/<str:rid>', views.updateSalesmanImage, name='updateSalesmanImage'),
    path('salesman/dashboard/raise/', views.raiseUrgent, name='raiseUrgent'),
    path('salesman/dashboard/raise/reason/<str:rid>', views.raiseReason, name='raiseReason'),
    path('salesman/dashboard/view_ongoing/', views.viewOngoingUrgentRequests, name='viewOngoingUrgentRequests'),

    # Receiver Realted URLs
    path('receiver/dashboard/', views.receiver_dashboard, name='receiver_dashboard'),
    path('receiver/dashboard/requests', views.receiverViewRequests, name='receiverViewRequests'),
    path('receiver/dashboard/requests/<str:rid>', views.viewSingleRequest, name='viewSingleRequest'),
    path('receiver/dashboard/requests/status/<str:status>', views.receiverViewRequestsConditional, name='receiverViewRequestsConditional'),
    path('receiver/dashboard/update_request/<str:rid>', views.updateReceiverRemark, name='updateReceiverRemark'),
    path('receiver/dashboard/requests/accept/<str:rid>', views.acceptRequest, name='acceptRequest'),
    path('receiver/dashboard/urgent_requests/<str:status>', views.allUrgentRequestView, name='allUrgentRequestView'),
    path('receiver/dashboard/urgent_requests_view/<str:uid>', views.viewSingleUrgentRequest, name='viewSingleUrgentRequest'),
    path('receiver/dashboard/denial_reason/<str:uid>', views.addDenialReason, name='addDenialReason'),
    path('receiver/dashboard/accept_urgent/<str:uid>', views.acceptUrgentReason, name='acceptUrgentReason'),
    
    path('checker/dashboard/', views.checker_dashboard, name='checker_dashboard'),
    path('checker/dashboard/requests', views.checkerViewRequests, name='checkerViewRequests'),
    path('checker/dashboard/requests/<str:rid>', views.viewSingleRequest, name='checkerViewSingleRequest'),
    path('checker/dashboard/update_image/<str:rid>', views.updateCheckerImage, name='updateCheckerImage'),
    path('checker/dashboard/update_image_both/<str:rid>', views.updateCheckerImageBoth, name='updateCheckerImageBoth'),
    path('checker/dashboard/requests/accept/<str:rid>', views.acceptRequest, name='acceptRequest'),
    path('checker/dashboard/update_request/<str:rid>', views.updateCheckerRemark, name='updateCheckerRemark'),
    path('checker/dashboard/urgent_requests/<str:status>', views.allUrgentRequestView, name='allUrgentRequestView'),
    path('checker/dashboard/passed_requests/', views.checkerViewPassedRequest, name='checkerViewPassedRequest'),
    path('checker/dashboard/failed_requests/', views.checkerViewFailedRequest, name='checkerViewFailedRequest'),
    
    path('accountant/dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('accountant/dashboard/requests/', views.accountantViewRequests, name='accountantViewRequests'),
    path('accountant/dashboard/requests/upload_invoice/<str:rid>', views.uploadInvoice, name='uploadInvoice'),
    path('accountant/dashboard/requests/update_invoice/<str:iid>', views.updateInvoice, name='updateInvoice'),
    path('accountant/dashboard/requests/refunded/', views.accountantViewRefundRequests, name='accountantViewRefundRequests'),

    path('dashboard/requests/reject/<str:rid>', views.rejectRequest, name='rejectRequest'),
    
    path('milanadmin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('milanadmin/dashboard/salesman', views.viewSalesman, name='viewSalesman'),
    path('milanadmin/dashboard/receiver', views.viewReceiver, name='viewReceiver'),
    path('milanadmin/dashboard/checker', views.viewCheckers, name='viewChecker'),
    path('milanadmin/dashboard/accountant', views.viewAccountant, name='viewAccountant'),
    path('milanadmin/dashboard/edit_user/<str:pk>', views.editUser, name='editUser'),
    path('milanadmin/dashboard/requests/', views.adminViewAllRequests, name='adminViewAllRequests'),
    path('milanadmin/dashboard/delete_user/<str:pk>', views.deleteUser, name='deleteUser'),
    
    path('dashboard/notifications/', views.viewNotifications, name='viewNotifications'),
] 


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
