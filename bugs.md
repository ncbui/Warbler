1. `user.is_following` and `user.is_followed_by` returns False, even if `user.follows` and `user.followed` confirms that user relationship exists

2. Add autoincrement to ID keys in the Messages and User models

3. FIXED: When editing the user, the password check built into edit template does not check for password match