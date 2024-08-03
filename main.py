import paho.mqtt.client as mqtt


# local server config
local_mqtt_server = "xxxxxxxxxxxxxx"
local_mqtt_port = 1883
local_mqtt_topic = "xxxxxxx"
local_user = "xxxx"
local_password = "xxxx"


# remote server config
remote_mqtt_server = "xxxxx"
remote_mqtt_port = 1883
remote_mqtt_client_id = "xxxxx"
remote_mqtt_user = "xxxxxxxxxxxx"
remote_mqtt_uid = "xxxxxxxxxxxxxxxxxxxxxxxxx"
remote_mqtt_topic = "xxx"


## set your type table
TableType = ["AC","LED","SWITCH"]


# set transfer rule
def forword_to_remote(message):
    try:
        ## limit subscribe type
        mytype  = message["type"]
        print("[type]:"+mytype)
        if mytype not in TableType:
            return 
        ## get local topic
        mytopic = message["topic"]
        print("[topic]:"+mytopic)
        ## read local message
        info = message["info"]["message"]
        print("[msg]:"+info)

        # forword local message to remote server
        remote_client.publish(mytopic, info)
    except Exception as error:
        print(error)

# init MQTT
local_client = mqtt.Client()
remote_client = mqtt.Client(client_id=remote_mqtt_uid)


def on_connect_local(client, userdata, flags, rc):
    print("Connected to local MQTT server with result code " + str(rc))
    client.subscribe(local_mqtt_topic)

def on_message_local(client, userdata, msg):
    ##print("Message received from local MQTT server: " + msg.payload.decode())

    ## format message = {
    ##          "type":"your type",
    ##          "topic":"your topic",   
    ##          "info":{
    ##              "message":"your message"
    ##              ...
    ##          }
    ##        }
    message = eval(msg.payload.decode())
    forword_to_remote(message)



def on_connect_remote(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to remote Cloud MQTT server")
        ##remote_client.subscribe(remote_mqtt_topic)  ## subscribe remote topic 
    else:
        print("Failed to connect to remote Cloud MQTT server, return code %d\n", rc)
def on_message_remote(client,userdata,msg):
    print("subscribe remote msg:"+ msg.payload.decode()) ## print message received from remote server


# set callback
local_client.on_connect = on_connect_local
local_client.on_message = on_message_local
remote_client.on_connect = on_connect_remote
#remote_client.on_message = on_message_remote

# connect to remote server
remote_client.connect(remote_mqtt_server, remote_mqtt_port, 60)
# connect to local server
local_client.connect(local_mqtt_server, local_mqtt_port, 60)
local_client.username_pw_set(local_user, local_password)


# start MQTT
local_client.loop_start()
remote_client.loop_start()

# keep running
try:
    while True:
        pass

except KeyboardInterrupt:
    print("Exiting")
    local_client.loop_stop()
    remote_client.loop_stop()
    local_client.disconnect()
    remote_client.disconnect()

