from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()
import requests
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)

items = [
  {
    "name": "Water Bottle",
    "price": 20
  },
  {
    "name": "Cola",
    "price": 25
  }
]

@app.get('/get-allItems')
def get_items():
  try:
    return jsonify({"items": items}), 200
  except Exception as e:
    return jsonify({"error": "Failed to fetch items"}), 500
  

@app.post('/add-items')
def add_items():
  try:
    body = request.get_json()
    if not body:
      raise BadRequest("No JSON data provided")

    required_fields = ['name', 'price']
    if not all(field in body for field in required_fields):
      raise BadRequest("Missing required fields: name, price")
    
    if not isinstance(body['price'], (int, float)) or body['price'] < 0:
      raise BadRequest("Price must be a positive number")
    
    items.append(body)
    return jsonify({"message":"Items added","items":items}), 201
  except BadRequest as e:
    raise e
  except Exception as e:
    return jsonify({"errror":"Failed to add item"}), 500
  

@app.get('/get-item/<string:name>')
def get_item_by_name(name):
    try:
        if not name:
            raise BadRequest("Name parameter required")
        
        for item in items:
            if name.lower() == item['name'].lower():
                return jsonify(item), 200
        raise NotFound(f"Item '{name}' not found")
    except (BadRequest, NotFound) as e:
        raise e
    except Exception:
        return jsonify({"error": "Failed to fetch item"}), 500
    

@app.get('/get-item')
def get_item_by_params():
    try:
        name = request.args.get('name')
        if not name:
            raise BadRequest("Query parameter 'name' is required")
        
        for item in items:
            if name.lower() == item['name'].lower():
                return jsonify(item), 200
        raise NotFound(f"Item '{name}' not found")
    except (BadRequest, NotFound) as e:
        raise e
    except Exception:
        return jsonify({"error": "Failed to fetch item"}), 500
    

@app.put('/update-item')
def update_item():
    try:
        body = request.get_json()
        if not body:
            raise BadRequest("No JSON data provided")
        
        required_fields = ['name', 'price']
        if not all(field in body for field in required_fields):
            raise BadRequest("Missing required fields: name, price")
        
        for i, item in enumerate(items):
            if item['name'].lower() == body['name'].lower():
                items[i]['price'] = body['price']
                return jsonify({"message": "Item updated", "item": items[i]}), 200
        
        raise NotFound(f"Item '{body['name']}' not found")
    except (BadRequest, NotFound) as e:
        raise e
    except Exception:
        return jsonify({"error": "Failed to update item"}), 500
    

@app.delete('/delete-item/<string:name>')
def delete_item(name):
  try:
    #name = request.args.get('name')
    if not name:
       raise BadRequest("Query Parameter 'name' is required")
    for i, item in enumerate(items):
      if name.lower() == item['name'].lower():
        deleted_item = items.pop(i)
        return jsonify({'message':"Item deleted", "deleted": delete_item}), 200
      
    raise NotFound(f"Item '{name}' not found")
  except (BadRequest, NotFound) as e:
    raise e
  except Exception:
    return jsonify({"error": "Failed to delete Item"}), 500


@app.get('/random-user')
def get_random_user():
  try:
     url = "https://api.freeapi.app/api/v1/public/randomusers/user/random"
     response = requests.get(url, timeout=10)
     response.raise_for_status()

     data = response.json()
     if data.get("success") and "data" in data:
        user = data["data"]
        return jsonify({
           "Usernamme":user["login"]["username"],
           "Country": user["location"]["country"],
           "email": user["email"]
        }), 200
     raise Exception("Invalid API Response")
  except requests.RequestException as e:
     return jsonify({"error": "Failed to fetch user data"}), 500
  except Exception as e:
     return jsonify({"error": "Failed to fetch user"}), 500
  

@app.get('/movie/<string:movie_name>')
def get_movie_data(movie_name):
   try:
      api_key = os.getenv('OMDB_API_KEY')
      if not api_key:
         return jsonify({"error": "OMDB API Key missing"}), 500
      
      url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
      response = requests.get(url, timeout=10)
      response.raise_for_status()

      data = response.json()
      if data.get("Response") == "True":
         return jsonify({
            "title": data["Title"],
            "year": data["Year"],
            "imdb_rating": data["imdbRating"],
            "plot": data["Plot"]
         })
      return jsonify({"error": "Movie not found"}), 404
   except Exception as e:
      return jsonify({"error": f"Movie API error: {str(e)}"}), 503
   

@app.get('/weather/<city>')
def get_weather(city):
   try:
      api_key = os.getenv('OPENWEATHER_API_KEY')
      if not api_key:
         return jsonify({"error": "OpenWeather API Key missing"}), 500
      
      url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
      response = requests.get(url, timeout=10)
      response.raise_for_status()

      data = response.json()
      if data.get("cod") == 200:
         return jsonify({
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
         }), 200
      return jsonify({"error": "City not found"}), 404
   except Exception as e:
      return jsonify({"error": f"Weather API error: {str(e)}"}), 503
   

#Country in code e.g. us, gb, in
@app.get('/news/<country>')
def get_news(country):
    try:
        api_key = os.getenv('NEWS_API_KEY')
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey={api_key}"

        res = requests.get(url)
        data = res.json()
        if data.get("status") == "ok":
          articles = [
            {"title": a["title"], "url": a["url"]}
            for a in data["articles"][:5]
          ]
          return jsonify({"articles": articles}), 200
    except Exception as e:
       return jsonify({"error": f"News API error: {str(e)}"}), 500
    

@app.post('/create-post')
def create_post():
  try:
    body = request.get_json()
    if not body:
      raise BadRequest("No JSON data provided")
    res = requests.post(os.getenv('BASE_URL'), json=body, timeout=10)
    return jsonify({"status": "Post Created", "response": res.json()}), 201
  except Exception as e:
    return jsonify({"error": f"Failed to create post: {str(e)}"}), 500

@app.put('/update-post/<int:post_id>')
def update_post(post_id):
  try:
    body = request.get_json()
    if not body:
      raise BadRequest("No JSON data provided")
    res = requests.put(f"{os.getenv('BASE_URL')}/{post_id}", json=body, timeout=10)
    try:
      response_data = res.json()
    except ValueError:
      response_data = {"message": "No JSON response from API"}
    return jsonify({"status": "Post Updated", "response": response_data}), 200
  except Exception as e:
    return jsonify({"error": f"Failed to update the post: {str(e)}"}), 500


@app.delete('/delete-post/<int:post_id>')
def delete_post(post_id):
  try:
    res = requests.delete(f"{os.getenv('BASE_URL')}/{post_id}", timeout=10)
    if res.status_code == 200:
      return jsonify({"status": "Post Deleted"}), 200
    return jsonify({"error": "Failed to delete post"}), 500
  except Exception as e:
    return jsonify({"error": f"Failed to delete post: {str(e)}"}), 500
        