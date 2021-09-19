import { AWS_CONFIG } from "utils/constants";
const isArray = (a: unknown) => {
  return Array.isArray(a);
};

const isObject = (o: unknown) => {
  return o === Object(o) && !isArray(o) && typeof o !== "function";
};

const toCamel = (s: string): string => {
  return s.replace(/([-_][a-z])/gi, ($1: string) => {
    return $1.toUpperCase().replace("-", "").replace("_", "");
  });
};

const toSnake = (s: string): string => {
  return s.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
};

export const keysToCamel = (o: any) => {
  if (isObject(o)) {
    const n: any = {};
    Object.keys(o).forEach((k: string) => {
      n[toCamel(k)] = keysToCamel(o[k]);
    });

    return n;
  } else if (isArray(o)) {
    return o.map((i: any) => {
      return keysToCamel(i);
    });
  }

  return o;
};

export const keysToSnake = (o: any) => {
  if (isObject(o)) {
    const n: any = {};
    Object.keys(o).forEach((k) => {
      n[toSnake(k)] = keysToSnake(o[k]);
    });
    return n;
  } else if (isArray(o)) {
    return o.map((i: any) => {
      return keysToSnake(i);
    });
  }
  return o;
};

export const getHeaders = (name: string) => {
  const cognito = `CognitoIdentityServiceProvider.${AWS_CONFIG.aws_user_pools_web_client_id}.${name}.accessToken`;
  return {
    Authorization: "Bearer " + localStorage.getItem(cognito),
    accept: "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
  };
};
