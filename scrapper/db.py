import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, asc, inspect, Date
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

Base = declarative_base()


class LastUpdate(Base):
    __tablename__ = 'last_update'
    date = Column(Date, primary_key=True)


class ScrappedFlat(Base):
    __tablename__ = 'scrapped_flats'
    apartment_number = Column(String, primary_key=True)
    title = Column(String)
    rooms = Column(String)
    size = Column(String)
    total_area_size = Column(String)
    sales_price = Column(String)
    floor_number = Column(String)
    project_name = Column(String)
    href = Column(String)
    img_src = Column(String)
    status = Column(String)
    history = relationship(
        "FlatHistory",
        back_populates="flat",
        primaryjoin="ScrappedFlat.apartment_number==FlatHistory.apartment_number")

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__dict__ if not attr.startswith('_')}


class FlatHistory(Base):
    __tablename__ = 'flat_histories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    apartment_number = Column(String, ForeignKey('scrapped_flats.apartment_number'))
    timestamp = Column(DateTime, nullable=False)
    size = Column(String)
    total_area_size = Column(String)
    sales_price = Column(String)
    floor_number = Column(String)
    status = Column(String)
    flat = relationship(
        "ScrappedFlat",
        back_populates="history",
        primaryjoin="ScrappedFlat.apartment_number==FlatHistory.apartment_number")

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__dict__ if not attr.startswith('_')}


class Database:
    def __init__(self):
        self.engine = create_engine(os.environ['DATABASE_URL'])
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.scheduler = BackgroundScheduler()

    def create(self):
        if "DROP_DATABASE" in os.environ:
            Base.metadata.drop_all(self.engine)

        inspector = inspect(self.engine)

        tables = [
            LastUpdate,
            ScrappedFlat,
            FlatHistory
        ]

        for table in tables:
            if not inspector.has_table(table.__tablename__):
                table.metadata.create_all(self.engine)

        # Schedule the job to run every 5 minutes

        # self.scrap_flats()
        scrap_interval = int(os.getenv("SCRAP_INTERVAL_SECONDS", default=5))
        self.scheduler.add_job(self.scrap_flats, 'interval', seconds=scrap_interval, next_run_time=datetime.now())
        self.scheduler.start()

    def insert_flats(self, flats):
        for flat in flats:
            existing_flat = self.get_flat(flat.apartment_number)
            if existing_flat is None:
                self.create_flat(flat)
            else:
                self.update_flat(existing_flat.apartment_number, flat.to_dict())

    def create_flat(self, flat: ScrappedFlat):
        self.session.add(flat)
        self.session.commit()

    def get_flats(self):
        flats = self.session.query(ScrappedFlat).order_by(asc(ScrappedFlat.apartment_number)).all()
        return flats

    def get_flat(self, apartment_number):
        flat = self.session.query(ScrappedFlat).filter_by(apartment_number=apartment_number).first()
        if flat is not None:
            return flat
        else:
            return None

    def update_flat(self, apartment_number, flat_dict):
        flat = self.session.query(ScrappedFlat).filter_by(apartment_number=apartment_number).first()
        if flat is not None:
            # Create a new FlatHistory object to store the historical data
            history = FlatHistory(apartment_number=apartment_number, timestamp=datetime.now())
            for field in flat.__table__.columns.keys():
                if field in flat_dict:
                    # Update the current state of the flat
                    setattr(flat, field, flat_dict[field])
                    # Update the corresponding field in the historical data
                    setattr(history, field, flat_dict[field])
            # Add the new historical data to the flat's list of histories
            flat.history.append(history)
            self.session.commit()

        return flat

    def delete_flat(self, apartment_number):
        flat = self.session.query(ScrappedFlat).filter_by(apartment_number=apartment_number).first()
        if flat is not None:
            self.session.delete(flat)
            self.session.commit()
            return True
        else:
            return False

    def scrap_flats(self):
        from scrapper.real_estate_scrapper import parse_yit_page
        num_pages = int(os.getenv("PAGES_TO_SCRAP", default=5))
        if 'PRODUCTION' in os.environ:
            for page in range(0, num_pages):
                print(f"Scraping page {page}")
                flats = parse_yit_page(page)

                self.insert_flats(flats)
