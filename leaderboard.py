from app import db, User, Question, Attempt, CountAttempt

def get_rankings():
    try:
        questions = Question.query.all()
    except OperationalError:
        questions = Question.query.all()
    users = User.query.all()
    rankings = []
    for user in users:
        user_total_correct = 0
        user_total_attempts = 0
        user_practice = 0
        user_total_score = 0
        for question in questions:
            record = CountAttempt.query.filter_by(UserID=user.UserID, QuestionID=question.QuestionID).first()
            if record:
                user_total_correct += record.Correct
                user_total_attempts += record.NumAttempts
                user_practice += record.PracticeAttempts 
                user_total_score += record.Correct * 9 - record.NumAttempts
        user_total_score += user_practice*0.5
        else:
            user_total_score = 0
        rankings.append([user_total_score, user.Name, user_total_correct,
                        user_total_attempts, user_practice])
    rankings.sort(reverse=True)
    
    return rankings

