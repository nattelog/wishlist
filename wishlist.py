from database import Items, Links, Reservations


class WishlistError(Exception):

  def __init__(self, message):
    Exception.__init__(self, message)


class Wishlist():

  def __init__(self):
    self.items = Items()
    self.links = Links()
    self.reservations = Reservations()


  def add_item(self,
               name,
               description,
               image,
               links = None,
               max_reservations = 0):

    """Add an item to the wish list"""

    id = self.items.add_item(name, description, image, max_reservations)

    if links is not None:
      self.links.add_links(id, links)

    return id

  def add_reservation(self, item, amount):

    """
    Place a reservation on an item if max_reservations number is not reached
    """

    max_reservations = self.items.get_max_reservations(item)
    reserved = self.reservations.count_reservations(item)

    if (reserved + amount) > max_reservations:
      raise WishlistError('Reservation amount is too large')

    self.reservations.add_reservation(item, amount)


  def remove_reservation(self, item, amount):

    reserved = self.reservations.count_reservations(item)
    new_amount = amount

    if reserved == 0:
      return

    if amount > reserved:
      new_amount = reserved

    self.reservations.remove_reservation(item, new_amount)


  def get_reservations(self, item):

    return self.reservations.count_reservations(item)


  def get_items(self):

    """Returns all items"""

    items = self.items.get_items()

    for item in items:
      links = self.links.get_links(item['id'])
      item['links'] = links

    return items
