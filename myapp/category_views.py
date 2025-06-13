from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import  Category

@login_required
def categories(request):
        if request.method == "POST":
              category_name = request.POST.get("categoryName")

              if category_name:
                      Category.objects.create(
                                          category_name=category_name,
                                          created_by=request.user,
                            )
              else:
                            pass

              return redirect("categories")
        else:
              categories = Category.objects.filter(is_deleted=1).order_by(
              "-id"
              )
              return render(request, "myapp/categories.html", {"categories": categories})


@login_required
def edit_category(request):
        if request.method == "POST":
              id = request.POST.get("id")
              category_name = request.POST.get("categoryName")

              if category_name and id:
              #         check if categoy exists for editing
                  category_check = Category.objects.filter(id=id)
                  if category_check.count() > 0:
                            category = category_check.first()
                            category.category_name = category_name
                            category.save()
                  else:
                      pass
                              
              
              else:
                  pass

              return redirect("categories")
        else:
              return redirect("categories")
        
@login_required
def delete_category(request):
        if request.method == "POST":
              id = request.POST.get("id")

              if id:
              #         check if categoy exists for editing
                  category_check = Category.objects.filter(id=id)
                  if category_check.count() > 0:
                            category = category_check.first()
                            category.is_deleted = 0
                            category.save()
                  else:
                      pass
                              
              
              else:
                  pass

              return redirect("categories")
        else:
              return redirect("categories")

             