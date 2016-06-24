from system.core.model import Model

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def create_user(self, user):
		is_admin = 0
		sql = "select count(*) as count from users"
		if self.db.query_db(sql)[0]["count"] == 0:
			is_admin = 1

		pwd = self.bcrypt.generate_password_hash(user["pwd"])

		sql = "insert into users(email, first_name, last_name, password, created_at, updated_at, is_admin) " \
			"values(:email, :first_name, :last_name, :pwd, NOW(), NOW(), :is_admin)"
		data = {
			"email": user["email"],
			"first_name": user["first_name"],
			"last_name": user["last_name"],
			"pwd": pwd,
			"is_admin": is_admin
		}
		user_id = self.db.query_db(sql, data)

		sql = "select * from users where id = :id"
		data = {
			"id": user_id
		}
		result = self.db.query_db(sql, data)

		return { "status": True, "user": result[0] }

	def login_user(self, info):
		sql = "select * from users where email = :email"
		data = {
			"email": info["email"]
		}
		result = self.db.query_db(sql, data)

		errors = []

		if result == None or len(result) == 0:
			errors.append("Invalid email")
			return { "status": False, "errors": errors }

		if self.bcrypt.check_password_hash(result[0]["password"], info["pwd"]):
			return { "status": True, "user": result[0] }

		errors.append("Invalid password")
		return { "status": False, "errors": errors }

	def update_user_info(self, user_info):
		sql = "update users set email = :email, first_name = :first_name, last_name = :last_name, " \
			"updated_at = NOW(), is_admin = :is_admin where id = :id"
		data = {
			"email": user_info["email"],
			"first_name": user_info["first_name"],
			"last_name": user_info["last_name"],
			"is_admin": user_info["is_admin"],
			"id": user_info["user_id"]
		}
		self.db.query_db(sql, data)

		return { "status": True }

	def update_user_password(self, user_password):
		pwd = self.bcrypt.generate_password_hash(user_password["pwd"])

		sql = "update users set password = :pwd, updated_at = NOW() where id = :id"
		data = {
			"pwd": pwd,
			"id": user_info["user_id"]
		}
		self.db.query_db(sql, data)

		return { "status": True }

	def update_user_desc(self, user_desc):
		sql = "update users set description = :desc, updated_at = NOW() where id = :id"
		data = {
			"desc": user_info["desc"],
			"id": user_info["user_id"]
		}
		self.db.query_db(sql, data)

		return { "status": True }

	def delete_user_by_id(self, user_id):
		sql = "delete from users where id = :id"
		data = {
			"id": user_id
		}
		self.db.query_db(sql, data)

	def get_user_info(self, user_id):
		sql = "select * from users where id = :id"
		data = {
			"id": user_id
		}
		result = self.db.query_db(sql, data)

		if result == None or len(result) == 0:
			return None

		return result[0]

	def get_all_users(self):
		sql = "select * from users"
		return self.db.query_db(sql)

