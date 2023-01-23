## To run the project
```
docker compose up
```
The app will be accessible at http://localhost:8000
## To run the tests
```
docker-compose run web python3 manage.py test
```

## API examples
### For Token Authentication
To retrieve the token go here:
http://localhost:8000/admin/authtoken/tokenproxy/ accessing with
```
username: clipboard
password: clipboard
```
Then, copy the only visible key and use it in place of YOUR_TOKEN in the upcoming examples
### For Basic Authentication
Just Use
```
clipboard:clipboard
```
in place of
```
username:password
```
### Create Employee
##### Token
```
curl http://localhost:8000/employees/ \
-H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN" \
-d '{"name":"Marco","salary":"145000","currency":"USD","department":"Engineering","sub_department":"Machine Learning"}'
```
#### Basic
```
curl http://localhost:8000/employees/ \
-H "Content-Type: application/json" \
-u username:password \
-d '{"name":"Marco","salary":"145000","currency":"USD","department":"Engineering","sub_department":"Machine Learning"}'
```

### Delete Employee
To manually test this, you can use the UUID returned by the employee creation OR you can access http://localhost:8000/admin/api/employee/ and copying one of the UUID that you see. Then replace the value chosen in place of EMPLOYEE_UUID in the url
#### Token
```
curl -X DELETE http://localhost:8000/employees/EMPLOYEE_UUID/ \
-H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN"
```
#### Basic
```
curl -X DELETE http://localhost:8000/employees/EMPLOYEE_UUID/ \
-H "Content-Type: application/json" \
-u username:password \
```
### Get Overall SS
#### Token
```
curl http://localhost:8000/ss/ \
-H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN"
```
#### Basic
```
curl http://localhost:8000/ss/ \
-H "Content-Type: application/json" \
-u username:password \
```
### Get Overall SS of employees with on_contract = True
#### Token
```
curl http://localhost:8000/ss/?on_contract=true \
-H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN"
```
#### Basic
```
curl http://localhost:8000/ss/?on_contract=true \
-H "Content-Type: application/json" \
-u username:password \
```
### Get Overall SS of employees with currency = X
#### Token
```
curl http://localhost:8000/ss/?currency=EUR \
-H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN"
```
#### Basic
```
curl http://localhost:8000/ss/?currency=EUR \
-H "Content-Type: application/json" \
-u username:password \
```
you can combine currency and on_contract as parameters

### Get SS by department
#### Token
```
curl http://localhost:8000/departments/ss/ \
-H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN"
```
#### Basic
```
curl http://localhost:8000/departments/ss/ \
-H "Content-Type: application/json" \
-u username:password \
```

### Get SS by department+sub_department combination
#### Token
```
curl http://localhost:8000/sub_departments/ss/ \
-H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN"
```
#### Basic
```
curl http://localhost:8000/sub_departments/ss/ \
-H "Content-Type: application/json" \
-u username:password \
```
## Brief summary on how me and my team would ensure high-quality code


1. Writing clean, readable, and well-commented code that adheres to established coding conventions and standards. We should use tools that make this as automatic as possible(linters)

2. Using version control (such as Git) to track changes to code and collaborate with other team members. In this project you won't find any initialized git repository just because it was a work of few hours and the result was to be shipped via zip.

3. Performing regular code reviews to catch and fix any bugs or issues early on.

4. Using automated testing to ensure that code is functioning correctly and that changes do not break existing functionality.

5. Keeping up to date with the latest technologies and tools to ensure that code is efficient and performant.

6. Continuously monitoring and measuring the performance of code to identify and fix any issues that may arise.

7. Documenting code and keeping documentation up to date.

8. Following security best practices to protect the code and data

By following these best practices, we can work together as a team to ensure that our code is high-quality, maintainable, and reliable.


## Notes on the implementation

- Django + Django Rest Framework + SQLLIte
- Rest Framework Token Authentication
- Each API uses serializers to validate both the input and the output
- Department and Subdepartment are entities instead of just fields in Employee table. This ensures that one can add as many departments and subdepartments as he wants, easily. Also we can have departments that share the same name for one or more of their subdepartments. We are only constraining the combination department+subdepartment to be unique.
- The endpoint to create employees is also able to create departments and subdepartments if they do not exist, which is very useful.
- Instead of doing an endpoint to address the on_contract = True requirement, it made much more sense to add it as a parameter in the overall_ss API. Currency has the same behaviour.
- All the endpoints are tested against unauthorized authentication.
- When running the first time ```docker compose up``` a command called initialize_app is called, filling the db with demo data
