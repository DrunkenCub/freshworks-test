'use strict';
const axios = require('axios');

module.exports.hello = async (event) => {

  console.info(process.env.API);
  console.info(process.env.EMAIL);
  console.info(process.env.PASSWORD);
  let url = process.env.API + '/auth/login'
  let result = await axios.post(url, {
        email: process.env.EMAIL,
        password: process.env.PASSWORD
      });
  
  console.info(result.data.auth_token);
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': result.data.auth_token
  }
  
  url = process.env.API + '/feed/feed'
  result = await axios.post(url, event, {
    headers: headers
  });
  
  console.info(result.data.message);

  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        input: event,
        auth_token: result.auth_token
      },
      null,
      2
    ),
  };

  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  // return { message: 'Go Serverless v1.0! Your function executed successfully!', event };
};
