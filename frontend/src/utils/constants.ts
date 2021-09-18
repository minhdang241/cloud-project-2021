/* eslint-disable camelcase */

export const API = {
  BACKEND: process.env.REACT_APP_BACKEND ?? "",
};

export const AWS_CONFIG = {
  aws_cognito_region: process.env.REACT_APP_AWS_REGION ?? "",
  aws_user_pools_id: process.env.REACT_APP_AWS_COGNITO_POOL_ID ?? "",
  aws_user_pools_web_client_id: process.env.REACT_APP_AWS_COGNITO_APP_ID ?? "",
};
