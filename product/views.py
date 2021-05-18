import json

from django.views               import View
from django.http                import JsonResponse, HttpResponse
from django.db.models.functions import Lower
from django.core.exceptions     import ValidationError
from product.models             import Product, SubCategory

class FilterView(View):
    def get_queryset(self, request, sub_category_name): 
        sub_category = SubCategory.objects.get(english_name=sub_category_name)
        product_list = Product.objects.filter(sub_category=sub_category)
        return product_list
    def list(self, request, sub_category_name): 
        product_list = self.set_filters(self.get_queryset(request,sub_category_name), request)
        return list(product_list.values())
    def set_filters(self, product_list, request): 
        offset     = request.GET.get('offset', None)
        nextoffset = request.GET.get('nextoffset', None)
        if (offset != "") and (nextoffset != ""):
            product_list = product_list[int(offset):int(nextoffset)]
            return product_list
        if offset == "":
            product_list = product_list[:int(nextoffset)]
            return product_list
        if nextoffset == "":
            product_list = product_list[int(offset):]
            return product_list

    def get(self, request, sub_category_name):
        try:
            if list(request.GET.keys()) != []:
                field_list   = [field.name for field in Product._meta.get_fields()]
                products     = Product.objects.none()
                products     = FilterView.get_queryset(self, request, sub_category_name)
                sort_list    = {'PRICE_LOW_TO_HIGH':'price','PRICE_HIGH_TO_LOW':'-price','NEWEST':'is_new','NAME_ASCENDING':Lower('ko_name')}
                #pagenation 
                if list(request.GET.keys()) == ['offset', 'nextoffset']:
                    result.append(FilterView.list(self, request, sub_category_name))
                else:
                    #정렬 filter
                    for key, value in request.GET.items():
                        if key == 'sort':
                            if value not in list(sort_list.keys()):
                                return JsonResponse({'massage':'INVALID SORT'}, status=404)
                            elif value == 'NEWEST':
                                products = products.filter(is_new=True).values()
                            else:
                                products = products.order_by(sort_list[value]).values()
                        #색상, 가격, 시리즈, 특가, 신제품 filter(가격대 filter code 추가 필요)
                        elif key != 'sort':
                            if key not in field_list:
                                raise Product.DoesNotExist 
                            else:
                                products = products.filter(**{key:value}).values()
                result = [i for i in products.distinct()]     
                return JsonResponse({'result':result}, status=200)
        except Product.DoesNotExist as e:
            return JsonResponse({'massage':f'{e}'}, status=404)
        except ValidationError as e:
            return JsonResponse({'massge':f'{e}'}, status=404)