# from django.shortcuts import render
# from .image_comparison.main import Searcher, ColorDescriptor
# # Create your views here.

# from ctypes import sizeof
# import cv2
# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import status
# from .serializers import LogoSerializer
# import os
# from logoscan.settings import BASE_DIR, STATIC_ROOT
# import pymongo
# import gridfs
# import pprint
# import numpy as np
# from bson.objectid import ObjectId


# def index(request):
#     return JsonResponse({"message": "This is the backend api."})


# # initialize connection with mogoDb
# client = pymongo.MongoClient("mongodb+srv://ahmed:9izIB3wFIls8vins@cluster0.j9hy3nb.mongodb.net/?retryWrites=true&w=majority")

# # Create database and collections
# database = client['logoscan']

# master_images_index = database['master_images_index']
# uploaded_accurate_images_index = database['uploaded_accurate_images_index']
# uploaded_rejected_images_index = database['uploaded_rejected_images_index']

# # Create compound index on category, product, and brand fields
# master_images_index.create_index([('category', pymongo.ASCENDING),
#                                   ('product', pymongo.ASCENDING), ('brand', pymongo.ASCENDING)])

# uploaded_accurate_images_index.create_index([('category', pymongo.ASCENDING),
#                                              ('product', pymongo.ASCENDING), ('brand', pymongo.ASCENDING)])

# uploaded_rejected_images_index.create_index([('category', pymongo.ASCENDING),
#                                              ('product', pymongo.ASCENDING), ('brand', pymongo.ASCENDING)])


# class LogoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         cd = ColorDescriptor((8, 12, 3))
#         # Get logo data from the api post request
#         data = request.data
#         logo = data['image']

#         category = request.POST.get('category')
#         product = request.POST.get('product')
#         brand = request.POST.get('brand')

#         # initialize gridFs to store logo in database
#         fs = gridfs.GridFS(database)
#         logoId = fs.put(logo, name=logo.name,
#                         **{
#                             'category': category,
#                             'product': product,
#                             'brand': brand,
#                         }
#                         )

#         # process numpy array with logodata stored in database
#         nparr = np.frombuffer(fs.get(logoId).read(), np.uint8)
#         # decode numpy array and descibe image for comparison
#         image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
#         features = cd.describe(image)
#         # convet features to float because searcher need it to be float
#         features = [float(x) for x in features]

#         searcher = Searcher()
#         # do the search for the image features in all index database features
#         results = searcher.search(
#             queryFeatures=features, imagesData=master_images_index.find())

#         # see this print
#         print("____\n")
#         print(results)
#         print("____\n")

#         # if the database is empty
#         # or
#         # the first image in the results which is the most simillar one to the input image
#         # it's distance is > 0.1 means that the image is not dubplicated (dublicated == 0.0 i think)
#         # it will add the image to the database

#         if len(results) == 0 or results[0][1] > 0.1:
#             master_images_index.insert_one(
#                 {
#                     'category': category,
#                     'product': product,
#                     'brand': brand,
#                     'image_id': logoId,
#                     'features': features,
#                 })
#             uploaded_accurate_images_index.insert_one(
#                 {
#                     'category': category,
#                     'product': product,
#                     'brand': brand,
#                     'image_id': logoId,
#                     'features': features,
#                 })
#             uploaded_rejected_images_index.insert_one(
#                 {
#                     'category': category,
#                     'product': product,
#                     'brand': brand,
#                     'image_id': logoId,
#                     'features': features,
#                 })
#         else:
#             fs.delete(logoId)

#         limit = 3
#         images = []
#         for i in results[:limit]:
#             images.append("http://127.0.0.1:8000/api/image/"+i[0])

#         return JsonResponse({'results': images}, status=status.HTTP_201_CREATED)


# class ImageAPIView(APIView):
#     def get(self, request, id):
#         # Connect to MongoDB
#         fs = gridfs.GridFS(database)
#         # Retrieve the image data from MongoDB

#         image_data = fs.get(ObjectId(id)).read()
#         fileName = database.fs.files.find_one(
#             {
#                 "_id": ObjectId(id)
#             }
#         )["name"]
#         # get png or jpg part
#         fileExtension = fileName.split(".")[-1]

#         # Serialize the image data to return it as a response
#         # return Response({'image_data': image_data})
#         return HttpResponse(image_data, content_type=f'image/{fileExtension}')

from .image_comparison.main import Searcher, ColorDescriptor
# Create your views here.

import cv2
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import pymongo
import gridfs
import numpy as np
from bson.objectid import ObjectId


