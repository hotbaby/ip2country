import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import Column, BigInteger, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

MYSQL_SERVER = 'mysql://root:1@192.168.1.251/ip2country'

engine = sqlalchemy.create_engine(MYSQL_SERVER)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

class IPCountryMapper(Base):
    __tablename__ = 'ip2country'
    
    id = Column(BigInteger, primary_key=True)
    start = Column(BigInteger, nullable=False, unique=True)
    start_str = Column(String(16), nullable=False, unique=True)
    end = Column(BigInteger, nullable=False, unique=True)
    end_str = Column(String(16), nullable=False, unique=True)
    number = Column(BigInteger, nullable=False)
    registry = Column(String(32), nullable=False)
    assigned = Column(Integer, nullable=False)
    ctry = Column(String(4), nullable=False)
    cntry = Column(String(16), nullable=False)
    country = Column(String(32), nullable=False)
    
    def __repr__(self):
        return '<IPCountryMapper(start=%d, end=%d, registry=%s, assigned=%d, ctry=%s, cntry=%s, country=%s)>' %(
                                                    self.start, self.end, self.registry, self.assigned, self.ctry, self.cntry, self.country)

def get_country(ip):
    import socket
    import struct
    ip_int = struct.unpack('!I', socket.inet_aton(ip))[0]
    mapper = session.query(IPCountryMapper)\
                                .filter(and_(IPCountryMapper.start <= ip_int, IPCountryMapper.end >= ip_int))\
                                .first()
    return mapper.country

def create_all():
    Base.metadata.create_all()
    
def drop_all():
    Base.metadata.drop_all()
    
if __name__ == '__main__':
    import struct, socket
    def ip_aton(ip_string):
        return struct.unpack("!I", socket.inet_aton(ip_string))[0]
    def ip_ntoa(ip_int):
        return socket.inet_ntoa(struct.pack("!I", ip_int))

    print('start')
    counter = 0
    for item in session.query(IPCountryMapper).all():
        item.number = item.end - item.start + 1
        counter += 1
        if counter % 1024 == 0:
            session.commit()
            print('commit %d' % (counter))
    session.commit()
    print('end')