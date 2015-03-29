def create_restore_password_token(user):
    to_hex = lambda x: "".join([hex(ord(c))[2:].zfill(2) for c in x])
    password_len_2 = int(len(user.password)/2)
    return to_hex(user.password[:password_len_2])