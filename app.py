from flask import Flask,render_template,request,url_for,jsonify, session,redirect,make_response
from werkzeug.utils import secure_filename
from waitress import serve

import os
import pymongo
from bson import ObjectId
import uuid
from pymongo import TEXT

import datetime 




from Product import products_bp  # Import the Blueprint


# Configure MongoDB connection
myclient = pymongo.MongoClient("mongodb+srv://ChiragRohada:s54icYoW4045LhAW@atlascluster.t7vxr4g.mongodb.net/test")

mydb = myclient["WhiteHouse"]


app = Flask(__name__)
app.secret_key = 'saidkjlmasd46531'


app.config['UPLOAD_FOLDER'] = 'uploads'  # Create a folder named 'uploads' in your project directory

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)





app.register_blueprint(products_bp)  # Register the Blueprint







# Function to generate a unique filename
def generate_unique_filename(original_filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = str(uuid.uuid4().hex[:6])
    _, file_extension = os.path.splitext(original_filename)
    return f"{timestamp}_{random_string}{file_extension}"


@app.route("/dcart")
def dcart():
    di= request.args.get('di', '')
    print(di)
    email = session.get('user_id')
    result = mydb.User.update_one(
        {'email': email},
        {'$pull': {'cart': di}}
    )
    return redirect(url_for('cart'))



@app.route("/cart")
def cart():

    if session.get('user_id'):

        id = request.args.get('id', '')

 
        email = session.get('user_id')
        name = session.get('name')


        items=0
    
        cart=mydb.User.find({'email':session.get('user_id')},{'cart':1,"_id":0})
        for i in cart:
            for j in i['cart']:
                
                items=items+1
        print(items)

        if id:


            result1=mydb.User.find({"email":email},{"cart":1})
            for i in result1:
                for j in i["cart"]:
                    if j==id:
                        return {"res":"ok"}

            result = mydb.User.update_one(
            {'email': email},
            {'$push': {'cart': id}}
            )
        cart=[]
        # Find the document using the ObjectId
        product1=mydb.User.find({'email':email},{'cart':1,"_id":0})
        for i in product1:
            for j in i['cart']:
                object_id = ObjectId(j)
                product = mydb.mens.find_one({'_id': object_id})
                cart.append(product)
    else:
        return redirect(url_for('login'))
    



            


    

    # result1=mydb.Mens.find({})
    return render_template("cart.html",cart=cart,items=items)




@app.route("/logout")
def logout():
    if 'user_id' in session:
        username = session.pop('user_id')
        name = session.pop('name')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

    

@app.route("/")
def index():
    


    items=0
    if 'user_id' in session:
        login="logout"
        
        cart=mydb.User.find({'email':session.get('user_id')},{'cart':1,"_id":0})
        for i in cart:
            for j in i['cart']:
                
                items=items+1
        

        
    else:
        login="login"
    Trends=mydb.mens.find({"Trending":1}).limit(4)
    mens=mydb.mens.find({"Type":"Mens"}).limit(4)
    womens=mydb.mens.find({"Type":"Womens"}).limit(4)
    



    Trending=[]
    Mens=[]
    Womens=[]
    for i in Trends:
        Trending.append(i)
    for i in mens:
        Mens.append(i)
    
    for i in womens:
        Womens.append(i)

    response = make_response(render_template("index.html",Trending=Trending,Mens=Mens,Womens=Womens,login=login,items=items))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    

        

        

    return response

@app.route("/sign_up",methods = ['POST', 'GET'])
def sign_up():
    global n
    
    
    try:

        if request.method == 'POST':
            user_name=request.form['name']
            user_password=request.form['password']
            user_email=request.form['email']
            user_mobile=request.form['mobile']
            # user_password = bcrypt.generate_password_hash(user_password)
      

        
   
            mycol = mydb['User']
            x=mycol.find_one({"email":user_email})
            print(x)
            if x:
                return render_template('sign-up.html',error="email aleardy registered")
            else:
                query = {
                    'name': user_name,
                'email': user_email,
            'mobile': user_mobile,
            'password': user_password,
            'cart':[],
            'liked_products':[]
            
                    }   
                mydb.User.insert_one(query)
                return redirect(url_for('login'))

            
                
                
        
          

          
       
         
    except Exception as e:
        print("hello")

    return render_template("sign-up.html",error="")


@app.route("/admin_index")
def admin_index():
    return render_template("admin_index.html")



@app.route("/admin_login",methods = ['POST', 'GET'])
def admin_login():
    
    
    error=""

    if request.method == 'POST':
      email=request.form['email']
      password=request.form['password']
      


      try:
          mycol = mydb['Admin']
          x= mycol.find_one({"email":email})
           
          if(x['pass'] == password):
            
            session['admin_id']=x["email"]
            session['name']=x["name"]

            return redirect(url_for('admin_index'))
          else:
            error="invalid credential"
            return render_template('admin_login.html',error=error)
      except:
          return render_template('admin_login.html',error=error)
    else:
       return render_template('admin_login.html',error=error)



@app.route("/login",methods = ['POST', 'GET'])
def login():
    
    
    error=""

    if request.method == 'POST':
      email=request.form['email']
      password=request.form['password']
      


      try:
          mycol = mydb['User']
          x= mycol.find_one({"email":email})
          if x:
              
           
            if(x['password'] == str(password)):
            
                session['user_id']=x["email"]
                session['name']=x["name"]

                return redirect(url_for('index'))
            else:
                error="invalid credential"
                return render_template('login.html',error=error)
          else:
              return render_template('login.html',error="Invalid Credential")
      except:
          return render_template('login.html',error=error)
    else:
       return render_template('login.html',error=error)




@app.route("/search")
def search():
    search = request.args.get('search', '')
    print(search)
    query = {"search": {"$regex": search, "$options": 'i'}}
    search2= list(mydb.Search.find(query,{"_id":0}))
    
    return  jsonify(search2)







@app.route('/like/<product_id>', methods=['POST','GET'])
def like_product(product_id):
    # Check if the user has already liked the product


    if session.get('user_id'):


 
        email = session.get('user_id')
        name = session.get('name')


        product1=list(mydb.User.find({'email':email},{'liked_products':1,"_id":0}))
        print(product1)
        

        
        if product_id not in product1[0]['liked_products']:
            mydb.mens.update_one({'_id': ObjectId(product_id)}, {'$inc': {'like': 1}})
            mydb.User.update_one({'email': email}, {'$addToSet': {'liked_products': product_id}})
        return {"res":"ok"}

        
        # if id:
        #     result = mydb.User.update_one(
        #     {'email': email},
        #     {'$push': {'cart': id}}
        #     )
        # cart=[]
        # # Find the document using the ObjectId
        # product1=mydb.User.find({'email':email},{'cart':1,"_id":0})
        # for i in product1:
        #     for j in i['cart']:
        #         object_id = ObjectId(j)
        #         product = mydb.mens.find_one({'_id': object_id})
        #         cart.append(product)
    else:
        return {"res":"error"}








@app.route("/fashion")
def fashion():
    if 'user_id' in session:
        login="logout"
    else:
        login="login"

    #Getting Paramters For Filter
    name = request.args.get('name', '')
    category = request.args.get('category', '')

    brand = request.args.get('brand', '')
    type = request.args.get('type', '')
    material = request.args.get('material', '')
    search = request.args.get('search', '')
    print(search)


    if search:
        mydb.Search.insert_one({'search':search})
    







    query = {
        "$and": [
            {"Name": name} if name else {},
            {"Category": category} if category else {},
            {"Brand": brand} if brand else {},
            {"Material": material} if material else {},
            {"Type": type} if type else {}  ,
            {"$text": {"$search": search.lower()}}  if search else {} 
                  ]
    }
    filtered_products = list(mydb.mens.find(query))

    filter=mydb.filter.find()
    Filter=[]
    for i in filter:
        Filter.append(i)

    dress=mydb.mens.find()
    Dress=[]

    for i in dress:
        Dress.append(i)
    
    # print(Dress)


    response = make_response(render_template("fashion.html",Filter=Filter,Dress=filtered_products,login=login,type=type ))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response
    






if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)