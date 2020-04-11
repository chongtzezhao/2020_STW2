# 2020_STW2

I tried to build this around the database requirements and stuck to it as close as possible

DB schemas
```
User(UserID, Name, _Password, Email, Admin_ )
Question(QuestionID, Option1, Option2, Answer)
Attempt(AttemptID, UserID, QuestionID, Response)
CountAttempt(UserID, QuestionID, NumAttempts, _Correct, PracticeAttempts_ )
```

## Features
1. UserID login, rather than outsourcing to Google or using email (Email is collected for future password-reset versions)
2. Uses ReCaptcha v2 (visible) instead of v3 (invisible to users) to give users peace of mind that there are _some_ security considerations when making this website.
3. Does not store user password directly but stores a hashed version (reverse hashing is very hard!)

## Technologies used

### Backend
Google ReCaptcha, MySQL

### Frontend
HTML, CSS (Bulma), Javascript (Jquery)

### Integration
Python, flask, flask_sqlalchemy, wtforms

## Moving Forward

1. Python/Flask has many third-party libraries out there for security, database management, email etc. Use them.
2. Third-party CSS is good for building websites quickly, though you may have to sacrifice on flexibility.
3. 


## Future Versions
1. Use sockets to verify if a userID has been taken instead of having the user to submit a form? hmm
2. Admin rights to add and remove questions
3. Open-ended questions (haha)
4. Question tags.

