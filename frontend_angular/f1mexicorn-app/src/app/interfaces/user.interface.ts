export interface GoogleAuthRequest {
  auth_token: string;
}

export interface AuthResponse {
  name: string;
  email: string;
  access_token: {
    access_token: string;
  } | string;
}

export interface User {
  userId: number;
  name: string;
  email: string;
}