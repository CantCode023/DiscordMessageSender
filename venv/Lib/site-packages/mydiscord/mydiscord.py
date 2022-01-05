import requests
import json
import traceback
import time
from urllib.request import Request, urlopen

class Discriminator:
    def toDis(number):
        a = []

        for i in range(len(number)):    
            a.append(i)

        for i in a:
            if number[i] == "0":
                if i == len(number)-1:
                    if number[i-1] == "0":
                        number = number
                    elif number[0] != "0":
                        number = number
                    else:
                        number = number[:i]
                elif i == 0:
                    if number[-1] == "0":
                        pass
                    else:
                        number = number[i+1:]
                
        return number

class Client:
    def __init__(self, token:str):
        self.token = token

    def setStatus(self, status:str):
        url = "https://discord.com/api/v9/users/@me/settings"
        headers = {
            "authorization": self.token,
            "content-type": "application/json"
        }
        data = {
            "custom_status": {
                "text": status
            }
        }

        try:
            resp = requests.patch(url, headers=headers, data=json.dumps(data))
            if resp.status_code == 200:
                return json.loads(resp.text)
            else:
                return traceback.format_exc()
        except Exception:
            return "There was an error!{}".format(traceback.format_exc())

    def makeInvite(self, serverid:int, channelid:int, max_age:int=604800, max_uses:int=0, temporary:bool=False):
        ages = [0, 1800, 3600, 21600, 43200, 86400, 604800]
        uses = [0, 1, 5, 10, 25, 50, 100]
        url = f"https://discord.com/api/v9/channels/{str(channelid)}/invites"
        headers = {"authorization": self.token}
        
        data = {
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary
        }

        ij = f"https://discord.com/channels/{str(serverid)}/{str(channelid)}"
        b = requests.get(ij, headers=headers, data=data).text
        b = str(b)
        if 'id="app-mount"' in b:
            if max_age in ages:
                if max_uses in uses:
                    try:
                        resp = requests.post(url, headers=headers, data=data)
                        resp1 = json.loads(resp.text)
                        if resp.status_code == 200:
                            return f"https://discord.com/invite/{resp1['code']}"
                        else:
                            return "There was an error! Please check your aruguments again. "
                    except Exception:
                        return "There was an error!\n{}".format(traceback.format_exc())
                else:
                    return "Wrong max_uses format! Please read the documentation."
            else:
                return "Wrong max_age format! Please read the documentation."
        else:
            return "Unvalid server!"

    def sendMessage(self, channel_id:int, message:str):
        url = f"https://discord.com/api/v6/channels/{channel_id}/messages"
        headers = {
            "authorization": self.token
        }

        data = {
            "content": message
        }

        try:
            resp = requests.post(url, headers=headers, data=data)
            resp1 = json.loads(resp.text)
            if resp.status_code == 200:
                return resp1['channel_id'], resp1['id']
            else:
                return "There was an error! Pleace check your arguments."
        except Exception:
            return "There was an error!\n{}".format(traceback.format_exc())

    def deleteMessage(self, channel_id:int, message_id:int):
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
        headers = {
            "authorization": self.token
        }
        try:
            resp = requests.delete(url, headers=headers)
        except Exception:
            return "There was an error!\n{}".format(traceback.format_exc())

    def pinMessage(self, channel_id:int, message_id:int):
        url = f"https://discord.com/api/v9/channels/{channel_id}/pins/{message_id}" 
        headers = {
            "authorization": self.token
        }
        try:
            resp = requests.put(url, headers=headers)
        except Exception:
            return "There was an error!\n{}".format(traceback.format_exc())

    def editMessage(self, channel_id:int, message_id:int, message:str):
        url = f"https://discord.com/api/v6/channels/{channel_id}/messages/{message_id}"
        headers = {
            "authorization": self.token
        }
        data = {
            "content": message
        }
        try:
            resp = requests.patch(url, headers=headers, data=data)
            resp1 = json.loads(resp.text)
            if resp.status_code == 200:
                return "Successfull edited message"
            else:
                return "There was an error! Please check your arguments."
        except Exception:
            return "There was an error!\n{}".format(traceback.format_exc())

    def replyMessage(self, channel_id:int, message_id:int, message:str):
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        
        headers = {"authorization": self.token}
        
        data = {
            "content": message,
            "message_reference": {
                "channel_id": channel_id,
                "message_id": message_id
            }
        }

        try:
            resp = requests.post(url, headers=headers, data=data)
            resp1 = json.loads(resp.text)
            if resp.status_code == 200:
                return resp1
            else:
                return "There was an error! Please check your arguments."
        except Exception:
            return  "There was an error!\n{}".format(traceback.format_exc())

    def setPresence(self, presence:str=["online", "idle", "dnd", "invisible"]):
        allowedPresence = ["online", "idle", "dnd", "invisible"]
        url = "https://discord.com/api/v9/users/@me/settings"

        headers = {
            "authorization": self.token
        }
        if presence in allowedPresence:
            data = {
                "status": presence.lower()
            }
            try:
                resp = requests.patch(url, headers=headers, data=data)
                resp1 = json.loads(resp.text)
                if resp.status_code == 200:
                    return resp1
                else:
                    return "There was an erorr! Please check your arguments."
            except Exception:
                return "There was an erorr!\n{}".format(traceback.format_exc())

    def addFriend(self, user:str="test#0000", id:int=None):
        url = "https://discord.com/api/v9/users/@me/relationships"
        
        headers = {
            "authorization": self.token
        }

        a = user.split("#")[0]
        b = Discriminator.toDis(user.split("#")[1])
        data = {
            "username": a,
            "discriminator": b
        }
        try:
            resp = requests.post(url, headers=headers, data=data)
            if resp.status_code == 204:
                return user
            else:
                return "There was an erorr! Please check your arguments."
        except:
            url = "https://discord.com/api/v9/users/@me/relationships/" + str(id)
            
            headers = {
                "authorization": self.token
            }

            data = {}

            try:
                resp = requests.put(url, headers=headers, data=data)
                if resp.status_code == 204:
                    return user, id
                else:
                    return "There was an erorr! Please check your arguments."
            except Exception:
                return "There was an error!\n{}".format(traceback.format_exc())

    def removeFriend(self, userid:int):
        url = f"https://discord.com/api/v9/users/@me/relationships/{userid}"
        headers = {
            "authorization": self.token
        }
        try:
            resp = requests.delete(url, headers=headers)
            if resp.status_code == 204:
                return f"Removed {userid} from friend list."
            else:
                return "There was an erorr! Please check your arguments."
        except Exception:
            return "There was an error!\n{}".format(traceback.format_exc())

    def setNote(self, userid:int, note:str):
        url = f"https://discord.com/api/v9/users/@me/notes/{userid}"
        
        headers = {
            "authorization": self.token,
            "content-type": "application/json"
        }

        data = {
            "note": note
        }

        try:
            resp = requests.put(url, headers=headers, data=json.dumps(data))
            if resp.status_code == 204:
                return  f"Successfully added the note {note} to {userid}"
            else:
                return "There was an erorr! Please check your arguments."
        except Exception:
            return "There was an erorr!\n{}".format(traceback.format_exc())

    def mentionUser(self, userid:int):
        return f"<@!{userid}>"

    def getFriends(self):
        url = "https://discordapp.com/api/v6/users/@me/relationships"

        headers = {
            "authorization": self.token
        }
        
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                return json.loads(resp.text)
            else:
                return "There was an erorr! Please check your arguments"
        except Exception:
            return "There was an erorr!\n{}".format(traceback.format_exc())

    def getHeaders(self, token, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    def createDM(self, uid):
        try:
            return json.loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=self.getHeaders(self.token), data=json.dumps({"recipient_id": uid}).encode())).read().decode())["id"]
        except:
            return traceback.format_exc()
    
    def spreadMessage(self, message:str, cooldown:int):
        for friend in self.getFriends():
            try:
                channel = self.createDM(friend["id"])
                self.sendMessage(channel, message)
                time.sleep(cooldown)
            except Exception:
                return traceback.format_exc()
        return "Success"