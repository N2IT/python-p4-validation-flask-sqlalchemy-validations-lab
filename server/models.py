from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name ):
        # breakpoint()
        if name == '':
            raise ValueError("Each author must have a name")
        elif Author.query.filter(Author.name == name).first():
            raise ValueError("No two authors can have the same name")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        # breakpoint()
        if len(number) != 10:
            raise ValueError("Number must be exactly 10 digits")
        elif not int(number):
            raise ValueError("Number must be exactly 10 digits")

        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def validate_title(self, key, title):
        if title == '':
            raise ValueError("Every post must have a title.")
        
        if "Won't Believe" in title:
            return title
        if "Secret" in title:
            return title
        if "Top" in title:
            return title
        if "Guess" in title:
            return title
        else:
            raise ValueError("Post title must contain a clickbait-y phrase.")
    
        # clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        # if not any(phrase in title for phrase in clickbait_phrases):
        #     raise ValueError("Post title must contain at least one of the following phrases: 'Won't Believe', 'Secret', 'Top', 'Guess'.")

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be atleast 250 char long")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must not exceed 250 characters.")
        return summary
     
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Category must be Fiction or Non-Fiction')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