def index(request):
    return JsonResponse({"message": "This is the backend api."})


# initialize connection with mogoDb
client = pymongo.MongoClient("mongodb+srv://ahmed:9izIB3wFIls8vins@cluster0.j9hy3nb.mongodb.net/?retryWrites=true&w=majority")

# Create database and collections
database = client['logoscan']

master_images_index = database['master_images_index']
uploaded_accurate_images_index = database['uploaded_accurate_images_index']
uploaded_rejected_images_index = database['uploaded_rejected_images_index']

# Create compound index on category, product, and brand fields
master_images_index.create_index([('category', pymongo.ASCENDING),
                                  ('product', pymongo.ASCENDING), ('brand', pymongo.ASCENDING)])

uploaded_accurate_images_index.create_index([('category', pymongo.ASCENDING),
                                             ('product', pymongo.ASCENDING), ('brand', pymongo.ASCENDING)])

uploaded_rejected_images_index.create_index([('category', pymongo.ASCENDING),
                                             ('product', pymongo.ASCENDING), ('brand', pymongo.ASCENDING)])


class LogoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        cd = ColorDescriptor((8, 12, 3))
        # Get logo data from the api post request
        data = request.data
        logo = data['image']

        category = request.POST.get('category')
        product = request.POST.get('product')
        brand = request.POST.get('brand')

        # initialize gridFs to store logo in database
        fs = gridfs.GridFS(database)
        logoId = fs.put(logo, name=logo.name,
                        **{
                            'category': category,
                            'product': product,
                            'brand': brand,
                            'flag': 'user_upload'
                        }
                        )

        # process numpy array with logodata stored in database
        nparr = np.frombuffer(fs.get(logoId).read(), np.uint8)
        # decode numpy array and descibe image for comparison
        image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        features = cd.describe(image)
        # convet features to float because searcher need it to be float
        features = [float(x) for x in features]

        searcher = Searcher()
        # Check if all three fields have values
        if category != "/" and product != "/" and brand != "/":
            query = {'category': category, 'product': product, 'brand': brand}
        elif category != "/" and product != "/":
            query = {'category': category, 'product': product}
        elif category != "/":
            query = {'category': category}
        else:
            query = None  # Retrieve all documents


        results = searcher.search(queryFeatures=features, imagesData=master_images_index.find(query))


        # if the database is empty
        # or
        # the first image in the results which is the most simillar one to the input image
        # it's distance is > 0.1 means that the image is not dubplicated (dublicated == 0.0 i think)
        # it will add the image to the database
        # result = [("image1",0.1),
        #           ("image2",0.3),
        #           ("image3",0.5) ]
        #


        uploaded_accurate_images_index.insert_one(
            {
                'category': category,
                'product': product,
                'brand': brand,
                'flag': 'user_upload',
                'image_id': logoId,
                'features': features,
            })
        uploaded_rejected_images_index.insert_one(
            {
                'category': category,
                'product': product,
                'brand': brand,
                'flag': 'user_upload',
                'image_id': logoId,
                'features': features,
            })

        limit = 5
        images = []
        for i in results[:limit]:
            if i[1] > 0.05:
                continue
            images.append("http://100091.pythonanywhere.com/image/"+i[0])

        return JsonResponse({'results': images}, status=status.HTTP_201_CREATED)


