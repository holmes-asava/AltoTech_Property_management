# AltoTech_Property_management

The first version is designed specifically for hotels. Our core functionality is the work order management.

# Initial Superuser account

username : dev@gmail.com
password : test_password

# Docker

to setup the project, please run `docker-compose up `to build and start the server
`docker exec -it {image.name}/{image.id} bash` to shell into docker image to run other django command

# Url

In the browser visit
`http://0.0.0.0:8000/ap/` for swagger (`https://swagger.io/`)
`http://0.0.0.0:8000/admin/` for django admin

# Note

this source design follow requirement on Assignment section.and also on assumption that

- Guest can only GET and check their work order
- Maid and Supervisor have permission to update some field of Work order

# Assignment

Work orders can be created by multiple sources.
orders consists of the following field:

- Work Order Number (Unique field)
- Created By (User)
- Assigned To (User)
- Room
- Started At
- Finished At
- Type (Cleaning, Maid Request, Technician Request, Amenity Request)
- Status (Created, Assigned, In Progress, Done, Cancel)

each work order type have different rules as follows:
Cleaning

- can be created by Maid Supervisor only
- has its proprietary status (Cancelled by Guest)

Maid Request

- can be created by Maid supervisor only
- has a free-text “Description” field

Technician Request

- can be created by guest or supervisor
- has its proprietary types for indicating defect in the room (Electricity,Air Con, Plumbing, Internet)

Amenity Request

- can be created by guest only
- has its proprietary fields (Amenity Type, Quantity) that will be used fordeducting inventory later (inventory system is out of scope for this assignment)

Your assignment is the following:

- Write a Work Order module that has APIs to create and update the data.
- Make sure that your code follows the rule above strictly with a degree of extensibility
- Ensure that your module is tested and bullet-proof to the code changes mistakenly
  applied.
- Choose the repository (database) as you are convenient with. Only make sure that
  your database is scalable and data integrity is also a major concern for this system.
