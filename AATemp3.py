
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next



# g = ListNode(2)
# f = ListNode(5, g)
# e = ListNode(2)
d = ListNode(1)
c = ListNode(0, d)
b = ListNode(3, c)
a = ListNode(1, b)

def partition(head, x: int):
    if head is None:
        return

    dummy = ListNode(0, head)
    p1 = dummy
    p2 = dummy.next
    start = None
    prev = None

    while p2 is not None:
        if start is None and p2.val >= x:
            start = p2
            prev = p1
        elif start is not None and p2.val < x:
            prev.next = p2
            prev = prev.next
            p1.next = p2.next
            p1 = p2
            p2 = p2.next
        else:
            p1 = p1.next
            p2 = p2.next

    prev.next = start
    return dummy.next


r = partition(a, 3)
while r is not None:
    print(r.val)
    r = r.next

