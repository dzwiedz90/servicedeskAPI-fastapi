def validate_case(case_data):
    if type(case_data['content']) == str and type(case_data['severity']) == int and type(case_data['user_id']) == int:
        return True
    return False
