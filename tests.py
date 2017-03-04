import unittest
from wishlist import Wishlist, WishlistError
import json


class WishlistTestCase(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    self.wishlist = Wishlist()


  @classmethod
  def tearDownClass(self):
    self.wishlist.items.drop_table()
    self.wishlist.links.drop_table()
    self.wishlist.reservations.drop_table()


  def test_item(self):
    links = [
      { 'title': 'Link 1', 'href': 'website.com' },
      { 'title': 'Link 2', 'href': 'internet.com' }
    ]
    id = self.wishlist.add_item('Item 1', 'An item', 'imagedata', links, 1)
    self.assertNotEqual(id, None)

    rows = self.wishlist.get_items()
    result = rows[0]

    self.assertEqual(len(rows), 1)
    self.assertEqual(result['id'], id)
    self.assertEqual(result['name'], 'Item 1')
    self.assertEqual(result['description'], 'An item')
    self.assertEqual(result['image'], 'imagedata')
    self.assertEqual(len(result['links']), 2)
    self.assertEqual(result['max_reservations'], 1)

    def add_reservations():
      self.wishlist.add_reservation(id, 2)

    self.assertRaises(WishlistError, add_reservations)

    self.wishlist.add_reservation(id, 1)
    reserved = self.wishlist.get_reservations(id)

    self.assertEqual(reserved, 1)

    self.wishlist.remove_reservation(id, 1)
    reserved = self.wishlist.get_reservations(id)

    self.assertEqual(reserved, 0)

    self.wishlist.remove_reservation(id, 1)
    reserved = self.wishlist.get_reservations(id)

    self.assertEqual(reserved, 0)

unittest.main()
