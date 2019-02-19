# Oauthkeeper
A simple, but functional, web application to manage HR contacts. Only lets authorised users to view certain contacts.

## Why was Oauthkeeper built?

The Mock Placements is an annual event conducted by the Placement Cell of SVCE. The objective of the event is to provide students with information about their strengths and weaknesses before they attend actual campus placements and job interviews. This is achieved by inviting real HRs or recruiters to SVCE. These recruiters will the interview students and put them through GDs, giving the students some experience on how the process works.

The Mock Placements is organised by FORESE (Forum for Economic Studies for Engineers), a college club run wholly by students. Inviting HRs to the college, as mentioned above, is one of the most important steps of the organisational process. This is done by allocating several HR contacts to specific students and letting them call and invite the HRs to the Mock Placements.

However, this process can be chaotic and is inherently prone to problems. Some of the problems that were faced by the organisers are displayed below.

* The HR contacts database was maintained in an excel sheet. Students would have to manually search the database for the contacts that were assigned to them.
* Sometimes, a student would accidentally call contacts that were assigned to another students. This results in overlapping of contacts. This also leads to HRs and recruiters getting annoyed by getting calls from multiple students.
* Students with a grudge against another student would be able to intentionally muddle that student's contact list. Excel sheets have no log and, therefore, it would be difficult to identify such students.
* Making note of the statuses of HRs for the event (Confirmed, Rejected, Call Postponed, etc) was hard for students as they would have to note it all down somewhere. This would make it hard for the organisers to keep track of the number of HRs coming for the event and their details.

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


For the seniors who are managing these students,

* Seniors can log into an administrator account. The username will be provided while they can decide the password that they use.
* Seniors can view all contacts in the database and can edit permissions for each contact. That is, they can decide which students can view a particular contact.
* There are also features which help these seniors to search for and filter contacts based on student-in-charge, mobile number, status and company name.
* Seniors can also view statistics on the number of HRs in each stage (such as 'Not Called', 'Confirmed', etc etc).
* Seniors can also generate CSV files of the data present in the SQL database. These files can later be opened in Excel.

This software potentially erases the problems that students were facing in the previous years.

## Tools and Technologies

* Flask (Python Web Micro-Framework)
* MySQL Server
* Vim editor
* uWSGI standard/server

## Team

* Arjun Aravind - Design and Development
* Aravind B, Kriti G and Harshitha J - Inputs
