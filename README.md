# Oauthkeeper
A simple, but functional, web application to manage HR contacts. Only lets authorised users to view certain contacts.

## Why was Oauthkeeper built?

The Mock Placements is an annual event conducted by the Placement Cell of SVCE. The objective of the event is to provide students with information about their strengths and weaknesses before they attend job interviews. This is achieved by inviting real HRs or recruiters to SVCE and then making them interview students in a, sort of, mock interview.

The Mock Placements are organised by FORESE (Forum for Economic Studies for Engineers), a college club consisting wholly of students. Inviting HRs to the college, as mentioned above, is one of the most important steps of the organisational process. However, this process can be chaotic and is inherently prone to problems. Some of the problems faced by the organisers are displayed below.

* The HR contact database would be maintained in an excel sheet. Students would have to search throughout the database for contacts that are assigned to them.
* HR contacts assigned to a certain student would, accidentally, be called by other students too in an overlapping of contacts.
* Students with a grudge againt another student would be able to intentionally muddle that student's contact list. Excel sheets have no log and, therefore, the students cannot be identified.
* Making note of the statuses of HRs was hard for students as they would have to note it all down somewhere. This would make it hard for students to update statuses and for EDs to keep track with what their team members are doing.

There was a need for a solution which would be able to potentially remove all of these problems.

## How does Oauthkeeper solve these problems?

This software has the following features:-

For the students who are calling the HRs,

* Students who are calling HRs will be given an account. Their username will be provided and the students must decide their own passwords.
![alt text](https://raw.githubusercontent.com/ForeseTech/Oauthkeeper/master/static/img/github-screenshots/login.png)
* Each student, once logged in, can only view contacts that have been assigned to them.
![alt text](https://raw.githubusercontent.com/ForeseTech/Oauthkeeper/master/static/img/github-screenshots/contacts.png)
* They have the option of adding contacts, provided the mobile number of the HR contact does not already exist in the database. This is taken care of by the solution.
![alt text](https://raw.githubusercontent.com/ForeseTech/Oauthkeeper/master/static/img/github-screenshots/addcontact.png)
* Students can also update information of contacts that are visible to them such as name, companu, number, email, address and, most importantly, status.


For the EDs who are managing these students,

* EDs can log into an administrator account. The username will be provided while they can decide the password that they use.
* EDs can view all contacts in the database and can edit permissions for each contact. That is, they can decide which students can view a particular contact.
* There are also features which help EDs to search for and filter contacts based on student-in-charge, mobile number, status and company name.
* EDs can also view statistics on the number of HRs in each stage (such as 'Not Called', 'Confirmed', etc etc).

This software potentially erases the problems that students were facing in the previous years.

## Tools and Technologies

* Flask Micro-framework
* Vim editor
* uWSGI standard/server

## Team

* Arjun Aravind - Design and Development
* Aravind B, Kriti G and Harshitha J - Inputs
