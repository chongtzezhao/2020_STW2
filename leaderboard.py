from app import db, User, Question, Attempt, CountAttempt

def get_rankings():
    users = User.query.all()
    questions = Question.query.all()
    rankings = []
    for user in users:
        user_total_correct = 0
        user_total_attempts = 0
        user_practice = 0
        for question in questions:
            record = CountAttempt.query.filter_by(UserID=user.UserID, QuestionID=question.QuestionID).first()
            if record:
                user_total_correct += record.Correct
                user_total_attempts += record.NumAttempts
                user_practice += record.PracticeAttempts 
        if user_total_attempts>0:
            user_total_score = (user_total_correct /
                                user_total_attempts) + 0.1*user_practice
        else:
            user_total_score = 0
        rankings.append([user_total_score, user.Name, user_total_correct,
                        user_total_attempts, user_practice])
    rankings.sort(reverse=True)
    
    return rankings

