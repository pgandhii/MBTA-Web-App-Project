# MBTA-Web-App-Project

This is the base repository for Web App project. Please read the [instructions](instructions.md) for details.

# Contributors
* Palak Gandhi
* Nidhi Rudraraju

# Project Overview

Our project is a web application that helps the user find the nearest MBTA station to a given place in Massacusetts, along with the weather. The app basically allows the user to enter an input, which is a location, coverts it to geographic coordinates using the Mapbox Geocoding API, identifies the closest MBTA stop through the MBTA APO, and displays details such as the nearest station's name, where it is accessible and the transit system. The core features are geomapping lookup, sorting distance using an API, reporting accesibility, and an app for the interface. Additionally, we added the feature to view the weather because it is important to know the weather and dress appropriately, especially in Massachusetts where the weather fluctuates a lot.

# Reflection

## Development Process

One major improvement in our workflow occurred after talking with the professor. Initially, we tried to build most of the project before testing anything, which made debugging almost impossible. After receiving guidance, we shifted to testing each function individually. This change helped us understand the data moving through the system, and it made our debugging process possible.

A challenge we faced was understanding how the APIs behave in edge cases. For example, Mapbox sometimes returns multiple possible locations, which confused our code and led to unexpected errors. We only figured this out after discussing it withe professor. Another issue was that our helper functions were not returning results when called from outside the test block, which turned out to be an indentation error and a function-calling mistake. Solving this required a great amount of patience and attention to detail while checking each part of the output. 

Additionally, Palak really found it a little challenging to understand HTML. It was already hard enough to understand python.

For problem-solving, we used a combination of sources, such as AI tools, a friend's help for an alternate set of eyes, the professor's guidance and API docs. This approach helped us understand errors and the logic behind the API responses, and even prepare us for the final project. If we were to do this project again, we would spend more time learning the APIS instead of immediately dividn into the code. This made us a little AI dependent to understand every step. However, the lectures in class really helped with the OpenWeather work.

# Teamwork & Work Division

At the start of the project, we planned our roles clearly and stuck to that plan throughout. We decided that Palak will work on building the Flask application, structuring the helper functions, writing the reflection, and organizing the final markup. On the other hand, Nidhi would handle the API components, including the Mapbox and MBTA integration, as well as adding the wow factors to the app. We decided this based on what was important for the person to practice for their final project. Since we set internal deadlines and communicated regularly, we did not face major coordination issues. Since we knew the timeline of all the processes, the other person could plan their work schedule accordingly. For next time, we would try working together in person on certain sections instead of working separately, as we believe that real-time collaboration could make troubleshooting even smoother and faster.

# Learning & Use of AI Tools

This project really deepened our understanding of backend development. We learned how APIs return structured JSON data, how to parse those responses in Python, and how to organize code using helper modules. We also became more comfortable with Flask routing, template rendering, and the structure of a functioning web application. However, debugging continues to be our area of improvement. We really spent a lot of time debugging.

We used ChatGPT as our primary AI tool. It helped us understand unfamiliar libraries, generate example code, and try to roubleshoot certain bugs. However, AI was not always sufficient. For example, initially Palak could not call the .env file, and when she asked AI for help, it did not work. Finally, she asked the professor, and got it to work. I think a limitation of AI is that at times it misses a few things, which result in output different than expected. It might also not be the best at reading the API's documentation and providing a solution, or maybe that was due to our prompting.

This project made it clear that understanding the underlying API behavior early on would have saved us time. In the future, we would review the official docs before coding to avoid avoidable debugging.
