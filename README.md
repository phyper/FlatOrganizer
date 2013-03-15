FlatOrganizer
=============
Installation

1. Import the project
2. Initialize the database by running the command "python manage.py syncdb" in terminal
3. Import the populate.py script by running the command "python manage.py shell" 
	>> "import populate"
4. Start the server by running the command "python manage.py runserver"
5. Open your browser and type in your IP address and port number (standard port number is 8000).
6. Append the /flats at the end of your ip + portnumber. Example with localhost: 127.0.0.1:8000/flats
7. You can either choose to create your own user or log in with some existing profiles: 
	Username1: madonna 		PasswordUser1: madonna
	Username2: rihanna 			PasswordUser2: rihanna
	Username3: gary			PasswordUser3: gary
8. To make the email function work you will need to add a SMTP server and provide a email host user and email host password in the settings.py on lines 174 - 178.