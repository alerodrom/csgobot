import os
import sys

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from datetime import date

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_telegram'
    id = Column(Integer, primary_key=True)
    id_telegram = Column(Integer)
    first_name = Column(String)
    alias = Column(String)
    admin = Column(Integer, default=0)


class Mix(Base):
    __tablename__ = 'mix'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    mix_date = Column(Date)


class MixUser(Base):
    __tablename__ = 'mix_user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    mix_id = Column(Integer)


class DBHelper:
    def setup(self):
        # Example schema:  "sqlite:///csgo_bot.db"
        # MYSQL and PSQL can also be used, check sqlalchemy doc.
        schema = os.environ.get('csgo_bot_schema')
        if not schema:
            print('You should include a schema for your database.')
            sys.exit()
            return
        engine = create_engine(schema)
        Base.metadata.create_all(engine)

        DBSession = sessionmaker(bind=engine)
        self.session = (scoped_session(DBSession) if 'sqlite' in schema
            else DBSession())

    def get_last_mix(self):
        return self.session.query(Mix).order_by(Mix.id.desc()).first()

    def mix_exist(self):
        today = date.today()
        mix = self.session.query(Mix).filter(Mix.mix_date == today).first()
        return True if mix else False

    def user_in_mix(self, user_id, mix_id):
        return (True if self.session.query(MixUser).filter(
                MixUser.mix_id == mix_id).filter(
                MixUser.user_id == user_id).first() else False)

    def get_user(self, id_telegram):
        return self.session.query(User).filter(
            User.id_telegram == id_telegram).first()

    def get_admins(self):
        return self.session.query(User).filter(
            User.admin == 1).all()

    def user_create(self, id_telegram, first_name, alias):
        user = User(id_telegram=id_telegram, first_name=first_name,
            alias=alias)
        self.session.add(user)
        self.session.commit()
        return user

    def mix_today(self):
        today = date.today()
        last_mix = self.get_last_mix()
        if last_mix:
            if today == last_mix.mix_date:
                return True
            else:
                return False
        else:
            return False

    def create_mix(self, description):
        if not self.mix_exist():
            self.session.add(Mix(description=description,
                    mix_date=date.today()))
        elif self.mix_today():
            msg = 'Ya ha sido creado'
        try:
            self.session.commit()
            msg = 'Mix creado correctamente'
        except Exception:
            pass
        return msg

    def add_item(self, id_telegram, first_name, alias):
        user = self.get_user(id_telegram)
        if not user:
            self.user_create(id_telegram, first_name, alias)
            user = self.get_user(id_telegram)
        last_mix = self.get_last_mix()
        if last_mix and not self.user_in_mix(user.id, last_mix.id):
            self.session.add(MixUser(user_id=user.id,
                    mix_id=last_mix.id))
            return self.session.commit()
        return False

    def delete_item(self, id_telegram):
        last_mix = self.get_last_mix()
        user = self.get_user(id_telegram)
        if user and self.user_in_mix(user.id, last_mix.id):
            self.session.query(MixUser).filter(MixUser.user_id == user.id,
                MixUser.mix_id == last_mix.id).delete()
            return self.session.commit()

    def get_items(self):
        last_mix = self.get_last_mix()
        if not last_mix:
            return False
        mix_users = self.session.query(User).join(
            MixUser, MixUser.user_id == User.id).filter(
                MixUser.mix_id == last_mix.id).all()
        return mix_users

    def set_admin(self, user):
        user.admin = 1
        return self.session.commit()

    def revoke_admin(self, user):
        user.admin = 0
        return self.session.commit()

    def get_users(self):
        return self.session.query(User)

    def add(self, to_add):
        try:
            self.session.add(to_add)
            self.session.commit()
            return 1
        except Exception:
            return 0