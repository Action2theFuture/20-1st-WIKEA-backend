from django.urls   import path

from product.views import ProductMainView, SubCategoryView, ProductListView, ProductDetailView, FilterSortView

urlpatterns = [
    path('', ProductMainView.as_view()),
    path('/<str:category_name>', SubCategoryView.as_view()),
    path('/<str:sub_category_name>', ProductListView.as_view()),
    path('/<str:product_name>', ProductDetailView.as_view()),
    path('/<str:sub_category_name>/', FilterSortView.as_view()),
]