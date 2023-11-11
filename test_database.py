import shelve
from classes.stocks import Inventory
from classes.drink import Drink
from classes.shoppingBag import shoppingBag, ThaiMilkTea

db=shelve.open('storage.db','w')

# order_dict=db['Orders']
# for o in order_dict.values():
#     total=0
#     for d in o.get_order().values():
#         total += d.get_total_cost()
#     o.set_total_cost(round(total, 2))

# db['Orders']=order_dict

# s=[]
# for u in i:
#     print(u)
#     if u.get_email()=='alvin_tay@gmail.com':
#         i.pop(u.get_email())
#         break


# # for h in s:
# #     i.pop(h)

# db['Users']=i

        # print(u.get_shopping_bag().get_order().values())

# print(s.get_order().values())
# current_user.get_shopping_bag().get_order()

# for i in s.get_order().values():
#     print(i.get_drink_id())
#     print(i.get_name())
#     print(i.get_quantity())
#     print(i.get_size())
#     print(i.get_sugar_level())
#     print(i.get_topping())
#     print(i.get_cost())
# for n in s:
#     i.pop(n)
# # print(i)
# # # u.set_birth_month('February')
# db['Users']=i
# db.close()
# # print(i.get('amberyeo21@gmail.com').set_birth_month('February'))
# # get_birth_month

i=db['Inventory']

i.used_milk()
i.used_milk()

db['Inventory']=i
# print(f.get(9612).get_time().date())
# f={}

# for i in f.values():
#     print((i.get_time()).datetime())
db.close()
