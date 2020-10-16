from django.shortcuts import render
import openpyxl
import pandas as pd
import requests
import os
from django.conf import settings
from django.http import HttpResponse, Http404

def home(request):
    print("Hi")
    return render(request,'index.html')


def upload_excel(request):
    if "GET" == request.method:
        return render(request, 'index.html', {})
    else:
        latitudes=[]
        longitudes=[]
        excel_file = request.FILES["myfile11"]
        addresses_df = pd.read_excel(excel_file)
        addresses = addresses_df["Address"].values.tolist()
        print('addresses',addresses)
        for address in addresses:
            print(address)
            # result = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key=AIzaSyDa44caSQp1c1fwrfdzelLkZjSeZ0gorSE')
            # responsejson=result.json()
            # print(responsejson)
            result={
         "address_components" : [
            {
               "long_name" : "1600",
               "short_name" : "1600",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "Amphitheatre Parkway",
               "short_name" : "Amphitheatre Pkwy",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Mountain View",
               "short_name" : "Mountain View",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Santa Clara County",
               "short_name" : "Santa Clara County",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "California",
               "short_name" : "CA",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "United States",
               "short_name" : "US",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "94043",
               "short_name" : "94043",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
         "geometry" : {
            "location" : {
               "lat" : 37.4267861,
               "lng" : -122.0806032
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : 37.4281350802915,
                  "lng" : -122.0792542197085
               },
               "southwest" : {
                  "lat" : 37.4254371197085,
                  "lng" : -122.0819521802915
               }
            }
         },
         "place_id" : "ChIJtYuu0V25j4ARwu5e4wwRYgE",
         "plus_code" : {
            "compound_code" : "CWC8+R3 Mountain View, California, United States",
            "global_code" : "849VCWC8+R3"
         },
         "types" : [ "street_address" ]
      }

            if result and len(result):
                longitude = result['geometry']['location']['lng']
                latitude = result['geometry']['location']['lat']
            else:
                longitude = "N/A"
                latitude = "N/A"

            latitudes.append(latitude)
            longitudes.append(longitude)

        addresses_df["latitudes"] = latitudes
        addresses_df["longitudes"] = longitudes


        addresses_df.to_excel("Addresses_Geocoded.xlsx")

    # return HttpResponse("latitudes and longitudes updated successfully")
    return render(request, 'index.html', {})

def download_excel(request):
    path='Addresses_Geocoded.xlsx'
    file_path = os.path.join(settings.BASE_DIR, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404