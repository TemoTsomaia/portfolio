from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import CreateToyForm, AssignForm
from .models import Toy, Coal
from santas_list.models import Santas_list

def create_toy(request):
    if request.method == 'POST':
        form = CreateToyForm(request.POST)
        if form.is_valid():
            kid = form.cleaned_data['kid']
            time_to_create = form.cleaned_data['time_to_create']

            toy = Toy.objects.create(name=kid.wanted_toy, time_to_create=time_to_create)

            return JsonResponse({
                "message": f"Toy '{toy.name}' has been created for kid '{kid.name}'"
            }, status=200)
    else:
        form = CreateToyForm()

    return render(request, 'create_toy.html', {'form': form})


def view_toys(request):
    toys = Toy.objects.all()  # Query all toys from the Toy model
    return render(request, 'view_toys.html', {'toys': toys})

#def view_available(request):
    #toys = Toy.objects.filter(is_assigned=False)  # Query all toys from the Toy model
    #return render(request, 'view_toys.html', {'toys': toys})

def view_toy(request, toy_id):
    toy = get_object_or_404(Toy, id=toy_id)

    return render(request, 'view_toy.html', {'toy': toy})


def assign(request):
    if request.method == 'POST':
        form = AssignForm(request.POST)
        if form.is_valid():
            # Get the selected kid
            kid = form.cleaned_data['name']

            santas_list = Santas_list.objects.first()
            if not santas_list:
                return JsonResponse({"message": "Santa's list not found."}, status=404)


            if kid.niceness_coefficient > 5:
                toy = Toy.objects.filter(name=kid.wanted_toy, is_assigned=False).first()

                if toy:
                    kid.toy = toy
                    toy.is_assigned = True
                    kid.save()
                    toy.save()
                    return JsonResponse({
                        "message": f"Toy '{toy.name}' has been assigned to {kid.name}."
                    }, status=200)
                else:
                    return JsonResponse({"message": "No toy exists for this kid."}, status=400)

            elif kid.niceness_coefficient <= 5:
                coal = Coal.objects.create()
                kid.coal = coal
                kid.save()
                return JsonResponse({
                    "message": f"Coal has been assigned to {kid.name}."
                }, status=200)

    else:
        form = AssignForm()

    return render(request, 'assign.html', {'form': form})
