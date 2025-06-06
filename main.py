import requests
import time

def get_user_avatar_by_id(user_id):
    """
    Fetches the avatar URL of a user by their ID.
    
    Args:
        user_id (str): The ID of the user.
    
    Returns:
        str: The URL of the user's avatar.
    """
    url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=48x48&format=Png&isCircular=false"
    response = requests.get(url)
    
    return response.json().get("data")[0].get("imageUrl")
    
def get_user_avatars_by_tokens(playerTokens):
    url = "https://thumbnails.roblox.com/v1/batch"
    data = [
        {
            "token": token,
            "type": "AvatarHeadShot",
            "size": "48x48",
            "isCircular": False
        }
        for token in playerTokens
    ]
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    image_urls = [item["imageUrl"] for item in response.json().get("data", [])]
    return image_urls

def get_id_from_user(username):
    """
    Retrieves the user ID from a given username.

    Args:
        username (str): The username of the user.

    Returns:
        str: The user ID of the user, or None if the user does not exist.
    """
    url = "https://users.roblox.com/v1/usernames/users"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "usernames": [username],
        "excludeBannedUsers": False
    }
    response = requests.post(url, json=data, headers=headers)
    user_data = response.json().get("data", [])
    
    if len(user_data) == 0:
        return None
    
    return user_data[0].get("id")

def find_player_in_servers(place_id, user_avatar_url, min_player_count):
    """
    Searches for a player in Roblox servers by their avatar URL.

    Args:
        place_id (str): The ID of the Roblox place.
        user_avatar_url (str): The avatar URL of the player to find.
        min_player_count (int): The minimum number of players in a server to consider.

    Returns:
        bool: True if the player is found and teleported, False otherwise.
    """
    cursor = ""
    page = 1
    found = False
    job_id = None
    while not found:
        print(f"Retrieving server list... (page {page})")
        url = f"https://games.roblox.com/v1/games/{place_id}/servers/Public?sortOrder=Asc&limit=100"
        if cursor:
            url += f"&cursor={cursor}"
        
        response = requests.get(url)
        data = response.json()

        for i, server in enumerate(data.get("data", []), start=1):
            if server.get("playing", 0) < min_player_count:
                continue

            print(f"Scanning servers (page {page} - {i}/{len(data['data'])} - {server['playing']} online)")
            server_avatar_urls = get_user_avatars_by_tokens(server.get("playerTokens", []))

            if user_avatar_url in server_avatar_urls:
                print("Player found, teleporting...")
                job_id = server['id']
                found = True
                break

        if found:
            break

        cursor = data.get("nextPageCursor", "")
        page += 1

    if not found:
        print("Error: The player was not found on the specified place")
    
    return found, job_id

if __name__ == "__main__":
    username = input("Enter the username: ")
    place_id = input("Enter the place ID: ")
    min_player_count = int(input("Enter the minimum player count: "))

    user_id = get_id_from_user(username)
    if not user_id:
        print("User not found.")
        exit(1)

    user_avatar_url = get_user_avatar_by_id(user_id)
    print(f"Avatar URL: {user_avatar_url}")

    found, job_id = find_player_in_servers(place_id, user_avatar_url, min_player_count)
    if found:
        print("Player found, use this command in your browser's console to join:")
        print(f'''Roblox.GameLauncher.joinGameInstance("{place_id}", "{job_id}")''')
    else:
        print("Player not found.")