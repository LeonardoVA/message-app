# message-app
Code for a message sending application.

Current state:  

python file can be run via command line in client or server mode.  

-h for options, note a client can only be run once a server is up and running.  

If the file is run with no arguments it trys to connect to server, failing that it becomes the server host. So the next run with automatically connect to the sever as a client. This should be used by default in production as it takes away user error of chosing the wrong mode.   

Once run and client/server set up: the client/server can read what the other types, the messages are sent over a socket. This turns the console into a makeshift chat client, This works locally at the moment on port 55555, so you can have 2 shells communicating.  

TODO:  
Get the chat client working for two different computers.  
Ensure the Client works cross platform: test linux/windows.  
Encrypt the messages with rsa encryption.  
Investigate requirement of using AES/RSA hybrid encryption.  
Investigate feasability of Unit testing using different computers.  
