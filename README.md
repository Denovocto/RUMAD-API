# SSH RUMAD API
## About this project
The idea behind this project is to provide an interface for `rumad.uprm.edu:22` or rather the ssh-server hosted on the RUM server. Many of the students in the RUM campus colloquially refer to the server as 'putty', but putty is the tool used to connect to the server hosted in UPRM not the server itself. This project aims to 'technically' provide an alternative to the need to use putty to access `rumad.uprm.edu`. [Putty](https://www.putty.org/) is an ssh client and terminal emulator. The RUMAD API creates a client to send and receive data to/from `rumad.uprm.edu`. The RUMAD API can send different queries to gather different information like your GPA, current courses, courses taken, credits left, and course offer courses. Because this project still uses and depends on an active ssh connection, the information being transmitted to and from the server is encrypted using standard ssh2-protocol. This project aims to make a lot of future ideas & projects easier to build.
## How it works
For those of you inclined on the specifics of how can we connect to the server and gather the data without modifying the internal workings of the server, etc... 

The ssh-connection is created via the python library [Paramiko](http://www.paramiko.org) this library handles all the back and forth between the interface and the requests. 

As for the data extraction, the API uses regular expressions to recognize different patterns of text in the stream of data incoming from the paramiko library. For each field, a regular expression is created and compiled to fetch the different fields' data. Because paramiko outputs a byte-string when we receive data from the server, we need to decode the data, that's being received, into ASCII text, which is the intended encoding of the received text as most terminals use this by default to display text. Once the data received is decoded into ASCII text we need to strip any ANSI escape codes inside it, as UPRM uses them only for aesthetic purposes and oftentimes they interfere with our pattern matching and recognition. Once the data is polished, we can search for our precompiled Regex patterns on the text and save the results on a list. 
## Future goals 
Currently the API can recognize the names of the courses currently being taken, the names of the professors, the section number, the classroom and the period of these courses. 

**Our future goals are:**
- Using natural language processing to correctly detect all professor names.
- Adding a GUI interface for entering personal information.
- Build a command line interface parser for easy requests from the command line.
- Build a tool that uses the API to automatically fill out and do your course enrollment with a queue of interested courses, so that if one of the top priority courses is full, the program can recognize this and enroll the student with his/her's secondary option.
- adding compatibility with google calendar, and other API's so that students can enjoy the automatic filling of their enrolled courses on their calendars and such.
- Maybe building a web-app that uses the API in the backend such that no software download is needed to properly use the API
- Maybe an app for both IOS & Android
- Complete GUI for every possible menu in RUMAD

## FAQ's
1. **Q**: Is this legal? 
  
  **A**: Absolutely! The API only uses what's open to the public and accesible to the students using their credentials. Esentially it acts as a 'student' being used by another student. No backdoors or 'illegal' access used.
2. **Q**: Is this secure?
  
  **A**: The API is as secure as the ssh2-protocol itself, the API doesn't store any of the student's data. By being an open-source project we also benefit from complete transparency as to how everything works and how we handle your data. Additionally, anyone can contribute to make our project safer and more secure. So, yes it is safe. If you really are worried about how secure ssh is, look up the different encryption techniques used in the protocol, and decide for yourself.
3. **Q**: Why make such a project free and open-source?

  **A**: The project's intent is to make UPRM students' lives easier and more efficient by providing them with useful tools that make this possible. We don't need any recognition or money to be grateful to fulfill such a service. For years the enrollment system at UPR has been the same and with no GUI to back it up. The system is often-times slow, and even though we cannot alter the speed at which the server operates we can make the speed at which the student's access the server faster, frictionless and efficient. Some have tried to make and design better systems to be implemented in the server-side of things at UPRM but with the bureaucracy and politics that currently envelop the puertorican atmosphere, these efforts are yet to bear fruit. With the RUMAD API, we circumvent the need for asking for permission to mess with and modify the servers. It's a faster way (in terms of development) of achieving what many have dreamed of having, a central hub for everything related to student's academic progress. As to why make it open source, this will enable us to pass all the efforts made into making this project a reality to any student or person who desires to make it their own. The intent is to bring life into an old system by not changing how it operates.
