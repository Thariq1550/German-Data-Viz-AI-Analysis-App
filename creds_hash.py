import bcrypt
import json

credentials = {
    "user1": bcrypt.hashpw("pass1".encode(), bcrypt.gensalt()).decode(),
    "user2": bcrypt.hashpw("pass2".encode(), bcrypt.gensalt()).decode(),
	"user3": bcrypt.hashpw("pass3".encode(), bcrypt.gensalt()).decode(),
    "user4": bcrypt.hashpw("pass4".encode(), bcrypt.gensalt()).decode(),
	"user5": bcrypt.hashpw("pass5".encode(), bcrypt.gensalt()).decode(),
    "user6": bcrypt.hashpw("pass6".encode(), bcrypt.gensalt()).decode(),
	"user7": bcrypt.hashpw("pass7".encode(), bcrypt.gensalt()).decode(),
    "user8": bcrypt.hashpw("pass8".encode(), bcrypt.gensalt()).decode(),
	"user9": bcrypt.hashpw("pass9".encode(), bcrypt.gensalt()).decode(),
    "user10": bcrypt.hashpw("pass10".encode(), bcrypt.gensalt()).decode()
}

with open('creds.json', 'w') as file:
    json.dump(credentials, file)
