Loveefy

![Alt Text](./static/Screenshot%20from%202024-10-06%2017-55-16.png)

# API Documentation

## Base URL
`https://www.loveefy.africa/api`

---

## Endpoints

### 1. **Register User**
**Endpoint:** `/v1/auth/register`

**Method:** `POST`

**Description:** Registers a new user.


### 2. **Login User**
**Endpoint;** `/v1/auth/logins`

**Method:** `POST`

**Description:** Returns an access token with place id and preference id.(place and preference id is used to check whether the user has alread setup his/her profile).


### 3. ** Reset password **
**Endpoint:** `/v1/auth/reset_password_request`

**Method:** `POST`
**Request Body:** `Request body should contain the email address`
**Description:** `sends an OTP to the user email address`


### 4. ** Verify OTP **
**Endpoint:** `/v1/auth/reset_password/<token>`

**Method:** `POST`
**Request Params:** `contains the token`
**Description:** `Verifies the OTP`

### 5. ** Update Password**
**Endpoint:** `/v1/auth/update_password`
**Method:** `POST`

