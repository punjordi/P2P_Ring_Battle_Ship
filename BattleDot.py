

#Imports
import random, socket, sys , pickle, time


#Player class

class Player():
    def __init__(self):

        #Initialize player class variables and the grids with the ship at random

        self.grid = [['O' for x in range(10)]for y in range(10)]
        self.randomx = random.randint(0,9)
        self.randomy = random.randint(0,9)
        self.grid[self.randomx][self.randomy] = "X"
        self.attacklist = []
        self.leftnode = None
        self.rightnode = None
        self.knockouts = 0
        self.players = None
        self.port = None
        self.rightport = None
        self.leftport = None

        # Helper function used to return the user's Internal IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

        #Main looping function

def listen(player):

    # Assign host variable to the internal ip address obtained by the helper function
    host = get_ip_address()

    while True:
        if player.rightnode:

            print("Awaiting...")
            # Create socket
            listensocket = socket.socket()

            # Set the socket reusability for ease
            listensocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind socket to IP and Port
            listensocket.bind((host, 8080))
            # Listen
            listensocket.listen(5)
            # Wait for incoming connections
            c, addr = listensocket.accept()

            # Receive the message
            msg = c.recv(1024)
            # Deserialize the data
            msg_array = pickle.loads(msg)

            time.sleep(0.2)

            print("Received " + str(msg_array))


        else:

            print("Awaiting...")
            #Create socket
            listensocket = socket.socket()

            #Set the socket reusability for ease
            listensocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #Bind socket to IP and Port
            listensocket.bind((host,int(player.port)))
            #Listen
            listensocket.listen(5)
            #Wait for incoming connections
            c , addr = listensocket.accept()

            #Receive the message
            msg = c.recv(1024)
            #Deserialize the data
            msg_array = pickle.loads(msg)

            time.sleep(0.2)

            print("Received " + str(msg_array))


        #check if the msg sent was a redirect message from a Losing player
        if "atk" in msg_array:


            if player.rightnode:

                #Combine the knockouts and do parsing for the next node
                player.knockouts = player.knockouts + int(msg_array.partition("/")[2])
                player.rightnode = msg_array.partition("atk")[0]

                #Reset the attack list for the next player
                player.attacklist = []

                #Check if no players remaining
                if int(player.knockouts) == int(player.players):
                    print("Winner!")
                    break

                else:

                    #Attack the next player
                    #Create a new socket as we can not reuse the old one
                    newsocket = socket.socket()
                    # Connect to the next node in front of the current
                    newsocket.connect((player.rightnode, 8080))

                    #generate random values for attack
                    attackx = random.randint(0, 9)
                    attacky = random.randint(0, 9)
                    #Serialize the values
                    data_string = pickle.dumps((attackx, attacky))
                    #Send the values to the node
                    newsocket.send(data_string)
                    #Save the coordinates so we dont reuse the same attack
                    player.attacklist.append((attackx, attacky))

                    #Close all the sockets
                    print("Sent Attack to IP " + player.rightnode + "(" + str(attackx) + "," + str(attacky) + ")")
                    newsocket.close()
                    listensocket.close()

            else:
                # Combine the knockouts and do parsing for the next node
                player.knockouts = player.knockouts + int(msg_array.partition("/")[2])
                player.rightport = msg_array.partition("atk")[0]


                # Reset the attack list for the next player
                player.attacklist = []

                # Check if no players remaining
                if int(player.knockouts) == int(player.players):
                    print("Winner!")
                    break

                else:

                    # Attack the next player
                    # Create a new socket as we can not reuse the old one
                    newsocket = socket.socket()
                    time.sleep(2)
                    # Connect to the next node in front of the current
                    newsocket.connect((host,int(player.rightport)))

                    # generate random values for attack
                    attackx = random.randint(0, 9)
                    attacky = random.randint(0, 9)
                    # Serialize the values
                    data_string = pickle.dumps((attackx, attacky))
                    # Send the values to the node
                    newsocket.send(data_string)
                    # Save the coordinates so we dont reuse the same attack
                    player.attacklist.append((attackx, attacky))

                    # Close all the sockets
                    print("Sent Attack to port" + player.rightport + "(" + str(attackx) + "," + str(attacky) + ")")
                    newsocket.close()
                    listensocket.close()
                    print("updated")



        #We reassign the next nodes's LEFT NODE
        elif "def" in msg_array:

            if player.leftnode:
                if int(player.knockouts) == int(player.players):
                    print("Winner!")
                    break

                player.leftnode = "".join(msg_array.split("def"))
                print("updated")
                listensocket.close()
            else:
                if int(player.knockouts) == int(player.players):
                    print("Winner!")
                    break
                player.leftport = "".join(msg_array.split("def"))
                print("updated")
                listensocket.close()




        else:

            #If the msg recieved are coordinates we check if they hit our ship
            if player.grid[msg_array[0]][msg_array[1]] == "X":
                print("HIT! Player Lose")

                if player.rightnode:


                    #We connect with both left and right nodes so we can update their nodes respectively

                    socketright = socket.socket()
                    socketright.connect((player.rightnode, 8080))
                    #Send the IP of the left node to the right node so they are connected
                    data_string = pickle.dumps(player.leftnode + "def")
                    socketright.send(data_string)
                    socketright.close()

                    time.sleep(1) # sleep to avoid any deviance

                    socketleft = socket.socket()
                    socketleft.connect((player.leftnode, 8080))
                    #Send the IP of the right node to the left node and also it's knockouts  so they are connected
                    data_string = pickle.dumps(player.rightnode + "atk" + "/" + str(player.knockouts + 1))
                    socketleft.send(data_string)
                    socketleft.close()

                    listensocket.close()
                    break
                else:
                    socketleft = socket.socket()
                    socketleft.connect((host, int(player.leftport)))
                    # Send the IP of the right node to the left node and also it's knockouts  so they are connected
                    data_string = pickle.dumps(player.rightport + "atk" + "/" + str(player.knockouts + 1))
                    socketleft.send(data_string)
                    socketleft.close()


                    # We connect with both left and right nodes so we can update their nodes respectively

                    socketright = socket.socket()
                    socketright.connect((host, int(player.rightport)))
                    # Send the IP of the left node to the right node so they are connected
                    data_string = pickle.dumps(player.leftport + "def")
                    socketright.send(data_string)
                    socketright.close()

                     # sleep to avoid any deviance



                    listensocket.close()
                    break



            else:
                #there is no hit and we continue with our game where "!" is a location we will hit or have hit
                player.grid[msg_array[0]][msg_array[1]] = "!"

                if player.rightnode:

                    #Prepare new socket for next attack
                    newsocket = socket.socket()
                    newsocket.connect((player.rightnode, 8080))
                    while True:
                        #Randomize the coordinates and if they are already within our list of attacks then we re randomize
                        attackx = random.randint(0, 9)
                        attacky = random.randint(0, 9)
                        if (attackx,attacky) not in player.attacklist:

                            #Once again we serialize the coordinates
                            data_string = pickle.dumps((attackx, attacky))
                            newsocket.send(data_string)
                            #Append the new attack to the list
                            player.attacklist.append((attackx,attacky))

                            #Close all sockets9
                            print("Sent Attack to IP" + player.rightnode + "(" + str(attackx) + "," + str(attacky) + ")")
                            newsocket.close()
                            listensocket.close()
                            break
                else:

                    newsocket = socket.socket()
                    newsocket.connect((host,int(player.rightport)))

                    while True:
                        # Randomize the coordinates and if they are already within our list of attacks then we re randomize
                        attackx = random.randint(0, 9)
                        attacky = random.randint(0, 9)
                        if (attackx, attacky) not in player.attacklist:
                            # Once again we serialize the coordinates
                            data_string = pickle.dumps((attackx, attacky))
                            newsocket.send(data_string)
                            # Append the new attack to the list
                            player.attacklist.append((attackx, attacky))

                            # Close all sockets9
                            print("Sent Attack to port " + player.rightport + "(" + str(attackx) + "," + str(attacky) + ")")
                            newsocket.close()
                            listensocket.close()
                            break


