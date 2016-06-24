from system.core.model import Model

class Message(Model):
	def __init__(self):
		super(Message, self).__init__()
	
	def add_message(self, message):
		sql = "insert into messages(message, sender_id, receiver_id, created_at, updated_at) " \
			"values(:message, :sender_id, :receiver_id, NOW(), NOW())"
		data = {
			"message": message["message"],
			"sender_id": message["sender_id"],
			"receiver_id": message["receiver_id"]
		}
		self.db.query_db(sql, data)

		return { "status": True }

	def get_all_messages(self):
		sql = "select a.id as message_id, a.message, a.created_at as message_date, " \
			"a.sender_id, a.receiver_id, b.first_name, b.last_name from messages a " \
			"inner join users b on a.sender_id = b.id"
		return self.db.query_db(sql)

	def get_message_by_message_id(self, message_id):
		sql = "select a.id as message_id, a.message, a.created_at as message_date, " \
			"a.sender_id, a.receiver_id, b.first_name, b.last_name from messages a " \
			"inner join users b on a.sender_id = b.id " \
			"where a.id = :id"
		data = {
			"id": message_id
		}
		result = self.db.query_db(sql, data)

		if result == None or len(result) == 0:
			return None

		return result[0]

	def get_messages_by_receiver_id(self, receiver_id):
		sql = "select a.id as message_id, a.message, a.created_at as message_date, " \
			"a.sender_id, a.receiver_id, b.first_name, b.last_name from messages a " \
			"inner join users b on a.sender_id = b.id " \
			"where a.receiver_id = :id" 
		data = {
			"id": receiver_id
		}

		return self.db.query_db(sql, data)

	def delete_message_by_message_id(self, message_id):
		sql = "delete from messages where id = :id"
		data = {
			"id": message_id
		}
		self.db.query_db(sql, data)

	def delete_messages_by_sender_id(self, sender_id):
		sql = "delete from messages where sender_id = :id"
		data = {
			"id": sender_id
		}
		self.db.query_db(sql, data)

	def delete_messages_by_receiver_id(self, receiver_id):
		sql = "delete from messages where receiver_id = :id"
		data = {
			"id": receiver_id
		}
		self.db.query_db(sql, data)