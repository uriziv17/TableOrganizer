from Spot import Spot
from Table import Table

if __name__ == '__main__':
    sp = Spot(100, 200, "dad")
    su = Spot(300, 400, "uri")
    tb = Table("Images/tableFor3.jpeg")
    tb.add_spot(sp)
    tb.add_spot(su)
    tb.add_connection(sp, su)
    print(tb)

