import sqlite3
import time

DATABASE_PATH = 'database.db'

class Database():

  def __init__(self, table_name):
    self.db = None
    self._execute_schema()
    self.table_name = table_name


  def drop_table(self):
    self._execute('drop table if exists {}'.format(self.table_name))


  # Protected methods

  def _get_db(self):
    if self.db is None:
      self.db = sqlite3.connect(DATABASE_PATH)
      self.db.row_factory = self._dict_factory
    return self.db


  def _schema(self):

    raise NotImplemented('Abstract method')


  def _execute_schema(self):
    query = self._schema()
    self._execute(query)


  def _execute(self, query, args = {}, get_id = False):
    strategy = self._get_db().execute
    return self._db_execution(strategy, query, args, get_id)


  def _executemany(self, query, args):
    strategy = self._get_db().executemany
    return self._db_execution(strategy, query, args, False)


  # Private methods

  def _db_execution(self, strategy, query, args, get_id):
    db = self._get_db()
    cursor = strategy(query, args)
    result = None

    if get_id:
      result = cursor.lastrowid
    else:
      result = cursor.fetchall()

    db.commit()
    return result


  @staticmethod
  def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
    return d


class Items(Database):

  def __init__(self):
    Database.__init__(self, 'items')


  def _schema(self):
    return \
      """
      create table if not exists items(
      id integer primary key,
      name text,
      description text,
      image text,
      max_reservations integer
      )
      """


  def add_item(self, name, description, img, max_reservations = 0):
    return self._execute(
      """
      insert into items (name, description, image, max_reservations)
      values (?, ?, ?, ?);
      """,
      (name, description, img, max_reservations),
      True
    )


  def get_items(self):
    return self._execute('select * from items')


  def get_max_reservations(self, item):
    return self._execute(
      """
      select max_reservations from items where id = ?
      """,
      (item,)
    )[0]['max_reservations']


class Links(Database):

  def __init__(self):
    Database.__init__(self, 'links')


  def _schema(self):
    return \
      """
      create table if not exists links(
      item integer,
      title text,
      href text,
      foreign key (item) references items(id)
      )
      """


  def add_links(self, item, links):
    args = list((item, link['title'], link['href']) for link in links)

    return self._executemany(
      """
      insert into links values (?, ?, ?)
      """,
      args
    )


  def get_links(self, item):
    return self._execute(
      """
      select title, href from links where item = ?
      """,
      (item,)
    )


class Reservations(Database):

  def __init__(self):
    Database.__init__(self, 'reservations')


  def _schema(self):
    return \
      """
      create table if not exists reservations(
      item integer,
      amount integer,
      timestamp integer,
      foreign key (item) references items(id)
      )
      """


  def add_reservation(self, item, amount):
    return self._execute(
      """
      insert into reservations values (?, ?, ?)
      """,
      (item, amount, self._make_timestamp())
    )


  def remove_reservation(self, item, amount):
    return self.add_reservation(item, -amount)


  def count_reservations(self, item):
   result = self._execute(
     """
     select sum(amount) as amount
     from reservations
     where item = ?
     """,
     (item,)
   )[0]['amount']

   return result if result is not None else 0

  # Private methods

  @staticmethod
  def _make_timestamp():
   return time.time() * 1000
