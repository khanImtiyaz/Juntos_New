from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from Vendor import views

appname = 'Vendor'
# ******* WEBSITE URL ********
urlpatterns = [
	url(r'^vendor-signup$', views.VendorSignup.as_view(), name='vendor-signup'),
	url(r'^vendor-signup-1$', views.VendorSignupStep1.as_view(), name='vendor-signup-1'),
	url(r'^vendor-signup-2$', views.VendorSignupStep2.as_view(), name='vendor-signup-2'),
	url(r'^vendor-signup-3$', views.VendorSignupStep3.as_view(), name='vendor-signup-3'),
	url(r'^dashboard$', views.VendorDashboard.as_view(), name='vendor-dashboard'),
	url(r'^vendor$', views.BVendor.as_view(), name='bevendor'),
	url(r'^vendorlogout$', views.LogoutView.as_view(), name='vendor-logout'),
	url(r'^vendor/profile$', views.ProfileView.as_view(), name='vendor-profile-view'),
	url(r'^vendor/update/profile$', views.UpdateProfile.as_view(), name='vendor-update-profile'),
	url(r'^products/(?P<active>[0-1]+)$', views.ProductList.as_view(), name='product-list'),
	url(r'^expired-products', views.ExpiredProductList.as_view(), name='expired-products'),
	url(r'^add-product$', views.AddProduct.as_view(), name='add-product'),
	url(r'^notification/(?P<read>[0-9]+)$', views.Notification.as_view(), name='notifications'),
	url(r'^remove-notification/(?P<pk>[0-9]+)$', views.RemoveNotification.as_view(), name='remove-notifications'),
	url(r'^quantity-change$', views.quantityChange, name='quantity-change'),
	url(r'^update-expiry-date/(?P<pk>[0-9]+)$', views.UpdateExpiryDate.as_view(), name='update-expiry-date'),
	url(r'^payment$', views.PaymentTransactionDetails.as_view(), name='payments'),
	url(r'^sub-category$', views.SubCategoryList.as_view(), name="subcategories"),
	url(r'^vendor-reset-password$', views.ChangePassword.as_view(), name="change-password"),
	url(r'^remove-product/(?P<pk>[0-9]+)$', views.RemoveProduct.as_view(), name="remove-product"),
	url(r'^sellingchart/(?P<query>[a-z]+)$', views.SellingChart.as_view(), name="selling-chart"),
	url(r'^order-history/(?P<status>[A-Za-z]+)$', views.OrderHistory.as_view(), name="orders-history"),
	url(r'^order-delivered/(?P<pk>[0-9]+)$', views.OrderDelivered.as_view(), name="order-delivered"),
	url(r'^update-product/(?P<slug>.*)$', views.UpdateProduct.as_view(), name='update-product'),
	url(r'^sub-catogorytag$', views.GetSubCategoryTag.as_view(), name="subcategory-tag"),
	# url(r'^complete-registration/$', complete_registration, name="complete_registration"),
	url(r'^order-details/(?P<order_id>[0-9]+)$', views.OrderDetails.as_view(), name="order-details"),
	# url(r'^order-invoice-pdf/(?P<order>[0-9]+)/(?P<invoice>[0-9]+)$', invoice_pdf_generator, name="html_to_pdf_directly"),
	url(r'^dhl-shipment-page$', views.DhlPage.as_view(), name="dhl-page"),
	url(r'^dhl-credential$', views.DhlCredentials.as_view(), name="dhl-credential"),
	url(r'^uploaded-product$', views.UploadedProducts.as_view(), name='uploaded-products'),
	url(r'^delete-colors$', views.DeleteColors.as_view(), name='delete-colors'),
	url(r'^vendor/view-order$', views.VendorViewOrder.as_view(), name='vendor-view-order'),
	# url(r'^Reposting_product/$', repost_products, name='repost_products'),
	url(r'^order-invoice$', views.InvoiceOrder.as_view(), name="invoice-order"),
	url(r'^delete-product-image$', views.DeleteProductImage.as_view(), name="delete-product-image"),
	url(r'^upload-image$', views.UploadImage.as_view(), name="upload-image"),

]