class LogoUploadView2(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        cd = ColorDescriptor((8, 12, 3))
        # Get logo data from the api post request
        data = request.data
        logo = data['image']

        category = request.POST.get('category')
        product = request.POST.get('product')
        brand = request.POST.get('brand')

        # initialize gridFs to store logo in database
        fs = gridfs.GridFS(database)
        logoId = fs.put(logo, name=logo.name,
                        **{
                            'category': category,
                            'product': product,
                            'brand': brand,
                            'flag': 'admin_upload'
                        }
                        )

        # process numpy array with logodata stored in database
        nparr = np.frombuffer(fs.get(logoId).read(), np.uint8)
        # decode numpy array and descibe image for comparison
        image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        features = cd.describe(image)
        # convet features to float because searcher need it to be float
        features = [float(x) for x in features]

        searcher = Searcher()
        # do the search for the image features in all index database features
        # results = searcher.search(
        #     queryFeatures=features, imagesData=master_images_index.find())

        # create an empty dictionary for query filters
        query_filters = {}

        # check if category is not None, and add it to the query filters
        if category is not None and category != "":
            query_filters['category'] = category

        # check if product is not None, and add it to the query filters
        if product is not None and product != "":
            query_filters['product'] = product

        # check if brand is not None, and add it to the query filters
        if brand is not None and brand != "":
            query_filters['brand'] = brand

        # if all category, product, and brand are None, then the find query will return all documents in the collection
        if not query_filters:
            query_filters = {}

        # perform the find query with the query filters
        results = searcher.search(
            queryFeatures=features, imagesData=master_images_index.find(query_filters))

        # see this print
        print("____\n")
        print(results)
        print("____\n")

        # if the database is empty
        # or
        # the first image in the results which is the most simillar one to the input image
        # it's distance is > 0.1 means that the image is not dubplicated (dublicated == 0.0 i think)
        # it will add the image to the database

        if len(results) == 0 or results[0][1] > 0.1:
            master_images_index.insert_one(
                {
                    'category': category,
                    'product': product,
                    'brand': brand,
                    'flag': 'admin_upload',
                    'image_id': logoId,
                    'features': features,
                })
        else:
            fs.delete(logoId)

        limit = 3
        images = []
        for i in results[:limit]:
            images.append("http://100091.pythonanywhere.com/image"+i[0])

        return JsonResponse({'results': images}, status=status.HTTP_201_CREATED)


class ImageAPIView(APIView):
    def get(self, request, id):
        # Connect to MongoDB
        fs = gridfs.GridFS(database)
        # Retrieve the image data from MongoDB

        image_data = fs.get(ObjectId(id)).read()
        fileName = database.fs.files.find_one(
            {
                "_id": ObjectId(id)
            }
        )["name"]
        # get png or jpg part
        fileExtension = fileName.split(".")[-1]

        # Serialize the image data to return it as a response
        # return Response({'image_data': image_data})
        return HttpResponse(image_data, content_type=f'image/{fileExtension}')


class DropDownMenuData(APIView):
    def get(self, request, *args, **kwargs):

        # Get category, product, and brand values from request
        category = request.GET.get('category')
        product = request.GET.get('product')
        brand = request.GET.get('brand')

        # Define query object based on request parameters
        query = {}
        if category:
            query['category'] = category
        if product:
            query['product'] = product
        if brand:
            query['brand'] = brand

        # Query distinct categories, products, and brands based on query object
        categories = master_images_index.distinct('category', query)
        products = master_images_index.distinct('product', query)
        brands = master_images_index.distinct('brand', query)

        # Return response as JSON
        data = {
            'categories': categories,
            'products': products,
            'brands': brands
        }
        return JsonResponse(data)


class AdminAuth(APIView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'dowell admin' and password == 'logoscan admin':
            return JsonResponse({'authenticated': True})
        else:
            return JsonResponse({'authenticated': False})


class ReviewsView(APIView):
    def get(self, request, *args, **kwargs):
        # Extract the image URL from the request GET parameters
        image_url = request.GET.get('image_url')
        if not image_url:
            return JsonResponse({'error': 'Missing image URL.'}, status=400)

        # finding the db collections
        fs_files = database['fs.files']
        reviews_collection = database['reviews']

        # Extract the image ID from the URL
        image_id = image_url.split('/')[-1]

        # Find the document with the given ID in the fs.files collection
        file_doc = fs_files.find_one({'_id': ObjectId(image_id)})
        if not file_doc:
            return JsonResponse({'error': 'File not found.'}, status=404)

        # Get the category, product, and brand from the file document
        category = file_doc.get('category')
        product = file_doc.get('product')
        brand = file_doc.get('brand')

        # Find the reviews with the same category, product, and brand in the reviews collection
        reviews = []
        for review in reviews_collection.find({'category': category, 'product': product, 'brand': brand}):
            reviews.append({'username': review.get('username'),
                           'feedback': review.get('feedback')})

        # Return the list of reviews
        return JsonResponse({'reviews': reviews, 'category': category, 'product': product, 'brand': brand})


class UserReview(APIView):

    def post(self, request, *args, **kwargs):
        # Extract the review data from the request POST parameters
        category = request.POST.get('category')
        product = request.POST.get('product')
        brand = request.POST.get('brand')
        username = request.POST.get('username')
        feedback = request.POST.get('feedback')

        # Check if all required parameters are present
        if not all([category, product, brand, username, feedback]):
            return JsonResponse({'error': 'Missing review data.'}, status=400)

        reviews_collection = database['reviews']

        # Insert the review into the reviews collection
        review_doc = {
            'category': category,
            'product': product,
            'brand': brand,
            'username': username,
            'feedback': feedback
        }
        result = reviews_collection.insert_one(review_doc)

        # Return a success response
        return JsonResponse({'message': 'Review submitted successfully.', 'review_id': str(result.inserted_id)})
