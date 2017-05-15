# Multi-Tenant, Cloud Scale, Multi-AZ SaaS App using Amazon Web Services
## Languages and frameworks used:
#### Backend: Python, Flask framework.
#### Database: MySQL
#### Front-end: HTML 5, javascript, Angular.js

#### Application Login page URI:
http://ec2-52-10-224-75.us-west-2.compute.amazonaws.com/login.html

VPC name: personal, located in Oregon region  
AZs:  us-west-2a, us-west-2b  

#### Tenants:  
Harshit Agarwal  
Kaushik Shingne  
Binoy Michael Prakash  
Apoorva Maheshwari  

#### Load balancer config:
Port 80: Binoy's target group  
Port 81: Kaushik's target group  
Port 82: Harshit's target group  
Port 83: Apoorva's target group  

#### Schema info:    
tenant_data: table which stores the incoming data for all the tenants, tenant's columns are mapped using tenant_field table.  
tenant_field: table storing field name, type, column number, tenant id, and table name  
tenant_table: stores each tenants' table information    
t-binoy: Binoy's table, contains 1 custom comment: TEST-PASSED    
t-harshit: Harshit's table, contains 1 custom comment : CHALLENGE  
t-apoorva: Apoorva's table, contains no custom comments, only the common grading attributes.  
t-kaushik: Kaushik's table, contains 2 custom comments: IMPROVEMENTS, DRAWBACKS.  

#### Data Multi-tenancy:  
Each tenant table has 3 common graading attributes namely MARKS, COMPLETE OR INCOMPLETE and COMMENTS. Besides that, Binoy also has a custom field TEST-PASSED, Kaushik has 2 custom fields DRAWBACKS, IMPROVEMENTS, and Harshit has one custom field CHALLENGES.  
The schema can be extended freely to add/modify fields for specific tenants with minimal changes to the code.  

### NOTE: I've used my friends AWS account for this project, so the Demonstration video contains the name Sanjot Saini on AWS console. I've done complete implementation from scratch.   

