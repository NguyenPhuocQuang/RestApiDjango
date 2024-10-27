
HOW TO RUN PROJECT

    1. Create ENV
       py  -m venv env
    
    2. Activate ENV
       env\Scripts\activate
    
    3. Install libaries
       pip install -r requirements.txt
    
    4. python  manage.py migrate

    5. Run project 
        python manage.py runserver

    6. Run TestCase
      python manage.py test todos




HOW TO USE API

    1. Create user

      curl --location 'http://127.0.0.1:8000/api/users' \
         --header 'Content-Type: application/json' \
         --data '{
            "username":"user",
            "password":"user"

         }'
    
    2. Create token

      curl --location 'http://127.0.0.1:8000/api/token' \
            --header 'Content-Type: application/json' \
            --data '{
               "username":"user",
               "password":"user"

         }'

    3. Get todos.
         curl --location 'http://127.0.0.1:8000/api/todos' \
               --header 'Authorization: "token"
     
    
      