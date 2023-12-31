from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy import insert, update, delete
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional, Annotated

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"

    ssn = Column("ssn",Integer, primary_key=True) #not null?...
    firstname = Column("firstname",String(15))
    lastname = Column("lastname",String(15))
    gender = Column("gender",CHAR(1))
    age = Column("age",Integer)

    def __init__ (self,ssn,firstname,lastname,gender,age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn} {self.firstname} {self.lastname} {self.gender} {self.age})"

class Thing(Base):

    __tablename__ = "things"
    tid = Column("tid",Integer,primary_key=True)
    description = Column("description",String(15))
    owner = Column (Integer, ForeignKey("people.ssn"))

    def __init__(self,tid,description,owner):
        self.tid = tid
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f"({self.tid} {self.description} {self.owner})"

class ppl(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] =None





URL_DATABASE = 'mysql+pymysql://root:1234@localhost:3306/new'
engine = create_engine(URL_DATABASE)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# person = Person(12312,"Mike","Smith","m",35)
# session.add(person)
# session.commit()


# can we store it in csv files
p1 = Person(68921,"Anna","Blue","f",40)
p2 = Person(85964,"Bob","Blue","m",35)
p3 = Person(78546,"Angela","Cold","f",22)

# session.add(p1)
# session.add(p2)
# session.add(p3)
# session.commit()

t1 = Thing(1, "Car", p1.ssn)
t2 = Thing(2, "Laptop", p1.ssn)
t3 = Thing(3, "PS5", p2.ssn)
t4 = Thing(4, "Tool", p3.ssn)
t5 = Thing(5, "Book", p3.ssn)
# session.add(t1)
# session.add(t2)
# session.add(t3)
# session.add(t4)
# session.add(t5)
#
# session.commit()

result = session.query(Person).all()
for r in result:
    print(r)

print()

result = session.query(Person).filter(Person.lastname=="Blue")
for r in result:
    print(r)

print()
result = session.query(Person).filter(Person.firstname.in_(["Anna","Mike"]))
for r in result:
    print(r)

print()
result = session.query(Thing, Person).filter(Thing.owner==Person.ssn).filter(Person.firstname == "Anna")
for r in result:
    print(r)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db =session()
    try:
        yield db
    finally:
        db.close()

@app.get("/get-by-name/")
def get_person(person_name:str):
    result = session.query(Person).filter(Person.firstname==person_name).all()

    return result

# Update operation
@app.put("/update_people/")
def update_person(ssn_id: int, person_update:ppl, db: Session = Depends(get_db)):
    record = db.query(Person).filter(Person.ssn ==ssn_id).first()
    if record:
        return record

    else:
        raise HTTPException(status_code=404, detail=f"Person with SSN {ssn} not found")

# Insert operation
@app.post("/people/")
def create_person(ssn: int, firstname: str, lastname: str, gender: str, age: int, db: Session = Depends(get_db)):
    person = Person(ssn=ssn, firstname=firstname, lastname=lastname, gender=gender, age=age)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person



# Delete operation
@app.delete("/people/{ssn}")
def delete_person(ssn: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter_by(ssn=ssn).first()
    if person:
        db.delete(person)
        db.commit()
        return {"message": f"Person with SSN {ssn} deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"Person with SSN {ssn} not found")







