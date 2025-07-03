from django.shortcuts import render, HttpResponse
from santas_list.models import *

# Create your views here.

def count_lists(request):
    santas_list = Santas_list.objects.first()
    naughty_count = santas_list.naughty_list.count()

    nice_count = santas_list.nice_list.count()

    message = f"Number of kids in Santa's Naughty list: {naughty_count}\nNumber of kids in Santa's Nice list: {nice_count}"

    return HttpResponse(message, content_type="text/plain")

def count_demand(request):
    demand = dict()
    kids = Kid.objects.filter(santas_list__isnull=False)
    for kid in kids:
        if kid.wanted_toy not in demand:
            demand[kid.wanted_toy] = 1
        else:
            demand[kid.wanted_toy] += 1

    return render(request, 'demand.html', {'demand': demand})


def sum_times_to_create(request):
    toys = Toy.objects.all()

    time = sum(toy.time_to_create for toy in toys)

    message = f"Time needed to create all {Toy.objects.all().count()} toys: {time}"

    return HttpResponse(message, content_type="text/plain")

def sum_times_to_deliver(request):
    toys = Toy.objects.all().count()

    time_for_one_toy = 15

    time = time_for_one_toy * toys

    message = f"Time needed to deliver all {toys} toys: {time}"

    return HttpResponse(message, content_type="text/plain")