def samemachine(player):

    player.leftport = sys.argv[3]
    player.rightport = sys.argv[4]
    player.players = sys.argv[5]
    player.port = sys.argv[6]

    listen(player)


def differentmachine(player):

    player.leftnode = sys.argv[1]
    player.rightnode = sys.argv[2]
    player.players = sys.argv[5]
    player.port = sys.argv[6]

    listen(player)


def game():

    #Check if they are less than 3 arguements
    if len(sys.argv) < 3:
        print("Specify a Left and Right Node/Address")

    #The player who will intiate the attacks
    elif len(sys.argv) == 8: # first attack
        try:
            #Simple arguement check
            if sys.argv[7] == "first":
                #check if the value of number of players is valid
                if int(sys.argv[5]):

                    if sys.argv[1] == sys.argv[2] == "N/A":


                        #Initialize new player
                        newplayer = Player()

                        #Bind the values of nodes entered into the player class
                        newplayer.leftport = sys.argv[3]
                        newplayer.rightport = sys.argv[4]
                        newplayer.players = sys.argv[5]
                        newplayer.port = sys.argv[6]
                        #initialize new socket and prepare for attack!!!
                        newsocket = socket.socket()
                        #Connect with the right node

                        host = get_ip_address()

                        newsocket.connect((host, int(newplayer.rightport)))

                        #Randomize coordinates to attack with
                        attackx = random.randint(0,9)
                        attacky = random.randint(0,9)
                        #Serialize the data
                        data_string = pickle.dumps((attackx,attacky))
                        newsocket.send(data_string)
                        print("Sent Attack to port" + newplayer.rightport + "(" + str(attackx) + "," + str(attacky) + ")")
                        newsocket.close()
                        #Go into looping listen
                        listen(newplayer)

                    else:
                        # Initialize new player
                        newplayer = Player()

                        # Bind the values of nodes entered into the player class
                        newplayer.leftnode = sys.argv[1]
                        newplayer.rightnode = sys.argv[2]
                        newplayer.players = sys.argv[5]
                        newplayer.port = sys.argv[6]
                        # initialize new socket and prepare for attack!!!
                        newsocket = socket.socket()
                        # Connect with the right node
                        host = get_ip_address()
                        newsocket.connect((newplayer.rightnode, 8080))
                        # Randomize coordinates to attack with
                        attackx = random.randint(0, 9)
                        attacky = random.randint(0, 9)
                        # Serialize the data
                        data_string = pickle.dumps((attackx, attacky))
                        newsocket.send(data_string)
                        print("Sent Attack to IP " + newplayer.rightnode + "(" + str(attackx) + "," + str(attacky) + ")")
                        newsocket.close()
                        # Go into looping listen
                        listen(newplayer)


        except TypeError:
            print("Enter number of players in INT")

    #Standard player
    elif len(sys.argv) == 7:

        try:
            #Value checks to see if its valid
            if int(sys.argv[5]):
                if sys.argv[1] == sys.argv[2] == "N/A":

                    player = Player()
                    samemachine(player)
                else:
                    player = Player()
                    differentmachine(player)


        except TypeError:
            print("Enter number of players in INT")


    return

if __name__ == '__main__':

    game()