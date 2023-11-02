
async function rejectFriend(friend_id, user_id, li) {
    /*
    Sends the id of the requester and the active user to the server to remove the request
    If the status comes back successful the list element is removed
    If there are no more requests, it displays 'No friends requests!'
    */
    response = await fetch('/friends/decline', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({friend_id, user_id})
    });
    if (await response.status === 201) {
        li.remove();
    }
    if (requestList.children.length === 0) {
        requestList.textContent = 'No friend requests!'
    }
}


async function addFriend(friend_id, user_id, li) {
    /*
    Sends the id of the requester and the active user to the server to add friend
    If the status comes back successful the list element is removed
    If there are no more requests, it displays 'No friends requests!'
    */
    response = await fetch('/friends/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({friend_id, user_id})
    });
    if (await response.status === 201) {
        li.remove();
    }
    if (requestList.children.length === 0) {
        requestList.textContent = 'No friend requests!'
    }
}

requestList = document.querySelector('#request-list');

function makeRequestElement(data, user_id) {
    /*
    Creates the li elements the relevent buttons
    to be added to the request list
    
    It also adds event listeners for the buttons to
    reject or accept the friend request
    */

    data.forEach(request => {
        const li = document.createElement('li');
        li.classList.add('request')

        // Create element to hold username
        const usernameElement = document.createElement('span')
        usernameElement.textContent=request.from_username;
        li.appendChild(usernameElement)

        // Create button container and buttons, append them to li element
        const buttonContainer = document.createElement('div')
        buttonContainer.classList.add('requestButtonContainer')

        const acceptButton = document.createElement('button')
        acceptButton.classList.add('accept')
        acceptButton.textContent = 'V'
        buttonContainer.appendChild(acceptButton)
        // Add event listener to accept request
        acceptButton.onclick = () => {
            addFriend(request.from_user_id, user_id, li);
            if (requestList.children.length === 0) {
                requestList.textContent = 'No friend requests!'
            }
        }

        // Create button container and buttons, append them to li element
        const declineButton = document.createElement('button')
        declineButton.classList.add('decline')
        declineButton.textContent = 'X'
        buttonContainer.appendChild(declineButton)
        // Add event listener to decline request
        declineButton.onclick = () => {
            rejectFriend(request.from_user_id, user_id, li);
        }

        li.appendChild(buttonContainer)

        requestList.appendChild(li);
    });
}


// Example response data
// {"data":[{"from_user_id":2,"from_username":"user2"},{"from_user_id":3,"from_username":"user3"}],"status":"success"}
async function fetchRequests() {

    /*
    Uses fetch to get all friend request for a user and 
    displays them on the homepage
    */
    user_id = -1

    try {
        response = await fetch(`http://localhost:5000/auth/get_user_id`, {
        method: 'GET'
    });

    if (response.ok) {
        const data = await response.json();
        user_id = data.id
    }

    } catch (error) {
    console.error('Error:', error);
    }

    try {
      const response = await fetch(`http://localhost:5000/friends/request/${user_id}`, {
        method: 'GET'
      });

      if (response.ok) {
        const data = await response.json();

        if (data.data.length != 0){
            makeRequestElement(data.data, user_id)
            return
        }  
      }

      // If no friend requests returned
      requestList.textContent = 'No friend requests!'

    } catch (error) {
      console.error('Error:', error);
    }
  }



  friendList = document.querySelector('#friend-list')


  function makeFriendElement(data) {
    /*
    Creates the li elements the relevent buttons
    to be added to the request list
    
    It also adds event listeners for the buttons to
    reject or accept the friend request
    */

    data.forEach(request => {
        const li = document.createElement('li');
        li.classList.add('request')

        // Create element to hold username
        const usernameElement = document.createElement('span')
        usernameElement.textContent=request.friend_username;
        li.appendChild(usernameElement)

        friendList.appendChild(li);
    });
}

  async function fetchFriends() {

    /*
    Uses fetch to get all friend request for a user and 
    displays them on the homepage
    */
    user_id = -1

    try {
        response = await fetch(`http://localhost:5000/auth/get_user_id`, {
        method: 'GET'
    });

    if (response.ok) {
        const data = await response.json();
        user_id = data.id
    }

    } catch (error) {
    console.error('Error:', error);
    }

    try {
      const response = await fetch(`http://localhost:5000/friends/${user_id}`, {
        method: 'GET'
      });

      if (response.ok) {
        const data = await response.json();

        if (data.data.length != 0){
            makeFriendElement(data.data)
            return
        }  
      }

      // If no friend requests returned
      friendList.textContent = 'No friends :('

    } catch (error) {
      console.error('Error:', error);
    }
  }


fetchRequests();
fetchFriends();
