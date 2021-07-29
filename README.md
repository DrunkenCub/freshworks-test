# freshworks-test



## How to run the application

Run following after editing the AWS keys in docker-compose.yml in the root.

``` docker-compose up ```



## How to run backend tests

navigate to ./server and run following

`` nosetests ``


## How to deploy the scheduler

navigate to ./scheduler and run following (Make sure AWS config is done and severless framework is installed globally)

``sls deploy ``
