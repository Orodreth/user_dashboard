from system.core.model import Model

class Comment(Model):
    def __init__(self):
        super(Comment, self).__init__()

    def add_comment(self, comment):
        sql = "insert into comments(comment, user_id, message_id, created_at, updated_at) " \
            "values(:comment, :user_id, :message_id, NOW(), NOW())"
        data = {
            "comment": comment["comment"],
            "user_id": comment["user_id"],
            "message_id": comment["message_id"]
        }
        self.db.query_db(sql, data)

        return { "status": True }

    def get_all_comments(self):
        sql = "select a.id as comment_id, a.comment, a.created_at as comment_date, b.id as user_id, " \
            "b.first_name, b.last_name, c.id as message_id from comments a " \
            "inner join users b on a.user_id=b.id " \
            "inner join messages c on a.message_id=c.id"
        return self.db.query_db(sql)

    def get_comment_by_comment_id(self, comment_id):
        sql = "select a.id as comment_id, a.comment, a.created_at as comment_date, b.id as user_id, " \
            "b.first_name, b.last_name, c.id as message_id from comments a " \
            "inner join users b on a.user_id=b.id " \
            "inner join messages c on a.message_id=c.id " \
            "where a.id = :id"
        data = {
            "id": comment_id
        }
        result = self.db.query_db(sql, data)

        if result == None or len(result) == 0:
            return None

        return result[0]

    def get_comments_by_message_id(self, message_id):
        sql = "select a.id as comment_id, a.comment, a.created_at as comment_date, b.id as user_id, " \
            "b.first_name, b.last_name, c.id as message_id from comments a " \
            "inner join users b on a.user_id=b.id " \
            "inner join messages c on a.message_id=c.id " \
            "where c.id = :id"
        data = {
            "id": message_id
        }

        return self.db.query_db(sql, data)

    def get_comments_by_messages(self, messages):
        if not messages:
            return None

        messages_id = ""
        for message in messages:
            if messages_id != "":
                messages_id += ", "

            messages_id += str(message["message_id"])

        sql = "select a.id as comment_id, a.comment, a.created_at as comment_date, b.id as user_id, " \
            "b.first_name, b.last_name, c.id as message_id from comments a " \
            "inner join users b on a.user_id=b.id " \
            "inner join messages c on a.message_id=c.id " \
            "where a.message_id in (:id)"
        data = {
            "id": messages_id
        }

        comments = {}
        result = self.db.query_db(sql, data)
        for rec in result:
            if rec["message_id"] not in comments:
                comments[rec["message_id"]] = []
            comments[rec["message_id"]].append(rec)

        return comments

    def delete_comment_by_comment_id(self, comment_id):
        sql = "delete from comments where id =:id"
        data = {
            "id": comment_id
        }
        self.db.query_db(sql, data)

    def delete_comments_by_message_id(self, message_id):
        sql = "delete from comments where message_id =:id"
        data = {
            "id": message_id
        }
        self.db.query_db(sql, data)

    def delete_comments_by_user_id(self, user_id):
        sql = "delete from comments where user_id =:id"
        data = {
            "id": user_id
        }
        self.db.query_db(sql, data)      