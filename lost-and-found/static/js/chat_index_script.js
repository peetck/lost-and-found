axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'


// initial variable
var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
var current = null
var search = ''
var messages = []
var theme = 'light'

// notification sound
var notification_sound = new Audio('/static/sounds/message_notification.mp3')
notification_sound.loop = false
//notification_sound.muted = true

var send_message = new Audio('/static/sounds/send_message.mp3')
send_message.loop = false
//sendMessage.muted = true

var firstTime = true;

async function initialize(){
    await axios.get('/chats/chat_api/' + '?search=' + search)
        .then(function (response) {
            // handle success
            data = response.data[0];
            theme = response.data[1]; // update theme

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
                seen = data[i][5]

                if (firstTime){
                    displayUser(username, msg, datetime, url, id, seen, play_sound=false);
                }
                else{
                    displayUser(username, msg, datetime, url, id, seen);
                }

                if (current === null){
                    select(id, url, username)
                }
            }

            firstTime = false;

            // set css
            if (theme == 'light'){
                document.getElementsByClassName('mesgs')[0].style.backgroundColor = 'white'
                document.getElementById('mesgs_hr_bottom').style = ''
                document.getElementsByClassName('inbox_people')[0].style.backgroundColor = '#f8f8f8'
                document.getElementById('header_msg').setAttribute('class', 'mt-2 text-dark')
                if (document.getElementsByClassName('active_chat')[0] != null){
                    document.getElementsByClassName('active_chat')[0].style.backgroundColor = '#ebebeb'
                }
                document.getElementsByClassName('inbox_msg')[0].style.border = '1px solid #c4c4c4'
                document.getElementsByClassName('headind_srch')[0].style = 'padding: 10px 29px 10px 20px; overflow: hidden; border-bottom: 1px solid #c4c4c4;'

                document.getElementById('chat_to_name_href').setAttribute('class', 'text-decoration-none text-dark')
            }
            else{
                document.getElementsByClassName('mesgs')[0].style.backgroundColor = '#18191A'
                document.getElementById('mesgs_hr_bottom').style.backgroundColor = '#6C757D'
                document.getElementsByClassName('inbox_people')[0].style.backgroundColor = '#18191A'
                document.getElementById('header_msg').setAttribute('class', 'mt-2 text-light')
                if (document.getElementsByClassName('active_chat')[0] != null){
                    document.getElementsByClassName('active_chat')[0].style.backgroundColor = '#242526'
                }
                document.getElementsByClassName('inbox_msg')[0].style.border = '1px solid #18191A'
                document.getElementsByClassName('headind_srch')[0].style = 'padding: 10px 29px 10px 20px; overflow: hidden; border-bottom: 1px solid #6C757D;'

                document.getElementById('chat_to_name_href').setAttribute('class', 'text-decoration-none text-light')
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

function displayUser(username, msg, datetime, url, id, seen, play_sound=true) {

    if (document.getElementById(id)){
        last = document.getElementById(id).firstElementChild.firstElementChild.lastElementChild.firstElementChild.firstElementChild
                .nextElementSibling.getAttribute('class')
        if (last == 'fas fa-exclamation-circle' || last == 'fas fa-exclamation-circle text-light'){
            play_sound = false
        }
        document.getElementById(id).remove()
    }

    div1 = document.createElement('div')
    div1.style.border = 'none'

    div2 = document.createElement('div')
    div2.setAttribute('class', 'chat_people')

    div3 = document.createElement('div')
    div3.setAttribute('class', 'chat_img my-circle')

    img = document.createElement('img')
    img.src = url
    img.setAttribute('class', 'rounded-circle')
    img.setAttribute('style', 'height: 75px; width: 75px;')

    div3.appendChild(img)

    div4 = document.createElement('div')
    div4.setAttribute('class', 'chat_ib')

    h5 = document.createElement('h5')

    if (theme == 'light'){
        h5.innerHTML = '<b>' + username + '</b>' + ' <span class="chat_date">' + datetime + '</span>'
    }
    else{
        h5.innerHTML = '<b class="text-light font-weight-normal">' + username + '</b>' + ' <span class="chat_date text-light">' + datetime + '</span>'
    }

    p = document.createElement('p')
    p.innerText = truncatechars(msg, 100)
    if (!seen && datetime !== 'ไม่มีข้อมูล'){
        p.setAttribute('class', 'font-weight-bold')

        // sound play
        if (play_sound){
            notification_sound.play()
        }

        if (theme == 'light'){
            h5.innerHTML = '<b>' + username + '</b> ' + '<i class="fas fa-exclamation-circle"></i>' + '<span class="chat_date">' + datetime + '</span>'
        }
        else{
            h5.innerHTML = '<b class="text-light font-weight-normal">' + username + '</b> ' + '<i class="fas fa-exclamation-circle text-light"></i>' + '<span class="chat_date text-light">' + datetime + '</span>'
        }
    }
    if (datetime == 'ไม่มีข้อมูล'){
        p.innerText = 'ไม่มีข้อมูล'
    }
    div4.appendChild(h5)
    div4.appendChild(p)

    div2.appendChild(div3)
    div2.appendChild(div4)

    div1.appendChild(div2)

    inbox_chat = document.getElementById('inbox_chat')

    if (current === null || current === id){
        div1.setAttribute('class', 'chat_list active_chat')
    }
    else{
        div1.setAttribute('class', 'chat_list')
    }

    if (theme == 'light'){
        div1.style.backgroundColor = '#f8f8f8'
        div1.style = 'border-bottom: 1px solid #c4c4c4; margin: 0; padding: 18px 16px 10px;'
    }
    else{

        div1.style = 'border-bottom: 1px solid #18191A; margin: 0; padding: 18px 16px 10px;'
        div1.style.backgroundColor = '#18191A'
    }

    span = document.createElement('span')
    span.setAttribute('onclick', ' select( ' + id + ',"' + url + '",' + '"' + username + '")')
    span.setAttribute('id', id)
    span.style.cursor = 'pointer'

    span.appendChild(div1)

    inbox_chat.appendChild(span)
}

function select(id, url, username){

    current = id

    let active = document.querySelector('.active_chat')
    if (active){
        active.setAttribute('class', 'chat_list') // set to not selected
    }
    document.getElementById(current).firstElementChild.setAttribute('class', 'chat_list active_chat') // selected

    if (theme == 'light'){
        document.getElementById('chat_to_name').innerHTML = "<a class='text-decoration-none text-dark' id='chat_to_name_href' href='" + '/accounts/' + id + "'>" + username + "</a>"
    }
    else{
        document.getElementById('chat_to_name').innerHTML = "<a class='text-decoration-none text-light' id='chat_to_name_href' href='" + '/accounts/' + id + "'>" + username + "</a>"
    }
    document.getElementById('chat_to_img').setAttribute('src', url)

    getMessage(current, true)
}

async function getMessage(id, scroll) {
    await axios.get('/chats/message_api/' + id + '/')
        .then(function (response) {
            // handle success
            data = response.data;
            let gets = data.gets
            let sends = data.sends
            let get_messages = []
            let seens = []
            let i = 0;
            let j = 0;
            while (i < sends.length && j < gets.length){
                if (new Date(sends[i].timestamp) < new Date(gets[j].timestamp)){
                    sends[i]['type'] = 'send'
                    get_messages.push(sends[i])
                    seens.push(sends[i]['seen'])
                    i++
                }
                else{
                    gets[j]['type'] = 'get'
                    get_messages.push(gets[j])
                    seens.push(gets[j]['seen'])
                    j++
                }
            }
            while (i < sends.length){
                sends[i]['type'] = 'send'
                get_messages.push(sends[i])
                seens.push(sends[i]['seen'])
                i++
            }
            while (j < gets.length){
                gets[j]['type'] = 'get'
                get_messages.push(gets[j])
                seens.push(gets[j]['seen'])
                j++
            }

            messages = get_messages

            let position = document.getElementById('msg_history').scrollTop // save last position
            let bottom = document.getElementById('msg_history').scrollHeight - document.getElementById('msg_history').clientHeight

            displayMessage(data.url, seens, id)

            document.getElementById('msg_history').scrollTop = position;

            if (scroll || position == bottom){
                /* make it bottom */
                makeChatHistoryBottom()
            }
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        })
}

function displayMessage(url, seens, id){
    let msg_history = document.getElementById('msg_history')
    msg_history.innerHTML = ''

    for (let i = 0; i < messages.length; i++){
        let message = messages[i]
        let seen = seens[i]

        if (message.type == 'send'){
            let div = createOutGoingMessage(message)
            msg_history.append(div)

            if (seen) {
                div.querySelector('.time_date').innerText += ' (อ่านแล้ว) '
            }
        }
        else if (message.type == 'get'){
            let div = createInComingMessage(message, url, id)
            msg_history.append(div)
        }
    }
    initialize() // because we need to display user on the left div
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
    p.setAttribute('class', 'bg-dark text-light')
    p.innerText = message.message

    let span = document.createElement('span')
    span.setAttribute('class', 'time_date')
    let datetime = new Date(message.timestamp)
    span.innerText = datetime.getHours() + ":" + ((datetime.getMinutes() < 10 ? '0' : '') + datetime.getMinutes()) + " | " + months[datetime.getMonth()] + " " + datetime.getDate()

    // append
    div2.append(p)
    div2.append(span)

    div.append(div2)

    return div
}

function createInComingMessage(message, url, id){
/*
    <div class="incoming_msg">
        <div class="incoming_msg_img my-circle">
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
    div2.setAttribute('class', 'incoming_msg_img my-circle')

    let a = document.createElement('a')
    a.setAttribute('href', '/accounts/' + id + '/')

    let img = document.createElement('img')
    img.setAttribute('src', url)
    img.setAttribute('style', 'height: 60px; width: 60px;')
    img.setAttribute('class', 'rounded-circle')

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
    span.innerText = datetime.getHours() + ":" + ((datetime.getMinutes() < 10 ? '0' : '') + datetime.getMinutes()) + " | " + months[datetime.getMonth()] + " " + datetime.getDate()

    // append

    div4.append(p)
    div4.append(span)

    div3.append(div4)

    a.append(img)
    div2.append(a)

    div.append(div2)
    div.append(div3)

    return div
}

async function sendMessage(msg){
    await axios.post('/chats/message_api/' + current + '/', {
        message : msg
    })
        .then(function (response) {
            // send message success
            getMessage(current, true)
            send_message.play()
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        })
}

/* truncatechars function */
function truncatechars(text, lim) {
    if (text.length > lim){
        return text.substring(0, lim - 1) + "...";
    }
    return text;
}

function changeTheme(change_to){
    axios.patch('/chats/chat_api/', {
        change_to : change_to
    })
    .then(function (response) {
        initialize()
    })
    .catch(function (error){
        console.log(error)
    })

}

$('#send_message_input').on('keydown', function(e){
    if (e.key === 'Enter' && e.currentTarget.value.trim() !== ''){
        sendMessage(e.currentTarget.value);
        e.currentTarget.value = ''
    }
})

$('#send_message_btn').on('click', function(){
    if ($('#send_message_input').val().trim() !== ''){
        sendMessage($('#send_message_input').val());
        $('#send_message_input').val('')
    }
})

$('#search_user').on('keyup', function(e){
    search = e.currentTarget.value;
    $('#inbox_chat').html('')
    initialize();
})

$('#toggle--daynight').on('change', function(e){
    checked = $('#toggle--daynight:checked').val();

    if (checked){
        // light theme
        changeTheme('light')
    }
    else{
        // dark theme
        changeTheme('dark')
    }


})


initialize();

setInterval(function(){
    getMessage(current, false);
}, 2000)