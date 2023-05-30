import pandas as pd
import openpyxl
import string

df = pd.read_excel('books.xlsx', engine='openpyxl')
books_list = df.to_dict(orient='records')
authors_set = set()
books_dict= {}


class BookNode:
  def __init__(self, title, author, author_lastname, topics, edition):
    self.title = title
    self.author = author
    self.author_lastname = author_lastname
    self.topics = topics.split(",")
    self.edition = edition

  def __repr__(self):
    ret = f"'{self.title}' - Book by {self.author} published in {self.edition} (topics: {', '.join(topic for topic in self.topics)})."
    return ret


for book in books_list:
  booknode = BookNode(book['Title'], book['Author'], book['Author LastName'], book['Genre'], book['Edition'])
  books_dict[booknode.title] = booknode
  authors_set.add((book['Author LastName'], book['Author']))


class AuthorNode:
    def __init__(self, name, full_name):
        self.name = name
        self.full_name = full_name
        self.books = []
    
    def add_book(self, booknode):
       self.books.append(booknode)


class ContainerNode:
    def __init__(self, value):
      self.value = value
      self.authors = []
    
    def add_author(self, author_node):
      self.authors.append(author_node)

class SearchingByAuthorTree:
    def __init__(self):
      self.name = "root"
      self.containers = {}
      self.creation_containers()

    def creation_containers(self):
        for letter in string.ascii_lowercase:
            container = ContainerNode(letter)
            self.containers[letter] = container


### start of helping methods
def found_no_authors():
    print("There is no author to suggest")
    check_again = input("Would you like to try find another author? Enter 'y' for 'yes' and any other button to return to start menu.")
    if check_again == "y":
        return searching_by_author()
    else:
        searching_by_author() ####!!!!!!!!!!!!!!!!! zamienić na start aplikacji
      
def found_one_author(author):
    print(f"The only author I can suggest is {author.full_name}")
    check_autor = input(f"Would you like to see {author.full_name}'s books? Enter 'y' for 'yes' and any other button to return to start menu.")
    if check_autor != "y":
      return searching_by_author() ####!!!!!!!!!!!!!!!!! zamienić na start aplikacji
    else:
      for book in author.books:
        print(book)
    check_again = input(f"Would you like to see another author? Enter 'y' for 'yes' and any other button to return to start menu.")
    if check_again == "y":
        return searching_by_author()
    else:
        searching_by_author() ####!!!!!!!!!!!!!!!!! zamienić na start aplikacji

def found_many_authros(searching_authors):
    while len(searching_authors) > 1:
        print("Here are the suggested authors: ")
        for author in searching_authors:
            print(author.full_name)
        selected_authors = []
        check_author = input("Type the beginning of the author's surname to view their books: ")
        for author in searching_authors:
            is_match = True
            for index in range(len(check_author)):
                if check_author[index].lower() != author.name[index].lower():
                    is_match = False
                    break
            if is_match:
                selected_authors.append(author)
        searching_authors = selected_authors
        print()
    if not searching_authors:
        return found_no_authors()
    return found_one_author(searching_authors[0])
### end of helping methods



def searching_by_author():
    root = SearchingByAuthorTree()
    for author, author_fullname in authors_set:
        container = root.containers.get(author[0].lower())
        if container is not None:
            container.add_author(AuthorNode(author, author_fullname))

    for container in root.containers.values():
        for author in container.authors:
            for book in books_dict.values():
              if book.author_lastname == author.name:
                  author.add_book(book)
    
    search(root)


def search(root):
    author_letter = input("Select the first letters of the author's surname:  ")
    if len(author_letter) == 0:
       question_1 = input("Would you like to see all the authors? Enter 'y' for 'yes' and any other button to return to start menu.")
       if question_1 == "y":
          for author in sorted(list(authors_set)):
            print(author)
       else:
          searching_by_author() ####!!!!!!!!!!!!!!!!! zamienić na start aplikacji
    elif len(author_letter) == 1:
      container = root.containers.get(author_letter.lower())
      
      if not container.authors:
        return found_no_authors()
      
      if len(container.authors) == 1:
        return found_one_author(container.authors[0])

      else:
        return found_many_authros(container.authors)

    elif len(author_letter) > 1:
      container = root.containers.get(author_letter[0].lower())
      if not container.authors:
        return found_no_authors()
      
      searching_authors = container.authors
      selected_authors = []
      for author in searching_authors:
        is_match = True
        for index in range(len(author_letter)):
          if author_letter[index].lower() != author.name[index].lower():
              is_match = False
              break
        if is_match:
            selected_authors.append(author)
      searching_authors = selected_authors
      
      if not searching_authors:
          return found_no_authors()

      else:
          return found_many_authros(searching_authors)

         
searching_by_author()