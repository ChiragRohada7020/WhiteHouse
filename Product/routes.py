# products/routes.py
from flask import Flask,render_template,request,url_for,session
from werkzeug.utils import secure_filename
import os
import pymongo
from bson import ObjectId
import uuid
import datetime 
from bson import ObjectId  # Import ObjectId from bson module


# Configure MongoDB connection
myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["WhiteHouse"]





from . import products_bp




# Function to generate a unique filename
def generate_unique_filename(original_filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = str(uuid.uuid4().hex[:6])
    _, file_extension = os.path.splitext(original_filename)
    return f"{timestamp}_{random_string}{file_extension}"

@products_bp.route("/add_product",methods=['GET', 'POST'])
def add_product ():
    if request.method == 'POST':
        # Retrieve product details from the form
        name = request.form.get('name')
        description = request.form.get('description')
        Barcode = request.form.get('barcode')
        category = request.form.get('category')
        brand = request.form.get('brand')
        material = request.form.get('material')
        type= request.form.get("type")
        Image_Url= ""
        Image_Url2=""
        Image_Url3=""




        image = request.files['image']
        image2 = request.files['image2']
        image3 = request.files['image3']
        if image and image2 and image3:
            filename = generate_unique_filename(image.filename)
            filename2 = generate_unique_filename(image2.filename)
            filename3 = generate_unique_filename(image3.filename)
            Image_Url=filename
            Image_Url2=filename2
            Image_Url3=filename3
            image.save(os.path.join(products_bp.config['UPLOAD_FOLDER'], filename))
            image2.save(os.path.join(products_bp.config['UPLOAD_FOLDER'], filename2))

            image3.save(os.path.join(products_bp.config['UPLOAD_FOLDER'], filename3))

        else:
            Image_Url = None

        

        # Insert the product into the MongoDB database
        product = {
            'Name': name,
            'Description': description,
            'Category': category,
            'Brand': brand,
            'ImageUrl': [Image_Url,Image_Url2,Image_Url3],
            'Material':material,
            "Barcode":Barcode,
            "Type":type,
            "Trending":1
        }   
        mydb.mens.insert_one(product)


    filter = mydb.filter.find()
    Filter=[]
    for i in filter:
        Filter.append(i)
    print(Filter)

        # Redirect to the index page after adding the product

    return render_template("add_product.html",Filter=Filter)


#Getting Each Product
@products_bp.route("/fashion/<name>/<pid>")
def Each_product(name,pid):
    if 'user_id' in session:
        login="logout"
    else:
        login="login"
        # Convert the product_id string to ObjectId
    object_id = ObjectId(pid)

    # Find the document using the ObjectId
    product = mydb.mens.find_one({'_id': object_id})


    return render_template("each_product.html",product=product,login=login)




    
