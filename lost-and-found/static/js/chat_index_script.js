axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
current = null

function initialize(){

    axios.get('/chats/chat_api/')
        .then(function (response) {
            // handle success
            data = response.data;
            console.log(data)
            for (var i = 0; i < data.length; i++) {
                username = data[i][0]
                msg = data[i][1]
                if (data[i][2] === '') {
                    datetime = 'ไม่มีข้อมูล';
                }
                else {
                    dateobject = new Date(data[i][2]);
                    datetime = months[dateobject.getMonth()] + " " + dateobject.getDate();
                }
                url = data[i][3]
                id = data[i][4]
                addUser(username, msg, datetime, url, id);

                if (i == 0){
                    getMessage(id, url)
                }
            }
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        })
}

function makeChatHistoryBottom() {
    var msg_history = document.querySelector('#msg_history');
    msg_history.scrollTop = msg_history.scrollHeight - msg_history.clientHeight;
}

function addUser(username, msg, datetime, url, id) {
    div1 = document.createElement('div')

    div2 = document.createElement('div')
    div2.setAttribute('class', 'chat_people')

    div3 = document.createElement('div')
    div3.setAttribute('class', 'chat_img')

    img = document.createElement('img')
    img.src = url
    img.setAttribute('class', 'rounded-circle')
    img.setAttribute('style', 'height: 75px; width: 75px;')

    div3.appendChild(img)

    div4 = document.createElement('div')
    div4.setAttribute('class', 'chat_ib')

    h5 = document.createElement('h5')
    h5.innerHTML = '<b>' + username + '</b>' + ' <span class="chat_date">' + datetime + '</span>'

    p = document.createElement('p')
    p.innerHTML = msg

    div4.appendChild(h5)
    div4.appendChild(p)

    div2.appendChild(div3)
    div2.appendChild(div4)

    div1.appendChild(div2)

    inbox_chat = document.getElementById('inbox_chat')

    if (inbox_chat.children.length === 0) {
        div1.setAttribute('class', 'chat_list active_chat')
    }
    else {
        div1.setAttribute('class', 'chat_list')
    }

    span = document.createElement('span')
    span.setAttribute('onclick', 'getMessage(' + id + ',"' + url + '")')
    span.setAttribute('id', id)
    span.style.cursor = 'pointer'

    span.appendChild(div1)

    inbox_chat.appendChild(span)
}

function getMessage(id, url) {
    axios.get('/chats/message_api/' + id + '/')
        .then(function (response) {
            // handle success

            current = id

            data = response.data;
            let gets = data.gets
            let sends = data.sends
            let messages = []
            let i = 0;
            let j = 0;
            while (i < sends.length && j < gets.length){
                if (new Date(sends[i].timestamp) < new Date(gets[j].timestamp)){
                    sends[i]['type'] = 'send'
                    messages.push(sends[i])
                    i++
                }
                else{
                    gets[j]['type'] = 'get'
                    messages.push(gets[j])
                    j++
                }
            }
            while (i < sends.length){
                sends[i]['type'] = 'send'
                messages.push(sends[i])
                i++
            }
            while (j < gets.length){
                gets[j]['type'] = 'get'
                messages.push(gets[j])
                j++
            }
            displayMessage(messages, url)
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        })
}

function displayMessage(messages, url){
    let msg_history = document.getElementById('msg_history')
    msg_history.innerHTML = ''

    for (let i = 0; i < messages.length; i++){
        let message = messages[i]

        if (message.type == 'send'){
            let div = createOutGoingMessage(message)
            msg_history.append(div)
        }
        else if (message.type == 'get'){
            let div = createInComingMessage(message, url)
            msg_history.append(div)
        }
    }
    makeChatHistoryBottom();
}

function createOutGoingMessage(message){
    /*
    <div class="outgoing_msg">
        <div class="sent_msg">
            <p class='bg-dark'> {{ message }} </p>
            <span class="time_date"> 11:01 AM | June 9</span>
        </div>
    </div>
    */
    let div = document.createElement('div')
    div.setAttribute('class', 'outgoing_msg')

    let div2 = document.createElement('div')
    div2.setAttribute('class', 'sent_msg')

    let p = document.createElement('p')
    p.setAttribute('class', 'bg-dark')
    p.innerText = message.message

    let span = document.createElement('span')
    span.setAttribute('class', 'time_date')
    let datetime = new Date(message.timestamp)
    span.innerText = datetime.getHours() + ":" + datetime.getMinutes() + " | " + months[datetime.getMonth()] + " " + datetime.getDate()

    // append
    div2.append(p)
    div2.append(span)

    div.append(div2)

    return div
}

function createInComingMessage(message, url){
/*
    <div class="incoming_msg">
        <div class="incoming_msg_img">
            <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil">
        </div>
        <div class="received_msg">
            <div class="received_withd_msg">
                <p class='bg-dark text-light'> -- </p>
                <span class="time_date"> 11:01 AM | Today</span>
            /div>
        </div>
    </div>
*/
    let div = document.createElement('div')
    div.setAttribute('class', 'incoming_msg')

    let div2 = document.createElement('div')
    div2.setAttribute('class', 'incoming_msg_img')

    let img = document.createElement('img')
    img.setAttribute('src', url)

    let div3 = document.createElement('div')
    div3.setAttribute('class', 'received_msg')

    let div4 = document.createElement('div')
    div4.setAttribute('class', 'received_withd_msg')

    let p = document.createElement('p')
    p.setAttribute('class', 'bg-dark text-light')
    p.innerText = message.message

    let span = document.createElement('span')
    span.setAttribute('class', 'time_date')
    let datetime = new Date(message.timestamp)
    span.innerText = datetime.getHours() + ":" + datetime.getMinutes() + " | " + months[datetime.getMonth()] + " " + datetime.getDate()

    // append

    div4.append(p)
    div4.append(span)

    div3.append(div4)

    div2.append(img)

    div.append(div2)
    div.append(div3)

    return div
}

function sendMessage(msg){
    axios.post('/chats/message_api/' + current + '/', {
        message : msg
    })
        .then(function (response) {
            // send message success
            let msg_history = document.getElementById('msg_history')
            let datetime = new Date(response.data.timestamp)
            msg_history.append(createOutGoingMessage(response.data))

            document.getElementById(current).firstElementChild.firstElementChild.lastElementChild.lastElementChild.innerHTML = response.data.message

            document.getElementById(current).firstElementChild.firstElementChild.lastElementChild.firstElementChild.lastElementChild.innerHTML = months[datetime.getMonth()] + " " + datetime.getDate()

            makeChatHistoryBottom();
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        })
}

$('#send_message_input').on('keydown', function(e){
    if (e.key === 'Enter'){
        sendMessage(e.currentTarget.value);
    }
})

$('#send_message_btn').on('click', function(){
    sendMessage($('#send_message_input').val());
})



initialize();