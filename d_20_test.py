import random

# users = ["Jonas", "Flo", "Nina", "Felix", "vinh", "ganker", "kim"]
# user_relations = []
# d20_random = len(users)

# while(d20_random % len(users) == 0):
#     d20_random = random.randrange(19)+1

# for i in range(len(users)):
#     partner_index = (i+d20_random)%len(users)
#     user_relations.append((users[i], users[partner_index]))

users = []

def addUser(uid, name, isAdmin, groupId):
    users.append(dict({"uid": uid, "name": name, "isAdmin": isAdmin, "groupId": groupId}))

def shuffle(groupName):
    group_name = groupName
    print("group: " + str(group_name))
    shuffle_users = []

    for user in users:
        if user["groupId"] == group_name:
            shuffle_users.append(user)
    
    user_relations = []
    d20_random = len(shuffle_users)

    while(d20_random % len(shuffle_users) == 0):
        d20_random = random.randrange(19)+1

    for i in range(len(shuffle_users)):
        partner_index = (i+d20_random)%len(shuffle_users)
        user_relations.append((users[i], users[partner_index]))
    
    print(user_relations)

    for user in user_relations:
        print(str(user[0]["name"]) + "->" + str(user[1]["name"]))


if __name__ == "__main__":
    addUser("123", "flo", False, "sadasd")
    addUser("qwe", "vinh", False, "sadasd")
    addUser("121233", "ganknuss", False, "sadasd")
    addUser("yxc", "kimse", False, "sadasd")
    addUser("ysxc", "xd", False, "asdsadasd")

    shuffle("sadasd")

