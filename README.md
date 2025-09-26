Only clone Hazim and not the main as the main rn doesn't work on env, will try to fix soon 
pls use env to run the debug and use (  pip install -r requirements.txt  ) when on env to install the necessary libraries for the website to work on ur end 
If u have issues on env use this (  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process  ) then  this (   .\env\Scripts\Activate  ) to activate ur env 


$env:FLASK_APP="main.py"

flask db upgrade

flask db migrate -m ""