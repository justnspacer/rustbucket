RustyUser Application

# Program.cs

This file contains the main entry point and configuration for the VerifyUser application. It sets up various services, middleware, and authentication for the application.

## Configuration

- `IpRateLimitOptions` and `IpRateLimitPolicies` are configured using the provided configuration file.
- CORS policy is set to allow requests from `https://localhost:5173/`.
- JWT authentication is configured with a symmetric security key.
- Swagger is configured with API documentation and JWT token security definition.

## Role Management

- Role manager is used to create roles if they don't exist.
- Roles "Admin", "Manager", "User", and "Guest" are created if they don't exist.

## Admin Creation

- User manager is used to create an admin user if it doesn't exist.


## UserService.cs

Methods:
1.	GetAllAsync(): Retrieves all users asynchronously and returns a list of UserDto objects representing the users.
2.	GetByIdAsync(string id): Retrieves a user by their ID asynchronously and returns a UserDto object representing the user, or null if not found.
3.	DeleteAsync(string id): Deletes a user asynchronously based on the provided ID. Returns an IdentityResult indicating the success or failure of the delete operation.
4.	AddRoleToUserAsync(AddRoleRequest model): Adds a role to a user asynchronously. Takes an AddRoleRequest model containing the user ID and role name. Returns an IdentityResult indicating the success or failure of the add role operation.

## AuthService.cs

Methods:
1.	RegisterAsync(UserRegister model): Registers a new user asynchronously. Takes a UserRegister model containing user registration details. Returns an IdentityResult indicating the success or failure of the registration operation.
2.	LoginAsync(UserLogin model): Logs in a user asynchronously. Takes a UserLogin model containing user login details. Returns an AuthResult object representing the result of the login operation.
3.	UpdateAsync(string id): Updates a user asynchronously based on the provided ID. Returns an IdentityResult indicating the success or failure of the update operation.
4.	ConfirmEmailAsync(ConfirmEmailRequest model): Confirms a user's email asynchronously. Takes a ConfirmEmailRequest model containing the user's ID and token. Returns an IdentityResult indicating the success or failure of the confirm email operation.
5.	LogoutAsync(): Logs out the current user asynchronously. Returns an IdentityResult indicating the success or failure of the logout operation.
