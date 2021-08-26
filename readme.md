# Mesos/Marathon front-end API

This is a **proof-of-concept** Mesos/Marathon front-end API to orchestrate applications.

## How to run

The API is provided as a Flask app in a Docker image, which has been added
in the docker compose file.

To run the API, run:
docker-compose up --build --force-recreate

To use the app:
- Example to start a shell command:
curl -X POST  0.0.0.0:5000/application --header "Content-type: application/json" --data @start.json
- Example to start a container:
curl -X POST  0.0.0.0:5000/application --header "Content-type: application/json" --data @start_container.json
- Example to list started applications:
curl -X GET  0.0.0.0:5000/application --header "Content-type: application/json"
- Example to show an application status:
curl -X GET  0.0.0.0:5000/application/hello --header "Content-type: application/json"
- Example to stop an application:
curl -X DELETE  0.0.0.0:5000/application/hello --header "Content-type: application/json"
- Example of a bad request:
curl -X POST  0.0.0.0:5000/application --header "Content-type: application/json" --data @bad.json

You can find an OpenAPI specification in openapi_spec.txt

## Potential improvements
- Add functional tests
- Provide better serialization and validation of the input with a library such as Marshmallow.
- As this API is just a simplified front-end for the Marathon API, we could gradually
add more functionality provided by the Marathon API, such as more options and more endpoints
(e.g. ability to modify existing deploymensts). Eventually we could also add features not provided by Marathon,
 which would make our API more useful.
- Currently our API mostly just forwards the response from Marathon,
we could filter it and hide details.
- Add authentication and authorization to use the API
- Add authentication and authorization between our API and Mesos/Marathon.
- The Flask app should run on a production-grade server such as Apache httpd, instead of the Flask development server
- For extra security we could configure SELinux on the host server

## Known issues
- A curious issue I encountered is that if the directory from where you run "docker-compose up" is called
'marathon_exercise', it won't work. I think it has to do with Marathon using the name of the current
directory as an option and getting confused. When I changed the name of the directory it worked.
