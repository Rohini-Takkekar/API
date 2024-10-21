from flask import Flask, render_template ,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String , DateTime
from sqlalchemy.orm import declarative_base


# app.config['SQLALCHEMY_DATABASE_URI']= "mysql+mysqlconnector://root:root@localhost/db"
# app.config['SQLALCHEMY_DATABASE_MODIFICATIONS']=False
#app.app_context()

# db= SQLAlchemy(app)

database_url = 'mysql+mysqlconnector://root:root@localhost/db'
engine = create_engine(database_url)
Base = declarative_base()
Sessionlocal = sessionmaker(bind = engine)

class Employee(Base):
    __tablename__ = 'Employee'
    sno=Column(Integer,primary_key=True)
    psno=Column(Integer,nullable=False)
    email=Column(String(100),nullable=False)
    details=Column(String(500),nullable=False)

    def __repr__(self) -> str:
        return f"{self.psno} {self.email}"
    
Base.metadata.create_all(bind=engine)    
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def EMP_DATA():
    db=Sessionlocal()
    if request.method=='POST':
        psno=request.form['psno']
        email=request.form['email']
        details=request.form['details']

        if psno=='' or email=='' or details=='':
            return redirect('/no_entry')
        else:
            emp=Employee(psno=psno,email=email,details=details)
            db.add(emp)
            db.commit()
    allemp=db.query(Employee).all()
    return render_template('page.html',allemp=allemp)

@app.route('/Update/<int:sno>',methods=['GET','POST'])
def update(sno):
    db=Sessionlocal()
    if request.method=='POST':
        psno=request.form['psno']
        email=request.form['email']
        details=request.form['details']
        emp=db.query(Employee).filter_by(sno=sno).first()
        emp.psno=psno
        emp.email=email
        emp.details=details
        db.commit()
        return redirect('/')
    emp=db.query(Employee).filter_by(sno=sno).first()
    return render_template('updates.html',emp=emp)


@app.route('/delete/<int:sno>')
def delete(sno):
    db=Sessionlocal()
    myemp=db.query(Employee).filter_by(sno=sno).first()
    db.delete(myemp)
    db.commit()
    return redirect('/')


@app.route("/no_entry")
def add_entry():
    return render_template('alerts.html')

if __name__ == "__main__":
    app.run(debug=True)

