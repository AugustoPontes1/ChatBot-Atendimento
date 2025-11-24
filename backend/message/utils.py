

class Verifier:
    """ 
    This class verifies the data type coming from the requests
    """
    def verify_user(request, user):
        if isinstance(request.data, dict):
            user_verified = request.data.get(user)

        if not user_verified:
            user_verified = request.headers.get('X-User') or \
                            request.query_params.get('user') or \
                            request.session.get('active_user')
        return user_verified

    def verify_user_text(request, text):
        if isinstance(request.data, dict):
            text_verified = request.data.get(text)

        if not text_verified:
            text_verified = request.query_params.get('text') or\
                    (request.data.get(text) 
                     if isinstance(request.data, dict) 
                     else None)
        return text_verified
