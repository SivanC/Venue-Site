from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://venuesignup:datapass@venuesignup.mysql.pythonanywhere-services.com/venuesignup$default'
db = SQLAlchemy(app)

engine = create_engine('mysql://venuesignup:datapass@venuesignup.mysql.pythonanywhere-services.com/venuesignup$default')

Session = sessionmaker(bind=engine)
session = Session()

class Submission(db.Model):

    __tablename__ = 'submissions'

    groupName = db.Column(db.String(40), primary_key = True)
    perfName = db.Column(db.String(40), nullable = False)
    extraNotes = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return '<Submission groupName={gN} perfName={pN} extraNotes={eN}>'.format(gN=self.groupName, pN=self.perfName, eN=self.extraNotes)

db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('venHome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('venForm.html')

@app.route('/performances', methods=['GET', 'POST'])
def performances():
    if request.method == 'POST':
        sub = Submission(groupName = request.form['groupName'], perfName=request.form['performanceName'], extraNotes=request.form['extraNotes'])
        session.add(sub)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.expunge_all()
            session.close()

    try:
        subList = []
        for i in session.query(Submission).order_by(Submission.groupName):
            subList.append(i)
    except:
        session.rollback()
    finally:
        session.close()

    return render_template('venDisplay.html', subList=subList)

@app.route('/secretdelete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        delName = request.form['deleteName']
        delList = Submission.query.filter(Submission.groupName==delName)
        for i in delList:
            j = session.merge(i)
            session.delete(j)
        try:
          session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    return render_template('venDelete.html')

if __name__ == "__main__":
    app.run(debug=True)