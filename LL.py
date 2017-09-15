class Node(object):

    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_next(self, new_next):
        self.next = new_next

class LinkedList(object):

    def __init__(self, head=None):
        self.head = head

    def insert(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node

    def delete(self, data):
        current = self.head
        prev = None
        while current:
            if current.get_data() == data:
                if current == self.head:
                    self.head = current.get_next()
                else:
                    prev.set_next(current.get_next())
                return current
            prev = current
            current = current.get_next()
        return None

    def prints(self):
        lst = []
        current = self.head
        while current:
            lst.append(str(current.get_data()))
            current = current.get_next()
        print lst

def main():
    LLTest = LinkedList()
    LLTest.insert('Sarah')
    LLTest.insert('Bob')
    LLTest.prints()

main()
