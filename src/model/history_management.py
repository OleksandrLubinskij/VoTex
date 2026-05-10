from src.model.database import Session, Base, engine
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, select, delete

class TranscribeRecord(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    model_size = Column(String)
    language = Column(String)
    fp16 = Column(Boolean)
    preprocessing = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.now())
    prompt = Column(Text)
    result = Column(Text)

class HistoryManager():
    def __init__(self):
        Base.metadata.create_all(engine)

    def create_record(self, model_size, language, fp16, preprocessing, prompt, result):
        with Session.begin() as session:
            new_record = TranscribeRecord(
                model_size = model_size,
                language = language,
                fp16 = fp16,
                preprocessing = preprocessing,
                prompt = prompt,
                result = result
            )
            session.add(new_record)

    def read_records(self, limit=10, offset=0):
        with Session() as session:
            stmt = select(TranscribeRecord.id,
                          TranscribeRecord.model_size, 
                          TranscribeRecord.language, 
                          TranscribeRecord.fp16,
                          TranscribeRecord.preprocessing
                        ).limit(limit
                        ).offset(offset
                        ).order_by(TranscribeRecord.timestamp.desc())
            result = session.execute(stmt).all()
            return result
        
    def read_prompt(self, id):
        with Session() as session:
            stmt = select(TranscribeRecord.prompt
                        ).where(TranscribeRecord.id == id)
            prompt = session.execute(stmt).one()[0]
            return prompt
    
    def read_result(self, id):
        with Session() as session:
            stmt = select(TranscribeRecord.result
                        ).where(TranscribeRecord.id == id)
            result = session.execute(stmt).one()[0]
            return result

    def delete_all(self):
        with Session.begin() as session:
            stmt = delete(TranscribeRecord)
            session.execute(stmt)

    def delete_by_id(self, id):
        with Session.begin() as session:
            stmt = delete(TranscribeRecord
                          ).where(TranscribeRecord.id == id)
            
            session.execute(stmt)
            

