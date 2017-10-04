from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from Juntos import views

appname = 'Juntos'
# ******* WEBSITE URL ********
urlpatterns = [
	url(r'^$', views.home,  name="home"),
	url(r'^result$', views.SearchProduct, name='search-product'),
	url(r'^product-detail/(?P<slug>.+)$',views.ProductDetail.as_view(), name='product-detail'),
	url(r'^product-details/(?P<pk>[0-9]+)$', views.ProductColor.as_view(), name='product-color'),
	url(r'^image-view/(?P<color>[0-9]+)$', views.ProductImageView.as_view() , name="product-image-view"),
	url(r'^category/(?P<slug>[-a-zA-Z0-9]+)$', views.Index.as_view(), name='index'),
	url(r'^proceed-cart$', views.ProceedCart.as_view(), name="proceed-cart"),
	url(r'^wish-list$', views.WishList.as_view(), name='wish-list'),
	url(r'^wish-list-add/(?P<product_id>[0-9]+)$', views.AddWishList.as_view(), name='add-wishlist'),
	url(r'^wish-list-remove/(?P<pk>[0-9]+)$', views.RemoveWishList.as_view(), name='remove-wishlist'),
	url(r'^faq$', views.FaqList.as_view(), name='faq'),
	url(r'^conditions$', views.ConditionsView.as_view(), name='conditions'),
	url(r'^term$', views.TermsList.as_view(), name='term'),
	url(r'^carrer$', views.CarrerList.as_view(), name='carrer'),
	url(r'^contact$', views.ContactList.as_view(), name='contact'),
	url(r'^logged-in$', views.LoginView.as_view(), name='login'),
	url(r'^sign-up$', views.RegisterView.as_view(), name='register'),
	url(r'^logout$', views.LogoutView.as_view(), name='logout'),
	url(r'^send-mail$', views.SendMail.as_view(), name='send-mail'),
	url(r'^subscribe-news-letter$', views.SubscribeNewsLetter.as_view(), name='subscribe'),
	url(r'^update$', views.UpdateProfile.as_view(), name='update-profile'),
	url(r'^my-orders$', views.ViewOrder.as_view(), name='view-order'),
	url(r'^check-otp$', views.CheckOTP.as_view(), name='check-otp'),
	url(r'^check-otp$', views.CheckOTP.as_view(), name='check-otp'),
	url(r'^resend-otp$', views.ResendOTP.as_view(), name='resend-otp'),
	url(r'^confirmation/(?P<confirmation_code>\w+)$', views.ConfirmationEmail.as_view(), name="cofirmation"),
	url(r'^add-cart$', views.AddToCart.as_view(), name='add-cart'),
	url(r'^product-detail/(?P<slug>.+)$',views.ProductDetail.as_view(), name='product-detail'),
	# url(r'^viewsscart/(?P<address>[0-9]+)$', view_cart, name='views_cart'),
	url(r'^viewscart$', views.ViewCart.as_view(), name='views-cart'),
	url(r'^check-availability$', views.CheckAvailability.as_view(), name='check-availability'),
	url(r'^image-view/(?P<color>[0-9]+)$', views.ProductImageView.as_view() , name="product-image-view"),
	url(r'^helpfull-review$', views.HelpfullReview.as_view(), name="helpfull-review"),
	url(r'^customer-review$', views.CustomerReview.as_view(), name="customer-review"),
	url(r'^add-cart$', views.AddToCart.as_view(), name='add-cart'),
	# url(r'^add_cart/(?P<pk>[0-9]+)$', add_to_cart, name='add_cart'),
	url(r'^add-shipping$', views.AddShipping.as_view(), name='add-shipping'),
	url(r'^rating$', views.Rating.as_view(), name='rating'),
	url(r'^change-cart-quantity$', views.IncreaseCartQuantity.as_view(), name='increase-cart'),



]

