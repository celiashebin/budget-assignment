from django.db.models import Sum
from django.shortcuts import render,redirect
from budget.models import *
from budget.forms import *
from django.views.generic import TemplateView
from django.http import JsonResponse
from datetime import date

# Create your views here.
def indexpage(request):
    return render(request, 'budget/index.html')

class CreateRegForm(TemplateView):
    form_class=UserRegFormCreation
    model_name=Users
    template_name = "budget/registration.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"created",'status':200})

class CreateUserLogin(TemplateView):
    model_name=Users
    form_class=UserLogin
    template_name = "budget/login.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print("inside post")
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            qs=Users.objects.get(username=username)
            print(qs)

            if((qs.username==username) & (qs.password==password)):
                request.session['username']=username
                return JsonResponse({"message":"login successfull",'status':200})

            else:
                return JsonResponse({"message":"login failed",'status':204})
        else:
            return redirect("userhome")
class Budgetlogout(TemplateView):

    def get(self, request, *args, **kwargs):
        del request.session["username"]
        return redirect("index")

class UserHome(TemplateView):

    def get(self, request, *args, **kwargs):
        print(request.session["username"])
        return render(request,"budget/userpage.html")

class DatewiseReview(TemplateView):
    model_name=Budget
    form_class=DatewiseReviewForm
    template_name = "budget/datewisereview.html"

    def get(self, request, *args, **kwargs):
        context = {}
        user=request.session["username"]
        context["user"]=user
        context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = request.session["username"]
            from_date = form.cleaned_data["from_date"]
            to_date = form.cleaned_data["to_date"]
            print("from date", from_date)
            print("to_date", to_date)
            qs = self.get_querySet(user, from_date, to_date)
            print(qs)
            context = {}
            context['user']=user
            context['qs'] = qs
            context['form'] = form
            return render(request, self.template_name, context)

    def get_querySet(self,user,from_date,to_date):
        return self.model_name.objects.filter(user=user,date__gte=from_date,date__lte=to_date).values('category_type__category_name').annotate(categorysum=Sum('expenses')).order_by('-categorysum')



class CreateBudget(TemplateView):
    form_class = BudgetFormCreation
    model_name = Budget
    template_name = "budget/budgetentry.html"
    login_required=True

    def get(self, request, *args, **kwargs):
        qs=self.model_name.objects.filter(user=request.session["username"])
        print(qs)
        context = {}
        context["form"] = self.form_class
        context["qs"]=qs
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user=request.session["username"]
            category_type=form.cleaned_data["category_type"]
            date=form.cleaned_data["date"]
            expenses=form.cleaned_data["expenses"]
            description=form.cleaned_data["description"]
            qs=self.model_name(user=user,category_type=category_type,expenses=expenses,date=date,description=description)
            qs.save()
            return redirect("budgetlist")
        else:
            context={}
            context["form"]=self.form_class
            return render(request,self.template_name,context)



class ListBudget(TemplateView):
    model_name = Budget
    template_name = "budget/budget_list.html"


    def get(self, request, *args, **kwargs):
        qs=self.model_name.objects.filter(user=request.session["username"])
        context = {}
        user=request.session["username"]
        context["user"] = user
        context["qs"]=qs
        print(qs)
        return render(request, self.template_name, context)



class UpdateBudget(TemplateView):
    model_name = Budget
    form_class = BudgetFormCreation
    template_name = "budget/budgetentry.html"

    def get_querySet(self):
        return self.model_name.objects.get(id=self.kwargs.get("pk"))

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_querySet())
        context = {}
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("budgetlist")
        else:
            context = {}
            context["form"] = form
            return render(request, self.template_name, context)


class BudgetDelete(TemplateView):
    model_name = Budget
    form_class = BudgetFormCreation
    template_name = 'budget/budget_delete.html'

    def get_queryset(self):
        return self.model_name.objects.get(id=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_queryset())
        context = {}
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.get_queryset().delete()
        print("deleted")
        return redirect("budgetlist")

class BudgetView(TemplateView):
    model_name = Budget
    form_class = BudgetFormCreation
    template_name = 'budget/budget_view.html'


    def get_queryset(self):
        return self.model_name.objects.get(id=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_queryset())
        context = {}
        context["form"] = form
        return render(request, self.template_name, context)


class CategorywiseReview(TemplateView):
    model_name=Budget
    form_class=CategorywiseForm
    template_name = "budget/datewisereview.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = request.session["username"]
            budget_category=form.cleaned_data["category_type"]
            from_date = form.cleaned_data["from_date"]
            to_date = form.cleaned_data["to_date"]
            print("category",budget_category)
            print("from date", from_date)
            print("to_date", to_date)
            qs = self.get_querySet(request,budget_category, from_date, to_date)
            print(qs)
            context = {}
            context['qs'] = qs
            context['form'] = form
            return render(request, self.template_name, context)

    def get_querySet(self,request,budget_category,from_date,to_date):
        return self.model_name.objects.filter(category_type__category_name=budget_category).filter(user=request.session["username"]).filter(date__range=[from_date,to_date]).values('category_type__category_name').annotate(categorysum=Sum('expenses')).order_by('-categorysum')

